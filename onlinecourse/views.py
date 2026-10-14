"""Views for the onlinecourse application."""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission

def index(request):
    """Render the homepage with list of courses."""
    courses = Course.objects.all()
    return render(request, 'onlinecourse/index.html', {'courses': courses})

def course_details(request, course_id):
    """Show details for a course."""
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html',
                  {'course': course})

def enroll(request, course_id):
    """Enroll the current user in a course."""
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    Enrollment.objects.get_or_create(user=user, course=course, mode='honor')
    return HttpResponseRedirect(reverse('onlinecourse:course_details',
                                        args=(course.id,)))

def submit(request, course_id):
    """Handle exam submission."""
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    selected_ids = [int(x) for x in request.POST.getlist('choice')]
    for choice_id in selected_ids:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)
    submission.save()
    return redirect(reverse('onlinecourse:show_exam_result',
                            args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    """Show exam results for a submission."""
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = list(submission.choices.values_list('id', flat=True))

    total_score = 0
    questions = []
    for question in course.question_set.all():
        is_correct = question.is_get_score(selected_ids)
        if is_correct:
            total_score += question.grade
        questions.append({
            'question': question,
            'is_correct': is_correct,
            'choices': question.choice_set.all(),
        })

    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'questions': questions,
    })
