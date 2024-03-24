from datetime import datetime,date
import calendar
from flask import Flask,session,request,redirect,url_for,render_template,request,jsonify
#from db_scripts import *
import os
import ast
import json
import sqlite3
conn = None

curs = None

PATH = "c:/flaskjournal/"
PATH_STATIC = os.path.join("c:/flaskjournal/" + 'static')

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://znicjqlianttbd:2b647980896c078e408c3d95511924c5fc615fca13cf23301b9a264d0a86aca0@ec2-107-21-67-46.compute-1.amazonaws.com:5432/dbmqltpol34viq'

working_days = ['Понеділок','Вівторок','Середа','Четвер',"П'ятниця"]

monday_schedule = ['Українська література', 'Алгебра', 'Зарубіжна література', 'Хімія', 'Мистецтво', 'Географія', 'Історія']
tuesday_schedule= ['Українська мова', 'Зарубіжна література', 'Трудове навчання', 'Англійська мова', 'Фізкультура', 'Правознавство',None]
wednesday_schedule = ['Інформатика', 'Інформатика', 'Геометрія', 'Хімія', 'Історія', 'Фізика', 'Виховна година']
thursday_schedule = ['Українська література', 'Алгебра', 'Біологія', 'Англійська мова', 'Фізкультура', 'Фізика', 'Історія']
friday_schedule = ['Фізика', 'Українська мова', 'Геометрія', 'Англійська', 'Біологія', 'Фізкультура', 'Основи здоров’я']

schedule = [monday_schedule,tuesday_schedule,wednesday_schedule,thursday_schedule,friday_schedule]



def open_db():
    global conn,curs
    conn = sqlite3.connect('info.db',check_same_thread=False)
    curs = conn.cursor()

def close():
    curs.close()
    conn.close()

def do(request):
    open_db()   
    curs.execute(request)
    conn.commit()

def clear():
    global all_tables
    open_db()
    for i in all_tables:
        do(f'DROP TABLE IF EXISTS {i}')


    close()


def structure_create():
    do("""CREATE TABLE IF NOT EXISTS students_log(
        id INTEGER PRIMARY KEY,
        name TEXT,
        second_name TEXT,
        login TEXT,
        password TEXT)""")
    
    do("""CREATE TABLE IF NOT EXISTS homework(
        
        date DATE,
        subject TEXT,
        description TEXT
        )""")

    
    do("""CREATE TABLE IF NOT EXISTS marks(
       student_id INTEGER,
       subject TEXT,
       mark INTEGER,
       reason TEXT,
       date DATE,
       time TEXT

    )""")
        
    

    do('''CREATE TABLE IF NOT EXISTS schedule(
       id INTEGER PRIMARY KEY,
       day TEXT,
       lesson_1 TEXT,
       lesson_2 TEXT,
       lesson_3 TEXT,
       lesson_4 TEXT,
       lesson_5 TEXT,
       lesson_6 TEXT,
       lesson_7 TEXT
    )''')
    do("""CREATE TABLE IF NOT EXISTS device_acc(
        device_id TEXT,
       log_id INTEGER)""")
    


    
    
    

def add_log_pass(name,second_name,login,password):
    open_db()
    
    curs.execute("""INSERT INTO students_log(
                name,second_name,login,password) VALUES (?,?,?,?)""",[name,second_name,login,password])
    conn.commit()
    close()

def correcting_id_order():
    open_db()
    do("""SELECT name,second_name,login,password FROM students_log ORDER BY second_name""")

    info_by = curs.fetchall()
    
    do('DROP TABLE IF EXISTS students_log')
    conn.commit()
    
    do("""CREATE TABLE IF NOT EXISTS students_log(
        id INTEGER PRIMARY KEY,
        name TEXT,
        second_name TEXT,
        login TEXT,
        password TEXT)""")

    
    

    curs.executemany("""INSERT INTO students_log(name,second_name,login,password) VALUES(?,?,?,?)""",info_by)


    conn.commit()

def add_mark(id,subj,mark,reason,date,time):
    open_db()
    curs.execute('INSERT INTO marks(student_id,subject,mark,reason,date,time) VALUES(?,?,?,?,?,?)',[id,subj,mark,reason,date,time])
    conn.commit()
    close()
    
def get_marks(user_id):
    open_db()

    curs.execute(f'SELECT subject,mark FROM marks WHERE student_id == {user_id}')
    a = curs.fetchall()
    return a

def get_markndate(user_id):
    open_db()
    

    curs.execute(f'SELECT subject,mark,reason,date,time FROM marks WHERE student_id == {user_id}')
    
    
    a = curs.fetchall()
    
    return a




            

    


def schedule_fill():
    global working_days

    
    for i in schedule:  
        curs.executemany('INSERT INTO schedule(lesson_1,lesson_2,lesson_3,lesson_4,lesson_5,lesson_6,lesson_7) VALUES(?,?,?,?,?,?,?)',[i])
    id = curs.execute('SELECT id FROM schedule')
    id = curs.fetchall()
    for i in id:
        i = i[0]
        day = working_days[int(i)-1]
        curs.execute(f'UPDATE schedule SET day = ? WHERE id = ?',[day,i])
    conn.commit()
    
    

def get_schedule():
    open_db()
    
    info = curs.execute("SELECT day,lesson_1,lesson_2,lesson_3,lesson_4,lesson_5,lesson_6,lesson_7 FROM schedule")
    a = info.fetchall()
    
    return a
    
    


    

def get_log_pass():
    open_db()
    curs.execute('SELECT id,login,password FROM students_log')
    a = curs.fetchall() 
    
    return a

def get_names_by_id(id):
    
    open_db()
    curs.execute('SELECT name,second_name FROM students_log WHERE id = ?',[id])
    a = curs.fetchone()
    
    return a


def prepare_student_info():
    do('SELECT id,name,second_name FROM students_log')
    res = curs.fetchall()
    
    return res

def add_homework(date,subject,desc):

    open_db()
    curs.execute('INSERT INTO homework(date,subject,description) VALUES(?,?,?)',[date,subject,desc])

    conn.commit()
    close()
    
def get_homework():
    open_db()
    
    
    curs.execute('SELECT * FROM homework')
    b =curs.fetchall()
    
    return b
    

def devices_id(mode,device_id,log_id):
    open_db()
    if mode == 'ADD':
        curs.execute('SELECT device_id FROM device_acc')
        a = curs.fetchall()
        if (device_id,) in a:
            curs.execute(f'UPDATE device_acc SET log_id = ? WHERE device_id = ?',[log_id,device_id])
            conn.commit()
        if (device_id,) not in a:
            curs.execute('INSERT INTO device_acc(device_id,log_id) VALUES(?,?)',[device_id,log_id])
            conn.commit()
        close()

        
    

    if mode ==  'CHECK_DEVICE':
        curs.execute('SELECT device_id FROM device_acc')
        a = curs.fetchall()
        if (device_id,) in a:
            curs.execute('SELECT log_id FROM device_acc WHERE device_id = ?',[device_id])
            data = curs.fetchone()[0]   
            return data
            #return curs.fetchall()
        if (device_id,) not in a:
            return 'False'
        close()

@app.route('/')
def show_home():
    return 'Hello!'

@app.route('/students_log')
def students_log():
    return get_log_pass()



def schedule():
    return get_schedule()

@app.route('/schedule_day',methods = ['post','get'])
def hw_page_helper():
    global schedule_
    if request.method == 'POST':
        selected_option = request.form['option']
        curr_year = datetime.now().year

        year_previous = curr_year - 1
        year_next = curr_year +1

        curr_month =datetime.now().month

        all_dates_now = calendar.monthcalendar(curr_year,curr_month)


        prev_month = curr_month -1
        next_month = curr_month+1
        if prev_month == 0:

            prev_month = 12
            all_dates_previous = calendar.monthcalendar(year_previous,prev_month)
            all_dates_previous = [i[:5] for i in all_dates_previous][-1]
        else:
            all_dates_previous = calendar.monthcalendar(curr_year,prev_month)
            all_dates_previous = [i[:5] for i in all_dates_previous][-1]


        all_dates_now = calendar.monthcalendar(curr_year,curr_month)
        all_dates_now = [i[:5] for i in all_dates_now]
        if next_month >12:

            next_month = 1
            all_dates_next = calendar.monthcalendar(year_next,next_month)
            all_dates_next = [i[:5] for i in all_dates_next][0]
        else:
            all_dates_next = calendar.monthcalendar(curr_year,next_month)
            all_dates_next = [i[:5] for i in all_dates_next][0]

    
        days = ['Понеділок','Вівторок','Середа','Четвер',"П'ятниця"]


        days_calendar = []
        days_date = []
        c = 0

        all_days_month = []
        for a in all_dates_now:
            if a.count(0) != 5:
                all_days_month.append(days)

        for a in all_dates_now:
            if 0 in a:
                if a.count(0) != 5:
                
                    if a == all_dates_now[0]:
                        
                        b = [str(i)+'.'+ str(prev_month) for i in all_dates_previous if i != 0]
                        for i in a:
                            if i != 0:
                                b.append(i)
                        all_dates_now[0] = b

                    if a == all_dates_now[-1]:
                        
                        b = [str(i)+'.'+ str(next_month) for i in all_dates_next if i != 0]
                        for i in range(a.count(0)):
                            a.remove(0)
                        for i in b:
                            a.append(i)
                else:
                    all_dates_now.remove(a)


        for i in all_dates_now:
            try:
                int_selected_option = int(selected_option)
                if int_selected_option in i:
                    day_index = i.index(int_selected_option)
            except:
                if selected_option in i:
                    day_index = i.index(selected_option)
        
       
           
        schedule_get = schedule()[day_index][1:]
        schedule_ = [{'index': schedule_get.index(i),'text': i}for i in schedule_get]
        
       
        return jsonify(schedule_)
       
   
            
        
        


def mark_fill_page():
    all_subjects = ['Алгебра','Англійська мова','Біологія','Географія','Геометрія','Зарубіжна література','Інформатика','Історія України','Мистецтво',"Основи здоров'я",'Правознавство','Трудове навчання','Українська література','Українська мова','Фізика','Фізична культура','Хімія']

    if request.method == 'GET':
        
        list_remake= []
        list_info= prepare_student_info()   
        for info in list_info:

            list_remake.append((info[0],info[1] + ' '+info[2]))

        marks_listt = [x+1 for x in range(12)]
        


        
        return render_template('add_mark.html',student_list = list_remake,subj_list = all_subjects,marks_list=marks_listt)
    if request.method == 'POST':
        student_id = request.form.get('student')
        subject = request.form.get('subject')
        mark = request.form.get('mark')
        reason = request.form.get('reason')
        date_ = date.today()
        time = str(datetime.now()).split(' ')[1].split('.')[0].split(':')[0]+':'+ str(datetime.now()).split(' ')[1].split('.')[0].split(':')[1]

        


        subject = all_subjects[int(subject)]
    
        add_mark(student_id,subject,mark,reason,date_,time)
            
        return redirect(url_for('add_mark'))
    
def add_homework_page():
    curr_year = datetime.now().year

    year_previous = curr_year - 1
    year_next = curr_year +1

    curr_month = datetime.now().month

    all_dates_now = calendar.monthcalendar(curr_year,curr_month)


    prev_month = curr_month -1
    next_month = curr_month+1
    if prev_month == 0:

        prev_month = 12
        all_dates_previous = calendar.monthcalendar(year_previous,prev_month)
        all_dates_previous = [i[:5] for i in all_dates_previous][-1]
    else:
        all_dates_previous = calendar.monthcalendar(curr_year,prev_month)
        all_dates_previous = [i[:5] for i in all_dates_previous][-1]


    all_dates_now = calendar.monthcalendar(curr_year,curr_month)
    all_dates_now = [i[:5] for i in all_dates_now]
    if next_month >12:

        next_month = 1
        all_dates_next = calendar.monthcalendar(year_next,next_month)
        all_dates_next = [i[:5] for i in all_dates_next][0]
    else:
        all_dates_next = calendar.monthcalendar(curr_year,next_month)
        all_dates_next = [i[:5] for i in all_dates_next][0]

  
    days = ['Понеділок','Вівторок','Середа','Четвер',"П'ятниця"]


    days_calendar = []
    days_date = []
    c = 0

    all_days_month = []
    for a in all_dates_now:
        if a.count(0) != 5:
            all_days_month.append(days)

    for a in all_dates_now:
        if 0 in a:
            if a.count(0) != 5:
            
                if a == all_dates_now[0]:
                    
                    b = [str(i)+'.'+ str(prev_month) for i in all_dates_previous if i != 0]
                    for i in a:
                        if i != 0:
                            b.append(i)
                    all_dates_now[0] = b

                if a == all_dates_now[-1]:
                    
                    b = [str(i)+'.'+ str(next_month) for i in all_dates_next if i != 0]
                    for i in range(a.count(0)):
                        a.remove(0)
                    for i in b:
                        a.append(i)
            else:
                all_dates_now.remove(a)

    dates_represent =[]
    for i in all_dates_now:
        for o in i:
            dates_represent.append(o)


    if request.method == 'GET':
        return render_template('add_homework.html',date_list= dates_represent)
    
    else:

        date_homework = request.form.get('date')
        subj = request.form.get('subjects')
        desc = request.form.get('hw_input')
        if len(date_homework.split('.')) == 1:
            total_date = date_homework +'.'+str(curr_month) +'.'+ str(curr_year)
        if len(date_homework.split('.')) == 2:
            month = int(date_homework.split('.')[1])
            if curr_month == 12 and month == 1:
                total_date = date_homework +'.'+str(year_next)
            
            elif curr_month == 1 and month == 12:
                total_date = date_homework +'.'+ str(year_previous)
            else:
                total_date = date_homework +'.'+ str(curr_year)

        
        total_date = datetime.strptime(total_date,'%d.%m.%Y').date()
        
        
        
        add_homework(total_date,subj,desc)
        return redirect(url_for('add_hw'))
    



def get_marks_url():
    url = request.url

    a =url.split('/')
    id = int(a[-1])
    return get_marks(id)
    

def get_news_page():
    url = request.url

    a =url.split('/')
    id = int(a[-1])
    

    return get_markndate(id)
    
def get_homework_page():
    
    return get_homework()

def add_device_acc():
    
    a = request.data
    dict_login = ast.literal_eval(a.decode('utf-8'))
    devices_id('ADD',dict_login['device_id'],dict_login['log_id'])
    
    return 's'
    
def check_device():
    a = request.data
    dict_login = ast.literal_eval(a.decode('utf-8'))
    device = dict_login['device']

    log_id = devices_id('CHECK_DEVICE',device,None)
    
    return str(log_id)

def get_names_show():
    a = request.data
    dict_login = ast.literal_eval(a.decode('utf-8'))

    return str(get_names_by_id(dict_login['id']))



app.add_url_rule('/add_mark','add_mark',mark_fill_page,methods = ['post','get'])
app.add_url_rule('/add_hw','add_hw',add_homework_page,methods = ['post','get'])
app.add_url_rule('/schedule','schedule',schedule,methods = ['post','get'])
app.add_url_rule('/get_hw','gethw',get_homework_page,methods= ['post','get'])
app.add_url_rule('/get_hw','gethw',get_homework_page,methods= ['post','get'])
app.add_url_rule('/add_device','adddevice',add_device_acc,methods= ['post'])
app.add_url_rule('/check_device','checkdevice',check_device,methods=['post'])
app.add_url_rule('/get_names_id','get_names',get_names_show,methods = ['post'])




for i in range(get_log_pass()[-1][0]):
    i = i+1
    app.add_url_rule(f'/get_marks/{i}',f'get_marks{i}',get_marks_url,methods = ['post','get'])

for i in range(get_log_pass()[-1][0]):
    i = i+1
    app.add_url_rule(f'/get_news/{i}',f'get_news{i}',get_news_page,methods = ['post','get'])



#pythonanywere запустити хост
if __name__ == '__main__':
    app.run()
