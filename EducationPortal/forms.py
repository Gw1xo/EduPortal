from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField, BooleanField, EmailField, SelectField, \
    DateField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired


class CsrfToken(FlaskForm):
    csrf_token = HiddenField()


class LoginForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    login = StringField('Login:', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password:', validators=[DataRequired()])
    uniq_school_code = PasswordField('Shcool code:', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    email = EmailField("Email:", validators=[DataRequired()])
    login = StringField('Login:', validators=[DataRequired(), Length(min=2, max=20)])
    name_school = StringField("School`s name:", validators=[DataRequired()])
    address_school = StringField("School`s address:", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class ClassForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    class_name = StringField("Class number:", validators=[DataRequired()])
    submit = SubmitField('Create class')


class StudentForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token

    def __init__(self, class_list):
        super().__init__()
        self.class_name.choices = class_list

    firstname = StringField("Firstname:", validators=[DataRequired()])
    lastname = StringField("Lastname:", validators=[DataRequired()])
    patronymic = StringField("Patronymic:", validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    phone_number = StringField('Phone number:', validators=[DataRequired(), Length(min=10, max=10)])
    home_address = StringField('Home address:', validators=[DataRequired()])
    birth_certificate = StringField('Birth certificate number:', validators=[DataRequired()])
    parent1_firstname = StringField("Parent 1 firstname:", validators=[DataRequired()])
    parent1_laststname = StringField("Parent 1 lastname:", validators=[DataRequired()])
    parent1_patronymic = StringField("Parent 1 patronymic:", validators=[DataRequired()])
    parent1_phone_number = StringField("Parent 1 phone number:", validators=[DataRequired(), Length(min=10, max=10)])
    parent1_email = EmailField("Parent 1 email:", validators=[DataRequired()])
    parent2_firstname = StringField("Parent 2 firstname:", validators=[DataRequired()])
    parent2_laststname = StringField("Parent 2 lastname:", validators=[DataRequired()])
    parent2_patronymic = StringField("Parent 2 patronymic:", validators=[DataRequired()])
    parent2_phone_number = StringField("Parent 2 phone number:", validators=[DataRequired(), Length(min=10, max=10)])
    parent2_email = EmailField("Parent 2 email:", validators=[DataRequired()])
    class_name = SelectField("Class:", validators=[DataRequired()])
    submit = SubmitField('Add student')


class TeacherForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    firstname = StringField("Firstname:", validators=[DataRequired()])
    lastname = StringField("Lastname:", validators=[DataRequired()])
    patronymic = StringField("Patronymic:", validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    phone_number = StringField('Phone number:', validators=[DataRequired(), Length(min=10, max=10)])
    home_address = StringField('Home address:', validators=[DataRequired()])
    psp_number = StringField('Passport number:', validators=[DataRequired()])
    education_level = StringField("Education level:", validators=[DataRequired()])
    additional_qualification = StringField("Additional qualification:", validators=[DataRequired()])
    experience_age = StringField('Age of experience', validators=[DataRequired()])
    submit = SubmitField('Add teacher')


class SubjectForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    name = StringField('Subject name:', validators=[DataRequired()])
    submit = SubmitField('Add subject')


class ScheduleForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    class_name = StringField("Class:", validators=[DataRequired()])
    subject_name = StringField("Subject:", validators=[DataRequired()])
    teacher_id = StringField("Teacher:", validators=[DataRequired()])
    day = SelectField('Day', choices=[('mon', 'Mon'), ('tue', 'Tue'), ('wed', 'Wed'), ('thu', 'Thu'), ('fri', 'Fri'),
                                      ('sat', 'Sat')], validators=[InputRequired()])


class CourseForm(FlaskForm):
    csrf_token = CsrfToken.csrf_token
    name_course = StringField('Course name', validators=[DataRequired()])
    class_name = SelectField("Class:", validators=[DataRequired()])
    subject = SelectField("Subject:", validators=[DataRequired()])

    def __init__(self, classes, subjects):
        super().__init__()
        self.class_name.choices = classes
        self.subject.choices = subjects
