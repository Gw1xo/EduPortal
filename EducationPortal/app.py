from flask import Flask, render_template, url_for, redirect, request, flash, session
from admin.admin import admin_bp
from teacher.teacher import teacher_bp
from student.student import student_bp
from init_db import OperatorDB
from forms import LoginForm, RegisterForm
from flask_wtf.csrf import CSRFProtect
from AdditionalScript import generate_unique_key

app = Flask(__name__)
app.config['SECRET_KEY'] = "asjdjasdkjdngvjwpoefkjmadc"
csrf = CSRFProtect(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    session.clear()
    login_form = LoginForm()

    if login_form.validate_on_submit():
        login = login_form.login.data
        password = login_form.password.data
        uniq_school_code = login_form.uniq_school_code.data

        try:
            with OperatorDB() as op:
                op.cur.execute(f"select school.shcoolid from school where uniq_code = '{uniq_school_code}'")
                school = op.cur.fetchone()
                if not school:
                    raise Exception("Невірний код школи")
                op.cur.execute(f"select * from users where (scoolid = {school[0]}) and (login = '{login}')")
                user = op.cur.fetchone()
                if not user:
                    raise Exception("Невірний логін")
                if user[3] != password:
                    raise Exception("Невірний пароль")

                session['userid'] = user[0]
                session['userrole'] = user[-2]
                session['uniqcode'] = uniq_school_code
                session['schoolid'] = school[0]

                match user[-2]:
                    case 1:
                        return redirect("/adm")
                    case 2:
                        return redirect("/tch")
                    case 3:
                        return redirect("/std")

        except Exception as e:
            flash(f"{e.__str__()}")
    return render_template('index.html', form=login_form)


@app.route("/reg", methods=['GET', 'POST'])
def registration():
    session.clear()
    form = RegisterForm()
    if request.method != 'POST':
        return render_template("registration.html", form=form)

    if form.validate_on_submit():
        if form.password.data == form.conf_password.data:
            email = form.email.data
            name_school = form.name_school.data
            address_school = form.address_school.data
            login = form.login.data
            password = form.password.data
            conf_password = form.conf_password.data

            unq_code = generate_unique_key()

            with OperatorDB() as op:
                op.cur.execute(
                    f"insert into school(name, uniq_code, address) "
                    f"VALUES ('{name_school}','{unq_code}','{address_school}');"
                )
                op.cur.execute(
                    f"select school.shcoolid, school.uniq_code from school where uniq_code = '{unq_code}'"
                )

                school_id = op.cur.fetchone()

                op.cur.execute('insert into users(email, login, psw, edu_role, scoolid) '
                               f"VALUES ('{email}','{login}','{password}',1,{school_id[0]})")

                op.cur.execute(f"select users.userid from users where scoolid = {school_id[0]} and login = '{login}'")
                user_id = op.cur.fetchone()

                session['userid'] = user_id[0]
                session['schoolid'] = school_id[0]
                session['uniqcode'] = school_id[1]

                return redirect('/adm')
        else:
            return render_template("registration.html", form=form)


# Реєстрація Blueprint
app.register_blueprint(admin_bp, url_prefix="/adm")
app.register_blueprint(teacher_bp, url_prefix="/tch")
app.register_blueprint(student_bp, url_prefix="/std")

if __name__ == "__main__":
    app.debug = True
    app.host = "0.0.0.0"
    app.run()
