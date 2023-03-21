# Create your tests here.
import sqlite3
import pytest
from django.db import connection
from rmc.models import *
import html
from rmc.utils.encrypt import md5

host = 'http://127.0.0.1:8000'


def customer_sqllite_operation(sql_statement, limit_one=True):
    '''sqllite custom query'''

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    db_path = connection.settings_dict['NAME']
    with sqlite3.connect(db_path, uri=True) as conn:
        # Make the query return as a dictionary
        conn.row_factory = dict_factory
        c = conn.cursor()
        result = c.execute(sql_statement)
        if limit_one:
            result = result.fetchone()
        else:
            result = result.fetchall()
        conn.commit()
    return result


def out_html_text(text):
    '''Convert string to html characters'''
    return html.escape(text)


def html_text_to_text(html_text):
    '''Convert html characters to strings''''
    h = html.parser
    return h.unescape(html_text)


class TestCaseStudentModel(object):
    """
    Model testing
    """

    student_name = 'test'

    # print("degree_programme_names:",degree_programme_names)

    @pytest.mark.skip('A mod with a foreign key is temporarily unable to complete the test, use @pytest.mark.django_db cant find data')
    def test_student_model(self):
        self.student_name += '1'
        # degree_programme=DegreeProgramme.objects.
        sql_statement = '''select * from rmc_degreeprogramme '''
        degree_programme_names = customer_sqllite_operation(sql_statement=sql_statement, limit_one=False)
        for degree_programme in degree_programme_names:
            kwargs = {'email': f'{self.student_name}@qq.com', 'name': self.student_name, 'password': md5('test123456'),
                      'gender': 1, 'age': 20, 'entry_date': '2022-09-06',
                      'degree_programme': degree_programme.get('name')}
            result = Student.objects.create(**kwargs)
            query_result = Student.objects.get(name=self.student_name)
            assert query_result

    @pytest.mark.skip('A mod with a foreign key is temporarily unable to complete the test, use @pytest.mark.django_db cant find data')
    def test_course_model(self):
        pass

    @pytest.mark.skip('A mod with a foreign key is temporarily unable to complete the test, use @pytest.mark.django_db cant find data')
    def test_course_review_model(self):
        pass

    @pytest.mark.django_db
    @pytest.mark.parametrize('level', [1, 2])
    @pytest.mark.parametrize('name', ['test1', 'test2'])
    def test_degreeprogramme_model(self, name, level):
        result = DegreeProgramme.objects.create(name=name, level=level)
        assert result

    @pytest.mark.django_db
    def test_Staff_model(self):
        self.student_name += '1'
        kwargs = {'email': f'{self.student_name}@qq.com', 'name': self.student_name, 'password': md5('test123456'),
                  'gender': 1}
        result = Staff.objects.create(**kwargs)
        assert result


class TestCaseStudentView(object):
    '''Testing the student-side view'''

    @pytest.mark.parametrize('gender,name,age', ([1, 'Ruijun+Jiang2', -1], [2, 'test', 20], [1, 'Ruijun+Jiang', 100]))
    @pytest.mark.run(order=1)
    def test_view_student_edit_success(self, student_login, gender, name, age):
        session, headers, csrf_token_form_data = student_login
        data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.post(url=f'{host}/student-edit/', data=data, headers=headers)
        assert response.status_code == 200
        assert str(gender) in response.text

    @pytest.mark.parametrize('page', [1, 2, -1, ''])
    @pytest.mark.run(order=2)
    def test_view_student_course_page_success(self, student_login, page):
        session, headers, csrf_token_form_data = student_login
        data = f'page={page}'
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.get(url=f'{host}/student-course/', data=data, headers=headers)
        assert response.status_code == 200

    @pytest.mark.parametrize('page', [1, 2, -1, ''])
    @pytest.mark.run(order=2)
    def test_view_student_comment_page_success(self, student_login, page):
        session, headers, csrf_token_form_data = student_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        data = f'page={page}'
        response = session.get(url=f'{host}/student-comment/', data=data, headers=headers)
        assert response.status_code == 200

    @pytest.mark.run(order=4)
    def test_view_student_password_reset(self, student_login, student_login_account):
        session, headers, csrf_token_form_data = student_login
        email, password = student_login_account
        sql_statement = f''' select id,password from rmc_student where email = "{email}" '''
        student_user_id_password = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        if student_user_id_password:
            student_user_id = student_user_id_password.get('id')
            old_encry_password = student_user_id_password.get('password')
            new_password = password + '1'
            data = f'{csrf_token_form_data}&password={new_password}&confirm_password={new_password}'
            response = session.post(url=f'{host}/{student_user_id}/student-reset/', data=data, headers=headers)
            sql_statement = f''' select password from rmc_student where id = {student_user_id} '''
            new_encry_password = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True).get('password')
            assert response.status_code == 200
            assert md5(data_string=password) == old_encry_password
            assert md5(data_string=new_password) != old_encry_password
            assert new_encry_password != old_encry_password
            data = f'{csrf_token_form_data}&password={password}&confirm_password={password}'
            response = session.post(url=f'{host}/{student_user_id}/student-reset/', data=data, headers=headers)
            sql_statement = f''' select password from rmc_student where id = {student_user_id} '''
            reset_encry_password = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True).get(
                'password')
            assert response.status_code == 200
            assert md5(data_string=password) == reset_encry_password
            assert md5(data_string=new_password) != reset_encry_password

    @pytest.mark.run(order=5)
    def test_view_student_log_out(self, staff_login):
        session, headers, csrf_token_form_data = staff_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.get(url=f'{host}/logout/', data=None, headers=headers)
        assert response.status_code == 200
        assert_list = ["staff-login", 'Login']
        assert all([i in response.text for i in assert_list])


class TestCaseStaffView(object):
    '''Test Manager view'''

    @pytest.mark.run(order=1)
    def test_view_data_visualisation_gender_distribution_socs_success(self, staff_login):
        session, headers, csrf_token_form_data = staff_login
        response = session.get(url=f'{host}/data-visualisation/gender-distribution-socs/', data=None, headers=headers)
        assert response.status_code == 200
        assert_list = ["Male", "Female"]
        assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=2)
    def test_view_data_visualisation_degree_programme_enrolment_success(self, staff_login):
        session, headers, csrf_token_form_data = staff_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.get(url=f'{host}/data-visualisation/degree-programme-enrolment/', data=None, headers=headers)
        assert response.status_code == 200
        assert_list = ["Computing Science MSc", "Data Science MSc",
                       "Information Technology MSc", "Software Development MSc"]
        assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('page', [1, 2, -1, ''])
    def test_view_course_management_page_success(self, staff_login, page):
        session, headers, csrf_token_form_data = staff_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        data = f'page={page}'
        response = session.get(url=f'{host}/course-management/', data=data, headers=headers)
        assert response.status_code == 200
        assert_list = ["Course list", "All courses are listed as follows:",
                       "Course name", "Associated degree programmes"]
        assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('course_name,associated_degree_programmes',
                             (['test1', 1], ['test2', 2], ['test3', 3], ['test4', 4]))
    def test_view_course_add_success(self, staff_login, course_name, associated_degree_programmes):
        session, headers, csrf_token_form_data = staff_login
        data = f'{csrf_token_form_data}&name={course_name}&associated_degree_programmes={associated_degree_programmes}'
        response = session.post(url=f'{host}/course-add/', data=data, headers=headers)
        assert response.status_code == 200
        assert_list = [course_name]
        assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=5)
    @pytest.mark.parametrize('course_name,associated_degree_programmes',
                             (['test1', 1], ['test2', 2], ['test3', 3], ['test4', 4]))
    def test_view_course_edit_success(self, staff_login, course_name, associated_degree_programmes):
        session, headers, csrf_token_form_data = staff_login
        new_course_name = course_name + '_new'
        sql_statement = f'select id from rmc_course where name in ("{course_name}","{new_course_name}") '
        course_id = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        if course_id:
            course_id = course_id.get('id')
            data = f'{csrf_token_form_data}&name={new_course_name}&' \
                   f'associated_degree_programmes={associated_degree_programmes}'
            response = session.post(url=f'{host}/{course_id}/course-edit/', data=data, headers=headers)
            assert response.status_code == 200
            assert_list = [new_course_name]
            assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=6)
    @pytest.mark.parametrize('course_name', ['test1', 'test2', 'test3', 'test4'])
    def test_view_course_delete_success(self, staff_login, course_name):
        session, headers, csrf_token_form_data = staff_login
        new_course_name = course_name + '_new'
        sql_statement = f'select id from rmc_course where name in ("{course_name}","{new_course_name}") '
        course_id = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        if course_id:
            course_id = course_id.get('id')
            response = session.get(url=f'{host}/{course_id}/course-delete/', data=None, headers=headers)
            assert response.status_code == 200
            assert_list = [new_course_name]
            assert all([i not in response.text for i in assert_list])

    @pytest.mark.run(order=7)
    def test_view_course_list_success(self, staff_login):
        session, headers, csrf_token_form_data = staff_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.get(url=f'{host}/course-list/', data=None, headers=headers)
        assert response.status_code == 200
        assert_list = ["All courses with review(s) are listed as follows:",
                       "Course name"]
        assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=8)
    @pytest.mark.parametrize('course_name',
                             ['Programming and Systems Development',
                              'Introduction to Data Science and Systems'
                              'Enterprise Cyber Security',
                              'Machine Learning & Artificial Intelligence for Data Scientists'])
    @pytest.mark.parametrize('page', [-1, 1, 20])
    def test_view_view_reviews_course_success(self, staff_login, course_name, page):
        session, headers, csrf_token_form_data = staff_login
        new_course_name = course_name + '_new'
        sql_statement = f'select id from rmc_course where name in ("{course_name}","{new_course_name}") '
        course_id = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        if course_id:
            course_id = course_id.get('id')
            data = f"page={page}"
            response = session.get(url=f'{host}/{course_id}/view-reviews-course/', data=data, headers=headers)
            assert response.status_code == 200
            html_encode_course_name = out_html_text(course_name)
            assert_list = [f"All reviews of {html_encode_course_name} are listed below:",
                           "Student name", "Overall score", "Easiness score", "Interest score",
                           "Usefulness score", "Teaching score", "Comment"]
            assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=9)
    def test_view_student_list_success(self, staff_login):
        session, headers, csrf_token_form_data = staff_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.get(url=f'{host}/student-list/', data=None, headers=headers)
        assert response.status_code == 200
        assert_list = ["All students who have made course reviews are listed as follows:",
                       "ID", "Email", "Student name", "Gender", "Age", "Entry year", "Degree programme", "Actions"]
        assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=10)
    @pytest.mark.parametrize('student_name',
                             ['Ruijun Jiang', 'John Smith', 'Jane Smith'])
    @pytest.mark.parametrize('page', [-1, 1, 20])
    def test_view_view_reviews_student_page_success(self, staff_login, student_name, page):
        session, headers, csrf_token_form_data = staff_login
        new_student_name = student_name + '_new'
        sql_statement = f'select id from rmc_student where name in ("{student_name}","{new_student_name}") '
        course_id = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        data = f'page={page}'
        if course_id:
            course_id = course_id.get('id')
            response = session.get(url=f'{host}/{course_id}/view-reviews-student/', data=data, headers=headers)
            assert response.status_code == 200
            html_encode_student_name = out_html_text(student_name)
            assert_list = [f"All reviews done by {html_encode_student_name} are listed below:",
                           "Course name", "Overall score", "Easiness score", "Interest score",
                           "Usefulness score", "Teaching score", "Comment"]
            assert all([i in response.text for i in assert_list])

    @pytest.mark.run(order=11)
    @pytest.mark.parametrize('student_name',
                             ['James Watt', 'James Bond'])
    def test_view_view_reviews_student_failed(self, staff_login, student_name):
        session, headers, csrf_token_form_data = staff_login
        new_student_name = student_name + '_new'
        sql_statement = f'select id from rmc_student where name in ("{student_name}","{new_student_name}") '
        course_id = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        if course_id:
            course_id = course_id.get('id')
            response = session.get(url=f'{host}/{course_id}/view-reviews-student/', data=None, headers=headers)
            html_encode_student_name = out_html_text(student_name)
            assert response.status_code == 500
            assert_list = [f"All reviews done by {html_encode_student_name} are listed below:",
                           "Course name", "Overall score", "Easiness score", "Interest score",
                           "Usefulness score", "Teaching score", "Comment"]
            assert all([i not in response.text for i in assert_list])

    @pytest.mark.run(order=12)
    def test_view_staff_password_reset(self, staff_login, staff_login_account):
        session, headers, csrf_token_form_data = staff_login
        email, password = staff_login_account
        sql_statement = f''' select id,password from rmc_staff where email = "{email}" '''
        staff_user_id_password = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True)
        if staff_user_id_password:
            staff_user_id = staff_user_id_password.get('id')
            old_encry_password = staff_user_id_password.get('password')
            new_password = password + '1'
            data = f'{csrf_token_form_data}&password={new_password}&confirm_password={new_password}'
            response = session.post(url=f'{host}/{staff_user_id}/staff-reset/', data=data, headers=headers)
            sql_statement = f''' select password from rmc_staff where id = {staff_user_id} '''
            new_encry_password = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True).get('password')
            assert response.status_code == 200
            assert md5(data_string=password) == old_encry_password
            assert md5(data_string=new_password) != old_encry_password
            assert new_encry_password != old_encry_password
            data = f'{csrf_token_form_data}&password={password}&confirm_password={password}'
            response = session.post(url=f'{host}/{staff_user_id}/staff-reset/', data=data, headers=headers)
            sql_statement = f''' select password from rmc_staff where id = {staff_user_id} '''
            reset_encry_password = customer_sqllite_operation(sql_statement=sql_statement, limit_one=True).get(
                'password')
            assert response.status_code == 200
            assert md5(data_string=password) == reset_encry_password
            assert md5(data_string=new_password) != reset_encry_password

    @pytest.mark.run(order=13)
    def test_view_staff_log_out(self, staff_login):
        session, headers, csrf_token_form_data = staff_login
        # data = f'{csrf_token_form_data}&age={age}&name={name}&gender={gender}'
        response = session.get(url=f'{host}/staff-logout/', data=None, headers=headers)
        assert response.status_code == 200
        assert_list = ["student-login", 'Staff Login', 'Login']
        assert all([i in response.text for i in assert_list])
