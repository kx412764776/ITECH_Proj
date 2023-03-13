from django.contrib import admin
from django.urls import path
from rmc import views


urlpatterns = [
    path("admin/", admin.site.urls),

    ########################################

    path("<int:staffid>/staff-reset/", views.staff_reset),
    path("<int:studentid>/student-reset/", views.student_reset),

    ########################################

    path("course-management/", views.course_management),
    path("course-add/", views.course_add),
    path("<int:courseid>/course-edit/", views.course_edit),
    path("<int:courseid>/course-delete/", views.course_delete),

    ########################################

    path("student-list/", views.student_list),
    path("<int:studentid>/view-reviews-student/", views.view_reviews_student),

    path("course-list/", views.course_list),
    path("<int:courseid>/view-reviews-course/", views.view_reviews_course),

    ########################################

    path("captcha/", views.captcha),
    path("login/", views.student_login),
    path("staff-login/", views.staff_login),
    path("logout/", views.logout),
    path("staff-logout/", views.staff_logout),

    path("registration/", views.student_registration),
    path("staff-registration/", views.staff_registration),

    ########################################

    path("data-visualisation/", views.data_visualisation),
    path("data-visualisation/gender-distribution-socs/", views.gender_distribution_socs),
    path("data-visualisation/degree-programme-enrolment/", views.degree_programme_enrolment),

    ########################################

    path("student-info/", views.student_info),
    path("student-edit/", views.student_edit),
    path('student-course/', views.student_course),
    path('student-addcomment/', views.student_addcomment),
    path('student-comment/', views.student_comment),

]
