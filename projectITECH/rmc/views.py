from django.shortcuts import render, redirect
from rmc import models
from rmc.utils.bootstrap import BootStrapModelForm
from rmc.utils.pagination import Pagination


########################################

def course_management(request):
    # Gets all the data in the rmc_course
    # associated_degree_programmes = models.ManyToManyField(to="DegreeProgramme", related_name="degree_programme_courses")
    courses = models.Course.objects.prefetch_related("associated_degree_programmes").all()

    pagination_object = Pagination(request, courses)

    contents = {
        # Organises the retrieved data with pagination
        "queryset": pagination_object.queryset_page,

        # Generates front-end code for pagination
        "tpl_pagination_navbar": pagination_object.tpl(),
    }

    # Sends the queryset to the front-end
    return render(request, "course-management.html", contents)


class CourseModelForm(BootStrapModelForm):
    class Meta:
        model = models.Course
        fields = ["name", "associated_degree_programmes"]

def course_add(request):
    # (1) Calls the html page and passes the database data if a GET request is received
    if request.method == "GET":
        # (1.1) Instantiates a ModelForm object
        form = CourseModelForm()

        # (1.2) Sends the ModelForm instance to the front-end
        return render(request, "course-add.html", {"form": form})

    # (2) Gets the user input (a ModelForm instance) from the front-end POST request
    form = CourseModelForm(data=request.POST)

    # (3) Validates the user input
    if form.is_valid():
        # print(form.cleaned_data)

        # Saves the user input into the database
        form.save()
        return redirect("/course-management/")
    else:
        # print(form.errors)

        # Sends the error messages to the front-end
        return render(request, "course-add.html", {"form": form})


def course_edit(request, courseid):
    # (1) Receives the course ID via URL
    # http://127.0.0.1:8000/1/course-edit/

    # (2.1) Gets the existing data from the database according to the course ID
    row_object = models.Course.objects.filter(id=courseid).first()

    # (2) Calls the html page and passes the database data if a GET request is received
    if request.method == "GET":
        # (2.1) Gets the existing data from the database according to the course ID
        # row_object = models.Course.objects.filter(id=courseid).first()

        # (2.2) Instantiates a ModelForm object and passes the existing database data
        form = CourseModelForm(instance=row_object)

        # (2.3) Sends the ModelForm instance to the front-end
        return render(request, "course-edit.html", {"form": form})

    # (3) Gets the user input (a ModelForm instance) from the front-end POST request,
    # and updates the existing database data
    # row_object = models.Course.objects.filter(id=courseid).first()
    form = CourseModelForm(data=request.POST, instance=row_object)

    # (4) Validates the user input
    if form.is_valid():
        # Saves the user input into the database
        form.save()
        return redirect("/course-management/")

    # (5) Sends the error messages to the front-end
    return render(request, "course-edit.html", {"form": form})


def course_delete(request, courseid):
    models.Course.objects.filter(id=courseid).delete()
    return redirect("/course-management/")

########################################

def student_list(request):
    # Gets all the data in the rmc_student
    students = models.Student.objects.all()

    pagination_object = Pagination(request, students)

    contents = {
        # Organises the retrieved data with pagination
        "queryset": pagination_object.queryset_page,

        # Generates front-end code for pagination
        "tpl_pagination_navbar": pagination_object.tpl(),
    }

    # Sends the queryset to the front-end
    return render(request, "student-list.html", contents)


def view_reviews_student(request, studentid):
    # (1) Receives the student ID via URL
    # http://127.0.0.1:8000/1/view-reviews-student/

    # (2) Gets the existing data from the database according to the student ID
    reviews = models.CourseReview.objects.filter(student_id=studentid)

    # (3) Extracts the student name from the queryset for display
    for row in reviews:
        student_name = row.student_id.name

    pagination_object = Pagination(request, reviews)

    contents = {
        "student_name": student_name,

        # Organises the retrieved data with pagination
        "queryset": pagination_object.queryset_page,

        # Generates front-end code for pagination
        "tpl_pagination_navbar": pagination_object.tpl(),
    }

    # (4) Sends the queryset to the front-end
    return render(request, "view-reviews-student.html", contents)










# def staff_info(request, staffid):
#     queryset = models.Staff.objects.filter(id=staffid).first()
#
#     return render(request, "staff-info.html", queryset)






def admin_list(request):
        # queryset = models.Admin.objects.all()

        ########################################
        # Search box
        data_dict = {}
        search_data = request.GET.get("search", "")
        if search_data:
            data_dict["username__contains"] = search_data

        queryset = models.Admin.objects.filter(**data_dict)
        ########################################
        # Pagination
        pagination_object = Pagination(request, queryset)

        context = {
            "search_data": search_data,
            "queryset": pagination_object.queryset_page,
            "tpl_pagination_navbar": pagination_object.tpl(),
        }
        ########################################

        return render(request, "admin-list.html", context)








