"""
Models for the online course application.
"""
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Course(models.Model):
    """Course model."""
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField('Instructor')
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return "Name: " + self.name + "," + "Description: " + self.description

class Lesson(models.Model):
    """Lesson model."""
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Title: " + self.title + "," + "Content: " + self.content

class Enrollment(models.Model):
    """Enrollment model."""
    AUDIT = 'audit'
    HONOR = 'honor'
    COURSE_MODES = [(AUDIT, 'Audit'), (HONOR, 'Honor')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

class Instructor(models.Model):
    """Instructor model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    """Learner model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    occupation = models.CharField(null=False, max_length=20, default="student")
    social_link = models.URLField(max_length=50)

    def __str__(self):
        return "user_name: " + self.user.username + "," + "occupation: " + self.occupation

class Question(models.Model):
    """Question model - stores exam questions for a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.content

    def is_get_score(self, selected_ids):
        """Check if all correct answers are selected."""
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(
            is_correct=True, id__in=selected_ids).count()
        return all_answers == selected_correct

class Choice(models.Model):
    """Choice model - stores choices for each question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content

class Submission(models.Model):
    """Submission model - stores an exam submission."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id} for {self.enrollment}"
