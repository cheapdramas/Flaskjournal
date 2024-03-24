from datetime import datetime,date
import calendar
from flask import Flask,session,request,redirect,url_for,render_template,request,jsonify
from db_scripts import *
import os
import ast
import json

PATH = "c:/flaskjournal/"
PATH_STATIC = os.path.join("c:/flaskjournal/" + 'static')

app = Flask(__name__)

app.config['DATABASE_URL'] = 'postgres://u7kffgs978unra:pc0a9409eed2de5a6bc74240aa2c23c126d7e7c8d7432b813a625dd0e1db9e0b8@cd5vlri6nnqe17.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddtlk7of7bpj1f'


@app.route('/')
def show_hello():
    return 'Hello'


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
