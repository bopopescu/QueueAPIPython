"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,jsonify
from QueApiFlask import app
import mysql.connector as mariadb
import string,random
from .modules import page_three as pg
from .modules import page_two as ptwo
from .modules import page_one as pone



@app.route('/api/analyticsqueu')
def APIAnalyticsQueu():
    threshold=request.args.get('threshold')
    store_type=request.args.get('storetype')
    queue_name=request.args.get('queue')
    if store_type=='express':
        db="tesco_express"
        return(pg(threshold,db,queue_name))
    elif store_type=='hyper':
        db="tesco_hyper"
        return(pg(threshold,db,queue_name))
    else:
        db="tesco_super"
        return(pg(threshold,db,queue_name))

    

@app.route('/api/max_people')
def max_people_for_each_queue():
    time_r=request.args.get('interval')
    cursor=connection.cursor()
    tt=5
    cursor.execute('select queue_name,max(people_count) as people_coun from QueueCount  where timestamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name ',(tt,))
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
    queue_name=request.args.get('queue')
    store_type=request.args.get('storetype')
    interval=request.args.get('interval')
    if store_type=='express':
        db="tesco_express"
        return(pone(interval,db,queue_name))
    elif store_type=='hyper':
        db="tesco_hyper"
        return(pone(interval,db,queue_name))
    else:
        db="tesco_super"
        return(pone(interval,db,queue_name))
    

@app.route('/api/user',methods=['POST'])
def user_insertion():
    connection=mariadb.connect(host='52.172.157.210',user='tescouser',password='tesco@123',database='tesco_users')
    if request.method=='POST':
        
        json_key=request.get_json()
        letters=string.ascii_lowercase
        user_c=''.join(random.sample(letters,4))
        print(json_key)
        input_key=json_key['key']
        cursor=connection.cursor()
        print(input_key)
        dic={}
        cursor.execute('insert into fcm_store(UserName,FCM) values(%s,%s)',(user_c,input_key))
        connection.commit()
        if(cursor.rowcount==1):
            dic['result']='Success'
        else:
            dic['result']='Failed'
        return jsonify(dic)
    return "It is not Post Request"


@app.route('/api/quepercent')
def percent_queue():
    queue_name=request.args.get('queue')
    store_type=request.args.get('storetype')
    interval=request.args.get('interval')
    if store_type=='express':
        db="tesco_express"
        return(ptwo(interval,db,queue_name))
    elif store_type=='hyper':
        db="tesco_hyper"
        return(ptwo(interval,db,queue_name))
    else:
        db="tesco_super"
        return(ptwo(interval,db,queue_name))












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
