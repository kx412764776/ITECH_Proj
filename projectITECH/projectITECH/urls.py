from django.urls import path
from course.views import login, register, staff, student


urlpatterns = [

    ########################################

    # Reset password
    path("<int:staffid>/staff-reset/", staff.staff_reset),

    path("<int:studentid>/student-reset/", student.student_reset),

    ########################################

    # Course management
    path("course-management/", staff.course_management),
    path("course-add/", staff.course_add),
    path("<int:courseid>/course-edit/", staff.course_edit),
    path("<int:courseid>/course-delete/", staff.course_delete),

    ########################################

    # View reviews
    path("student-list/", staff.student_list),
    path("<int:studentid>/view-reviews-student/", staff.view_reviews_student),

    path("course-list/", staff.course_list),
    path("<int:courseid>/view-reviews-course/", staff.view_reviews_course),

    ########################################

    # Data visualisation
    path("data-visualisation/", staff.data_visualisation),
    path("data-visualisation/gender-distribution-socs/", staff.gender_distribution_socs),
    path("data-visualisation/degree-programme-enrolment/", staff.degree_programme_enrolment),

    ########################################

    # Login
    path("captcha/", login.captcha),
    path("login/", login.student_login),
    path("staff-login/", login.staff_login),
    path("logout/", login.logout),
    path("staff-logout/", login.staff_logout),

    ########################################

    # Registration
    path("registration/", register.student_registration),
    path("staff-registration/", register.staff_registration),

    ########################################

    path("student-info/", student.student_info),
    path("student-edit/", student.student_edit),
    path('student-course/', student.student_course),
    path('student/addcomment/', student.student_add_comment),
    path('student-comment/', student.student_comment),

]
