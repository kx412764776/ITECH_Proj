from django.db import models


# (1) Table student
class Student(models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)

    gender_choices = (
        (1, "Male"),
        (2, "Female"),
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices)

    age = models.IntegerField(verbose_name="Age")
    entry_date = models.DateField(verbose_name="Date of entry")

    degree_programme = models.ForeignKey(to="DegreeProgramme", to_field="id", on_delete=models.CASCADE)


# (2) Table course
class Course(models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)
    associated_degree_programme = models.ManyToManyField(to="DegreeProgramme", related_name="associated_degree_programme")


# (3) Table coursereview
class CourseReview(models.Model):
    student_id = models.ForeignKey(to="Student", to_field="id", on_delete=models.CASCADE)
    course_id = models.ForeignKey(to="Course", to_field="id", on_delete=models.CASCADE)

    overall_score = models.IntegerField(verbose_name="Overall score")
    easiness_score = models.IntegerField(verbose_name="Easiness score")
    interest_score = models.IntegerField(verbose_name="Interest score")
    usefulness_score = models.IntegerField(verbose_name="Usefulness score")
    teaching_score = models.IntegerField(verbose_name="Teaching score")

    comment = models.CharField(max_length=300, default='')


# (4) Table degreeprogramme
class DegreeProgramme(models.Model):
    name = models.CharField(verbose_name="Degree programme name", max_length=32)
    level_choices = (
        (1, "Undergraduate"),
        (2, "Postgraduate"),
    )
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choices)

    programme_courses = models.ManyToManyField(to="Course", related_name="programme_courses")


# (5) Table staff
class Degree(models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)

    gender_choices = (
        (1, "Male"),
        (2, "Female"),
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices)

