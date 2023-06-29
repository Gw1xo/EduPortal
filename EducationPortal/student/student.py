from flask import Blueprint, render_template

student_bp = Blueprint("student", __name__, template_folder='templates', static_folder='static')


@student_bp.route("/")
def student_home():
    return render_template("student_home.html")


@student_bp.route("/curses")
def student_courses():
    return render_template("student_courses.html")


@student_bp.route("/curses/lessons")
def student_lessons():
    return render_template("student_lessons.html")


@student_bp.route("/curses/grades")
def student_grades():
    return render_template("student_grades.html")


@student_bp.route("/schedule")
def student_schedule():
    return render_template("student_schedule.html")
