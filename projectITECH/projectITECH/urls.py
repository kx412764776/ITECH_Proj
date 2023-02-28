from django.contrib import admin
from django.urls import path
from rmc import views


urlpatterns = [
    path("admin/", admin.site.urls),


    path("student-list/", views.student_list),
]
