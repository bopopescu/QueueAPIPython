"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,jsonify
from QueApiFlask import app
import mysql.connector as mariadb



connection=mariadb.connect(host='10.130.6.190',user='tescousr',password='Sp@culat1on',database='tescodb')

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
        cursor.execute('select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d where d.people_coun  >= %s',(i,threshold))
        records=cursor.fetchone()
        dic['intervals']=i
        dic['number']=records
        inter.append(dic.copy())
    dic['inter']=inter
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
