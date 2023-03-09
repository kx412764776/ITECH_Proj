from io import BytesIO

from django import forms
from django.shortcuts import render, redirect

from rmc import models
from rmc.utils.bootstrap import BootStrapModelForm, BootStrapForm
from rmc.utils.pagination import Pagination
from rmc.utils.encrypt import md5


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







def student_info(request):
    info = request.session["info"]

    # Get the data in rmc_student based on the login ID
    student = models.Student.objects.get(email=info['email'])
    stu_info = {
        "email": student.email,
        "name": student.name,
        "gender": student.get_gender_display(),
        "age": student.age,
        "entry_date": student.entry_date.strftime("%Y-%m-%d"),
        "degree_programme": student.degree_programme.name,
    }
    return render(request, "student_info.html", {"stu_info": stu_info})


class StudentInfoModelForm(BootStrapModelForm):
    class Meta:
        model = models.Student
        fields = ['name', 'gender', 'age']


def user_edit(request):
    """ Edit Student Profile """
    info = request.session["info"]
    student = models.Student.objects.filter(id=info['id']).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = StudentInfoModelForm(instance=student)

        return render(request, 'student_edit.html', {"form": form})

    form = StudentInfoModelForm(data=request.POST, instance=student)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/student/info/')
    return render(request, 'student_edit.html', {"form": form})


class LoginForm(BootStrapForm):
    email = forms.CharField(
        label="email",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    # def clean_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        user_object = models.Student.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "email or password error")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'email': user_object.email}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/student/info/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')



