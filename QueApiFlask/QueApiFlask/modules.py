from datetime import datetime
from flask import render_template,request,jsonify
from QueApiFlask import app
import mysql.connector as mariadb
import string,random



connection=mariadb.connect(host='10.130.6.125',user='tescouser',password='tesco@123',database='tesco_express')



def page_three(threshold,db,queue_name):
    interval_lis=[4,5,6,7]
    inter=[]
    di={}
    if queue_name=='Q1':
        connection=mariadb.connect(host='10.130.6.125',user='tescouser',password='tesco@123',database=db)
        for i in interval_lis:
            dic={}
            #sqlquery='select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL @interval MINUTE) group by queue_name) d group by d.people_coun having d.people_coun >= @threshhold'
            cursor=connection.cursor()
            #cursor.execute('select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d group by d.people_coun having d.people_coun >= %s',(i,threshold))
            cursor.execute("""select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d where d.people_coun  >= %s and REPLACE(d.Queue_Name,'Q','') between '1' and '5' """,(i,threshold))
            records=cursor.fetchall()
            print(records)
            dic['intervals']=i
            dic['number']=records
            inter.append(dic.copy())
        print(inter)
        di['inter']=inter
        return jsonify(di)    
    else:
        connection=mariadb.connect(host='10.130.6.125',user='tescouser',password='tesco@123',database=db)
        for i in interval_lis:
            dic={}
            #sqlquery='select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL @interval MINUTE) group by queue_name) d group by d.people_coun having d.people_coun >= @threshhold'
            cursor=connection.cursor()
            #cursor.execute('select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d group by d.people_coun having d.people_coun >= %s',(i,threshold))
            cursor.execute("""select count(d.people_coun) as number_of_people from (select queue_name, max(people_count) as people_coun from QueueCount  where time_stamp > DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by queue_name) d where d.people_coun  >= %s and REPLACE(p.Queue_Name,'Q','') between '1' and '5' """,(i,threshold))
            records=cursor.fetchall()
            dic['intervals']=i
            dic['number']=records
            inter.append(dic.copy())
        di['inter']=inter
        return jsonify(di)   
        

def page_one(interval,db,queue_name):
    connection=mariadb.connect(host='10.130.6.125',user='tescouser',password='tesco@123',database=db)
    cursor=connection.cursor()
    
    if queue_name=='Q1': 
        cursor.execute("""select * from (select Queue_Name,max(people_count) as people_coun from QueueCount  where time_stamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL 50 MINUTE) group by Queue_Name ) as p where REPLACE(p.Queue_Name,'Q','') between '1' and '5' """)
        records=cursor.fetchall()
        inter=[]
        di={}
        print(records)
        for i in records:
            dic={}
            dic['Queue_Name']=i[0]
            dic['people_count']=i[1]
            inter.append(dic.copy())
        di['queue']=inter
        return jsonify(di)   
    else:
        cursor.execute("""select * from (select Queue_Name,max(people_count) as people_coun from QueueCount  where time_stamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by Queue_Name ) as p where REPLACE(p.Queue_Name,'Q','') between 'Q1' and 'Q5' """,(interval))
        records=cursor.fetchall()
        inter=[]
        di={}
        for i in records:
            dic={}
            dic['Queue_Name']=i[0]
            dic['people_count']=i[1]
            inter.append(dic.copy())
        di['queue']=inter
        return jsonify(di) 


def page_two(interval,db,queue_name):
    connection=mariadb.connect(host='10.130.6.125',user='tescouser',password='tesco@123',database=db)
    cursor=connection.cursor()
    if queue_name=='Q1': 
        cursor.execute("""select * from (select Queue_Name,max(people_count) as people_coun from QueueCount  where time_stamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL 50 MINUTE) group by Queue_Name ) as p where REPLACE(p.Queue_Name,'Q','') between '1' and '5' """)
        records=cursor.fetchall()
        inter=[]
        di={}
        for i in records:
            percent_peopl=(i[1]*100)/len(records)
            dic={}
            dic['queue_name']=i[0]
            dic['count_people']=i[1]
            dic['percent_peop']=percent_peopl
            inter.append(dic.copy())
        di['queue']=inter
        return jsonify(di)   
    else:
        cursor.execute("""select * from (select Queue_Name,max(people_count) as people_coun from QueueCount  where time_stamp >  DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL %s MINUTE) group by Queue_Name ) as p where REPLACE(p.Queue_Name,'Q','') between 'Q1' and 'Q5' """,(interval))
        records=cursor.fetchall()
        inter=[]
        di={}
        for i in records:
            percent_peopl=(i[1]*100)/len(records)
            dic={}
            dic['queue_name']=i[0]
            dic['count_people']=i[1]
            dic['percent_peop']=percent_peopl
            inter.append(dic.copy())
        di['queue']=inter
        return jsonify(di)  
