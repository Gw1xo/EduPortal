from flask import Blueprint, render_template, session, url_for, flash
from forms import CourseForm
from AdditionalScript import check_access
from init_db import OperatorDB

teacher_bp = Blueprint("teacher", __name__, template_folder='templates', static_folder='static')


urls = {
    "home": "/",
    "courses": "/courses",
    "lessons": "/courses/lesson"
}

# session['userid'] = user[0]
# session['userrole'] = user[-2]
# session['uniqcode'] = uniq_school_code
# session['schoolid'] = school[0]


@teacher_bp.route(urls['home'])
@check_access(userrole=2)
def teacher_home():
    userid = session.get('userid')
    with OperatorDB() as op:
        op.cur.execute(f'select * from teachers where userid = {userid}')
        teacher = op.cur.fetchone()
    return render_template("teacher/teacher_home.html", teacher=teacher)


@teacher_bp.route(urls["courses"])
@check_access(userrole=2)
def teacher_courses():
    user_id = session.get('userid')
    school_id = session.get('schoolid')
    teacher_id = 0

    classes = []
    subjects = []
    courses = []

    with OperatorDB() as op:
        op.cur.execute(f'select teachers.teacherid from teachers where userid = {user_id}')
        teacher_id = op.cur.fetchone()[0]
        op.cur.execute(f'select * from courses where scoolid = {school_id} and teacherid = {teacher_id}')
        courses = op.cur.fetchall()
        op.cur.execute(f'select * from class where scoolid = {school_id}')
        classes = op.cur.fetchall()
        op.cur.execute(f'select * from subjects where scoolid = {school_id}')

    form = CourseForm(classes, subjects)

    if form.validate_on_submit():
        name_course = form.name_course.data
        class_name = form.class_name.data
        subject = form.subject.data

        with OperatorDB() as op:
            op.cur.execute(f"select class.classid from class where class_name = '{class_name}'")
            class_id = op.cur.fetchone()[0]
            op.cur.execute(f"select subjects.subjectid from subjects where name_sub = '{subject}'")
            subject_id = op.cur.fetchone()[0]

            op.cur.execute('insert into courses(name_course, classid, subjectid, teacherid, scoolid) '
                           f"VALUES('{name_course}', {class_id}, {subject_id}, {teacher_id}, {school_id})")
            flash('Курс успішно створено')

    return render_template("teacher_courses.html", courses=courses, form=form)



@teacher_bp.route(urls["lessons"])
@check_access(userrole=1)
def teacher_lessons():
    return render_template("teacher_lessons.html")
