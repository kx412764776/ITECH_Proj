from django.shortcuts import render, redirect
from rmc import models


def course_management(request):
    # Gets all the data in the rmc_course
    # associated_degree_programmes = models.ManyToManyField(to="DegreeProgramme", related_name="degree_programme_courses")
    courses = models.Course.objects.prefetch_related("associated_degree_programmes").all()

    # Sends the queryset to the front-end
    return render(request, "course-management.html", {"courses": courses})


def student_list(request):
    # Gets all the data in the rmc_student
    queryset = models.Student.objects.all()

    # Sends the queryset to the front-end
    return render(request, "student-list.html", {"queryset": queryset})




