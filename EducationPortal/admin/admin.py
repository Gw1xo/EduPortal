from flask import Blueprint, render_template, session, abort, redirect, flash, request, url_for
from init_db import OperatorDB
from AdditionalScript import check_access, generate_unique_key, get_user
from forms import ClassForm, StudentForm, CsrfToken, TeacherForm, SubjectForm
from functools import wraps

admin_bp = Blueprint("admin", __name__, template_folder='templates', static_folder='static')

urls = {
    "home": "/",
    "student": "/student",
    "student_add": "/student/add",
    "student_del": "/student/del",
    "student_info": "/student/info",
    "teacher": "/teacher",
    "teacher_add": "/teacher/add",
    "teacher_del": "/teacher/del",
    "teacher_info": "/teacher/info",
    "subject": "/subject",
    "subject_del": "/subject/del",
    "class": "/class",
    "class_del": "/class/del",
    "class_info": "/class/info",
    "schedule": "schedule"
}

# session['userid'] = user[0]
# session['userrole'] = user[-2]
# session['uniqcode'] = uniq_school_code
# session['schoolid'] = school[0]


@admin_bp.route(urls["home"])
@check_access(userrole=1)
def admin_home():
    school_uniq = session.get("uniqcode")
    school_name = ''
    with OperatorDB() as op:
        op.cur.execute(f"select school.name from school where uniq_code = '{school_uniq}'")
        school_name = op.cur.fetchone()[0]
    return render_template("admin/admin_home.html", uniq=school_uniq, name=school_name)


@admin_bp.route(urls["student"])
@check_access(userrole=1)
def admin_students():
    school_id = session.get("schoolid")
    students = []
    users = []
    form = CsrfToken()
    with OperatorDB() as op:
        op.cur.execute(f'select * from students where scoolid = {school_id}')
        students = op.cur.fetchall()
        users = [student[1] for student in students]

    return render_template("admin/admin_students.html", students=students, users=users, get_user=get_user, form=form)


@admin_bp.route(urls["student_del"], methods=['POST'])
@check_access(userrole=1)
def students_delete():
    student_id = request.form.get('student_id')
    with OperatorDB() as op:
        op.cur.execute(f"select students.userid from students where studentid = {student_id}")
        user_id = op.cur.fetchone()[0]

        op.cur.execute(f"delete from students where studentid = {student_id}")
        op.cur.execute(f"delete from users where userid = {user_id}")
    return redirect(url_for('admin.admin_students'))


@admin_bp.route(urls["student_info"], methods=['POST'])
@check_access(userrole=1)
def students_info():
    student_id = request.form.get('student_id')
    with OperatorDB() as op:
        op.cur.execute(f"select * from students where studentid = {student_id}")
        student = op.cur.fetchone()

        op.cur.execute(f"select * from users where userid = {student[1]}")
        user = op.cur.fetchone()

        op.cur.execute(f"select * from class where classid = {student[2]}")
        student_class = op.cur.fetchone()
        return render_template("admin/admin_student_info.html", student=student, user=user, student_class=student_class)


@admin_bp.route(urls["student_add"], methods=['POST', 'GET'])
@check_access(userrole=1)
def admin_students_add():
    school_id = session.get("schoolid")
    school_uniq = session.get("uniqcode")
    class_list = []
    with OperatorDB() as op:
        op.cur.execute(f"select * from class where scoolid = '{school_id}'")
        classes = op.cur.fetchall()
        for cl in classes:
            class_list.append((cl[1], cl[1]))
    print(class_list)
    form = StudentForm(class_list)
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        patronymic = form.patronymic.data
        phone_number = form.phone_number.data
        gender = form.gender.data
        home_address = form.home_address.data
        birth_certificate = form.birth_certificate.data
        parents = [{
            "firstname": form.parent1_firstname.data,
            "lastname": form.parent1_laststname.data,
            "patronymic": form.parent1_patronymic.data,
            "email": form.parent1_email.data,
            "phone_number": form.parent1_phone_number.data
        }, {
            "firstname": form.parent2_firstname.data,
            "lastname": form.parent2_laststname.data,
            "patronymic": form.parent2_patronymic.data,
            "email": form.parent2_email.data,
            "phone_number": form.parent2_phone_number.data
        }]
        class_name = form.class_name.data

        login = generate_unique_key() + "_" + school_uniq
        password = generate_unique_key()
        email = login + "@student.edu.ua"

        with OperatorDB() as op:
            op.cur.execute('insert into users(email, login, psw, edu_role, scoolid) '
                           f"VALUES ('{email}','{login}','{password}',3,{school_id})")
            op.cur.execute(f"select users.userid from users where login = '{login}'")
            userid = op.cur.fetchone()[0]

            op.cur.execute(f"select class.classid from class where class_name = '{class_name}'")
            class_id = op.cur.fetchone()[0]
            if class_id is not None:
                op.cur.execute('insert into students(userid, classid, firstname, lastname, patronymic, gender, '
                               'phone_number, home_address, birth_certificate_number, parent1_firstname, '
                               'parent1_lastname, parent1_patronymic, parent1_email, parent1_phone_number,'
                               ' parent2_firstname, parent2_lastname, parent2_patronymic, parent2_email,'
                               ' parent2_phone_number, scoolid) '
                               f"values ({userid}, {class_id}, '{firstname}', '{lastname}', '{patronymic}', '{gender}',"
                               f"'{phone_number}','{home_address}', '{birth_certificate}', '{parents[0]['firstname']}',"
                               f"'{parents[0]['lastname']}', '{parents[0]['patronymic']}', '{parents[0]['email']}', "
                               f"'{parents[0]['phone_number']}','{parents[1]['firstname']}','{parents[1]['lastname']}',"
                               f" '{parents[1]['patronymic']}','{parents[1]['email']}', '{parents[1]['phone_number']}',"
                               f" {school_id})")
                flash(f'Учень успішно зарахований до класу {class_name}')
            else:
                flash(f'Класу не існує')

    return render_template("admin/admin_students_add.html", form=form)


@admin_bp.route(urls["teacher"])
@check_access(userrole=1)
def admin_teachers():
    school_id = session.get('schoolid')
    students = []
    users = []
    form = CsrfToken()
    with OperatorDB() as op:
        op.cur.execute(f'select * from teachers where scoolid = {school_id}')
        teachers = op.cur.fetchall()
        users = [teacher[1] for teacher in teachers]

    return render_template("admin/admin_teachers.html", teachers=teachers, users=users, get_user=get_user, form=form)


@admin_bp.route(urls["teacher_add"], methods=['post', 'get'])
@check_access(userrole=1)
def admin_teacher_add():
    form = TeacherForm()
    school_id = session.get("schoolid")
    school_uniq = session.get("uniqcode")
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        patronymic = form.patronymic.data
        gender = form.gender.data
        phone_number = form.phone_number.data
        psp_number = form.psp_number.data
        home_address = form.home_address.data
        education_level = form.education_level.data
        additional_qualification = form.additional_qualification.data
        experience_age = form.experience_age.data

        login = generate_unique_key() + "_" + school_uniq
        password = generate_unique_key()
        email = login + "@teacher.edu.ua"

        with OperatorDB() as op:
            op.cur.execute('insert into users(email, login, psw, edu_role, scoolid) '
                           f"VALUES ('{email}','{login}','{password}',2,{school_id})")
            op.cur.execute(f"select users.userid from users where login = '{login}'")
            userid = op.cur.fetchone()[0]

            op.cur.execute('insert into teachers(userid, firstname, lastname, patronymic, gender, phone_number,'
                           ' psw_number, home_address, education_level, additional_qualification, '
                           'experience_age, scoolid)'
                           f"values ({userid}, '{firstname}', '{lastname}', '{patronymic}','{gender}','{phone_number}',"
                           f"'{psp_number}','{home_address}', '{education_level}', '{additional_qualification}',"
                           f"{experience_age},{school_id})")
            flash(f'Вчитель успішно прийнятий до навчального закладу')

    return render_template('admin/admin_add_teacher.html', form=form)


@admin_bp.route(urls["teacher_del"], methods=['POST'])
@check_access(userrole=1)
def teacher_delete():
    teacher_id = request.form.get('teacher_id')
    with OperatorDB() as op:
        op.cur.execute(f"select teachers.userid from teachers where teacherid = {teacher_id}")
        user_id = op.cur.fetchone()[0]

        op.cur.execute(f"delete from teachers where teacherid = {teacher_id}")
        op.cur.execute(f"delete from users where userid = {user_id}")
    return redirect(url_for('admin.admin_teachers'))


@admin_bp.route(urls["teacher_info"], methods=['POST'])
@check_access(userrole=1)
def teacher_info():
    teacher_id = request.form.get('teacher_id')
    with OperatorDB() as op:
        op.cur.execute(f"select * from teachers where teacherid = {teacher_id}")
        teacher = op.cur.fetchone()

        op.cur.execute(f"select * from users where userid = {teacher[1]}")
        user = op.cur.fetchone()

        return render_template("admin/admin_teacher_info.html", teacher=teacher, user=user)


@admin_bp.route(urls["subject"], methods=['post', 'get'])
@check_access(userrole=1)
def admin_subjects():
    school_id = session.get('schoolid')
    subjects = []
    with OperatorDB() as op:
        op.cur.execute(f'select * from subjects where scoolid = {school_id}')
        subjects = op.cur.fetchall()
    form = SubjectForm()
    if form.validate_on_submit():
        subject_name = form.name.data
        with OperatorDB() as op:
            op.cur.execute(f"insert into subjects(name_sub, scoolid) VALUES ('{subject_name}', {school_id})")
        return redirect(url_for('admin.admin_subjects'))
    return render_template("admin/admin_subjects.html", form=form, subjects=subjects)


@admin_bp.route(urls["subject_del"], methods=['post'])
@check_access(userrole=1)
def admin_subject_del():
    subject_id = request.form.get('subject_id')
    with OperatorDB() as op:
        op.cur.execute(f'select * from schedulesubjs where subjectid = {subject_id}')
        if len(op.cur.fetchall()) == 0:
            op.cur.execute(f"delete from subjects where subjectid = {subject_id}")
        else:
            flash('Предмет є в розкладі')
    return redirect(url_for('admin.admin_subjects'))


@admin_bp.route(urls["class"], methods=['POST', 'GET'])
@check_access(userrole=1)
def admin_class():
    school_id = session.get('schoolid')
    all_classes = []
    with OperatorDB() as op:
        op.cur.execute(f'select * from class where scoolid = {school_id}')
        all_classes = op.cur.fetchall()

    form = ClassForm()
    if form.validate_on_submit():
        name = form.class_name.data

        with OperatorDB() as op:
            op.cur.execute(f"insert into class(class_name, scoolid) VALUES ('{name}',{school_id})")

        return render_template("admin/admin_add_class_succesful.html")

    return render_template("admin/admin_class.html", classes=all_classes, form=form)


@admin_bp.route(urls["class_del"], methods=['post'])
@check_access(userrole=1)
def admin_class_del():
    class_id = request.form.get('class_id')
    with OperatorDB() as op:
        op.cur.execute(f'select * from students where classid = {class_id}')
        if len(op.cur.fetchall()) == 0:
            op.cur.execute(f"delete from class where classid = {class_id}")
        else:
            flash('В класі є учні')
    return redirect(url_for('admin.admin_class'))


@admin_bp.route(urls["schedule"])
@check_access(userrole=1)
def admin_schedule():
    return render_template("admin/admin_schedule.html")
