from django.contrib import admin
from django.urls import path
from rmc import views


urlpatterns = [
    path("admin/", admin.site.urls),


    path("course-management/", views.course_management),
    path("course-add/", views.course_add),
    path("<int:courseid>/course-edit/", views.course_edit),

    path("student-list/", views.student_list),
]
