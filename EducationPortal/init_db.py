import env
import psycopg2


class OperatorDB:

    def __create_table_School(self):
        self.cur.execute('create table School (shcoolid serial primary key,'
                         'name varchar(50) not null ,'
                         'uniq_code varchar(10) not null,'
                         'address varchar(50) not null )'
                         )

    def __create_table_Users(self):
        self.cur.execute('create table Users (userid serial primary key,'
                         'email varchar(50) not null ,'
                         'login varchar(50) not null,'
                         'psw varchar(50) not null ,'
                         'edu_role int not null ,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)')

    def __create_table_Class(self):
        self.cur.execute('create table Class (classid serial primary key,'
                         'class_name varchar(50) not null,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_EduAdmin(self):
        self.cur.execute('create table EduAdmin(eduadminid serial primary key,'
                         'userid int unique,'
                         'foreign key (userid) references Users(userid) on delete cascade'
                         ','
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)')

    def __create_table_Students(self):
        self.cur.execute('create table Students (studentid serial primary key,'
                         'userid int unique,'
                         'classid int,'
                         'foreign key (userid) references Users (userid) on delete cascade,'
                         'firstname varchar(50) not null,'
                         'lastname varchar(50) not null ,'
                         'patronymic varchar(50) not null,'
                         'gender varchar(6) not null ,'
                         'phone_number varchar(10) null ,'
                         'home_address varchar(100) not null,'
                         'birth_certificate_number varchar(16) not null ,'
                         'parent1_firstname varchar(50) not null,'
                         'parent1_lastname varchar(50) not null,'
                         'parent1_patronymic varchar(50) not null,'
                         'parent1_email varchar(50) null,'
                         'parent1_phone_number varchar(10) not null,'
                         'parent2_firstname varchar(50) null,'
                         'parent2_lastname varchar(50) null,'
                         'parent2_patronymic varchar(50) null,'
                         'parent2_email varchar(50) null,'
                         'parent2_phone_number varchar(10) null,'
                         'foreign key (classid) references Class (classid) on delete cascade,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Teachers(self):
        self.cur.execute('create table Teachers (teacherid serial primary key,'
                         'userid int unique,'
                         'foreign key (userid) references Users (userid) on delete cascade,'
                         'firstname varchar(50) not null,'
                         'lastname varchar(50) not null ,'
                         'patronymic varchar(50) not null,'
                         'gender varchar(6) not null ,'
                         'phone_number varchar(10) null ,'
                         'psw_number varchar(16) not null ,'
                         'home_address varchar(100) not null,'
                         'education_level varchar(50) not null,'
                         'additional_qualification varchar(100) not null,'
                         'experience_age int not null,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Subjects(self):
        self.cur.execute('create table Subjects (subjectid serial primary key,'
                         'name_sub varchar(50) not null,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Courses(self):
        self.cur.execute('create table Courses (courseid serial primary key,'
                         'name_course varchar(50) not null,'
                         'classid int ,'
                         'subjectid int ,'
                         'teacherid int ,'
                         'foreign key (classid) references Class (classid) on delete cascade,'
                         'foreign key (subjectid) references Subjects (subjectid) on delete cascade,'
                         'foreign key (teacherid) references Teachers (teacherid) on delete cascade,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Lessons(self):
        self.cur.execute('create table Lessons (lessonid serial primary key,'
                         'courseid int unique,'
                         'topic varchar(50) not null,'
                         'task varchar(1000) not null,'
                         'material varchar(100) not null,'
                         'date date not null,'
                         'start_time time not null ,'
                         'end_time time not null ,'
                         'foreign key (courseid) references Courses (courseid) on delete cascade,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Grades(self):
        self.cur.execute('create table Grades (gradeid serial primary key,'
                         'courseid int ,'
                         'lessonid int ,'
                         'studentid int ,'
                         'foreign key (courseid) references Courses (courseid) on delete cascade,'
                         'foreign key (lessonid) references Lessons (lessonid) on delete cascade,'
                         'foreign key (studentid) references Students (studentid) on delete cascade,'
                         'grade int not null,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Answers(self):
        self.cur.execute('create table Answers (answerid serial primary key,'
                         'lessonid int ,'
                         'studentid int ,'
                         'foreign key (lessonid) references Lessons (lessonid) on delete cascade,'
                         'foreign key (studentid) references Students (studentid) on delete cascade,'
                         'answer text null,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)')

    def __create_table_ScheduleSubjs(self):
        self.cur.execute('create table ScheduleSubjs(schedulesubjid serial primary key,'
                         'classid int ,'
                         'subjectid int ,'
                         'teacherid int ,'
                         'foreign key (classid) references Class (classid) on delete cascade,'
                         'foreign key (subjectid) references Subjects (subjectid) on delete cascade,'
                         'foreign key (teacherid) references Teachers (teacherid) on delete cascade,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)'
                         )

    def __create_table_Schedule(self):
        self.cur.execute('create table Schedule(scheduleid serial primary key,'
                         'schedulesubjid int ,'
                         'foreign key (schedulesubjid) references ScheduleSubjs (schedulesubjid) on delete cascade,'
                         'day varchar(3) not null,'
                         'week int not null,'
                         'num int not null,'
                         'scoolid int not null,'
                         'foreign key (scoolid) references School (shcoolid) on delete cascade)')

    def __delete_table(self, name):
        self.cur.execute(f'DROP TABLE IF EXISTS {name};')

    def create_tables(self):
        self.__create_table_School()
        self.__create_table_Users()
        self.__create_table_EduAdmin()
        self.__create_table_Class()
        self.__create_table_Students()
        self.__create_table_Teachers()
        self.__create_table_Subjects()
        self.__create_table_Courses()
        self.__create_table_Lessons()
        self.__create_table_Answers()
        self.__create_table_Grades()
        self.__create_table_ScheduleSubjs()
        self.__create_table_Schedule()

    def drop_all_tables(self):
        self.__delete_table('Schedule')
        self.__delete_table('ScheduleSubjs')
        self.__delete_table('Grades')
        self.__delete_table('Answers')
        self.__delete_table('Lessons')
        self.__delete_table('Courses')
        self.__delete_table('Subjects')
        self.__delete_table('Teachers')
        self.__delete_table('students')
        self.__delete_table('class')
        self.__delete_table('EduAdmin')
        self.__delete_table('users')
        self.__delete_table('school')

    def __enter__(self):
        self.connection = psycopg2.connect(host=env.HOST,
                                           database=env.DATABASE,
                                           user=env.DB_USERNAME,
                                           password=env.DB_PASSWORD)

        self.cur = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cur.close()
        self.connection.close()


if __name__ == "__main__":
    with OperatorDB() as db:
        db.cur.execute("select students.userid from students where studentid = 1")
        print(db.cur.fetchone())





