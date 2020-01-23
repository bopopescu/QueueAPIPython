"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,jsonify
from QueApiFlask import app
import mysql.connector as mariadb
import string,random



connection=mariadb.connect(host='10.130.7.135',user='tescousr',password='root@123',database='tescodb')

@app.route('/api/analyticsqueu')
def APIAnalyticsQueu():
    threshold=request.args.get('threshold')
    interval_lis=[4,5,6,7]
    inter=[]
    dic={}
    for i in interval_lis:
        dic={}
        #sqlquery='select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL @interval MINUTE) group by queue_name) d group by d.people_coun having d.people_coun >= @threshhold'
        cursor=connection.cursor()
        #cursor.execute('select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d group by d.people_coun having d.people_coun >= %s',(i,threshold))
        cursor.execute('select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where timestamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d where d.people_coun  >= %s',(i,threshold))
        records=cursor.fetchone()
        dic['intervals']=i
        dic['number']=records
        inter.append(dic.copy())
    dic['inter']=inter
    return jsonify(dic)

@app.route('/api/max_people')
def max_people_for_each_queue():
    time_r=request.args.get('interval')
    cursor=connection.cursor()
    tt=5
    cursor.execute('select queue_name,max(people_count) as people_coun from QueueCount  where timestamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name ',(tt))
    records=cursor.fetchone()
    dic={}
    inter=[]
    for i in records:
        dic={}
        dic['queue_name']=i[0]
        dic['count_people']=i[1]
        inter.append(dic.copy())
    dic['queue']=inter
    return jsonify(dic)

@app.route('/api/home')
def select_home_queues():
    queue=request.args.get('Queue')
    cursor=connection.cursor()
    if queue=="Q1":
        cursor.execute('select * from (select Queue_Name,max(people_count) as people_coun from QueueCount  where time_stamp >  DATEADD(MINUTE ,@time,  GetDate()) group by Queue_Name ) as p where p.Queue_Name between ')
        records=cursor.fetchone()
        inter=[]
        dic={}
        for i in records:
            dic={}
            dic['Queue_Name']=i[0]
            dic['people_count']=i[1]
            inter.append(dic.copy())
        dic['queue']=inter
        return jsonify(dic)
    else:
        cursor.execute('select * from (select Queue_Name,max(people_count) as people_coun from QueueCount  where time_stamp >  DATEADD(MINUTE ,@time,  GetDate()) group by Queue_Name ) as p where p.Queue_Name between ')
        records=cursor.fetchone()
        inter=[]
        dic={}
        for i in records:
            dic={}
            dic['Queue_Name']=i[0]
            dic['people_count']=i[1]
            inter.append(dic.copy())
        dic['queue']=inter
        return jsonify(dic)

@app.route('/api/user')
def user_insertion():
    letters=string.ascii_lowercase
    user_c=''.join(random.sample(letters,4))
    input_key=request.args.get(Key)
    cursor=connection.cursor()
    dic={}
    cursor.execute('insert into QueueUser(UserName,FCM) values(%s,%s)',(user_c,input_key))
    if(cursor.rowcount==1):
        dic['result']='Success'
    else:
        dic['result']='Failed'
    return dic


@app.route('/api/quepercent')
def percent_queue():
    time_r=request.args.get(interval)
    cursor=connection.cursor()
    cursor.execute('select queue_name,max(people_count) as people_coun from QueueCount  where timestamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name ',(time_r))
    records=cursor.fetchone()
    dic={}
    inter=[]
    for i in records:
        percent_peopl=(i[1]*100)/len(records)
        dic={}
        dic['queue_name']=i[0]
        dic['count_people']=i[1]
        dic['percent_peop']=percent_peopl
        inter.append(dic.copy())
    dic['queue']=inter
    return jsonify(dic)







        







@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
