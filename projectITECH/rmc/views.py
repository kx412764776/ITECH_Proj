from django.shortcuts import render, redirect
from rmc import models


def student_list(request):
    # Gets all the data in the rmc_student
    queryset = models.Student.objects.all()

    # Sends the queryset to the front-end
    return render(request, "student-list.html", {"queryset": queryset})




