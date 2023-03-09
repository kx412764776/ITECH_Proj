from django.contrib import admin
from django.urls import path
from rmc import views


urlpatterns = [
    path("admin/", admin.site.urls),

    ########################################

    # path("<int:staffid>/staff-info/", admin.staff_info),

    ########################################

    path("course-management/", views.course_management),
    path("course-add/", views.course_add),
    path("<int:courseid>/course-edit/", views.course_edit),
    path("<int:courseid>/course-delete/", views.course_delete),

    ########################################

    path("student-list/", views.student_list),
    path("<int:studentid>/view-reviews-student/", views.view_reviews_student),

    ########################################

    path("login/", views.login),
    path("logout/", views.logout),

    ########################################

    path("student/info/", views.student_info),
    path("student/edit/", views.user_edit),

]
