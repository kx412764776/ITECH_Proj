# Generated by Django 4.1.3 on 2023-02-27 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0002_rename_degree_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="degreeprogramme",
            name="programme_courses",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="programme_courses", to="course.course"
            ),
        ),
    ]