from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib

import cv2
import imagehash
import PIL.Image
from PIL import Image
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

# import mysql.connector
import pymysql
from pymysql import Error

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="kannan_45",
    charset="utf8",
    database="chain_of_custody"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""

    file = open('static/upload/E3.hash', 'rb')
    byte = file.read()
    file.close()
      
    decodeit = open('static/upload/E3.jpg', 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()

    return render_template('index.html',msg=msg,act=act)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM coc_login where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login.html',msg=msg,act=act)


@app.route('/login_auth',methods=['POST','GET'])
def login_auth():
    cnt=0
    act=""
    msg=""

    
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM coc_register where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('home')) 
        else:
            msg="Invalid Username or Password!"
            
    return render_template('login_auth.html',msg=msg,act=act)


@app.route('/digital-evidence-management')
def digital_evidence_management():
    return render_template('digital-evidence-management.html')

@app.route('/forensic-analysis')
def forensic_analysis():
    return render_template('forensic-analysis.html')

@app.route('/blockchain-solutions')
def blockchain_solutions():
    return render_template('blockchain-solutions.html')

@app.route('/security-consulting')
def security_consulting():
    return render_template('security-consulting.html')

@app.route('/training-certification')
def training_certification():
    return render_template('training-certification.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    msg=""
    act=""
    email=""
    mess=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT count(*) FROM coc_case")
    data1 = mycursor.fetchone()[0]
    
    mycursor.execute("SELECT count(*) FROM coc_register")
    data2 = mycursor.fetchone()[0]

    mycursor.execute("SELECT count(*) FROM coc_request where status=0")
    data3 = mycursor.fetchone()[0]

    mycursor.execute("SELECT count(*) FROM coc_attack where status=0")
    data4 = mycursor.fetchone()[0]

    return render_template('admin.html', msg=msg,data1=data1,data2=data2,data3=data3,data4=data4)

@app.route('/view_req', methods=['GET', 'POST'])
def view_req():

    msg=""
    act=request.args.get("act")
    st=""
    rid=request.args.get("rid")
    email=""
    mess=""
    data=[]

    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM coc_register order by id")
    data2 = mycursor.fetchall()
        
    mycursor.execute("SELECT count(*) FROM coc_request")
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM coc_request order by id desc")
        data = mycursor.fetchall()

        mycursor.execute("update coc_request set status=1")
        mydb.commit()

    
    if request.method == 'POST':
        if act=="send":
            user = request.form['user']
            message = request.form['message']
            mycursor.execute("SELECT max(id)+1 FROM coc_request")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO coc_request(id,uname,message,reply,status,cname) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (maxid,'admin',message,'','0',user)
            mycursor.execute(sql, val)
            mydb.commit()
            ###
            mycursor.execute('SELECT * FROM coc_request WHERE id=%s', (maxid,))
            dd = mycursor.fetchone()
            dtime=str(dd[5])
            bdata="Request ID:"+str(maxid)+", User ID:"+user+", Status:Request by admin, Date: "+dtime
            ###
            msg="send"
        else:
            
            reply = request.form['reply']
            mycursor.execute("update coc_request set reply=%s where id=%s",(reply,rid))
            mydb.commit()
            ###
            mycursor.execute('SELECT * FROM coc_request WHERE id=%s', (rid,))
            dd = mycursor.fetchone()
            dtime=str(dd[5])
            bdata="Request ID:"+rid+", User ID:"+dd[1]+", Status:Reply by admin, Date: "+dtime
            ###
            msg="reply"

        
    

    return render_template('view_req.html', msg=msg,act=act,data=data,data2=data2,st=st,bc=bc,bdata=bdata)

@app.route('/view_noti', methods=['GET', 'POST'])
def view_noti():

    msg=""
    act=request.args.get("act")
    st=""
    email=""
    mess=""
    data=[]

    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT count(*) FROM coc_attack")
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM coc_attack order by id desc")
        data = mycursor.fetchall()

        mycursor.execute("update coc_attack set status=1")
        mydb.commit()

    return render_template('view_noti.html', msg=msg,act=act,data=data,st=st)

@app.route('/add_auth', methods=['GET', 'POST'])
def add_auth():
    msg=""
    act=""
    email=""
    mess=""
    mycursor = mydb.cursor()
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
            
    if request.method=='POST':
        name=request.form['name']
        designation=request.form['designation']
        mobile=request.form['mobile']
        email=request.form['email']
        aadhar=request.form['aadhar']
        location=request.form['location']
        city=request.form['city']

        

        mycursor.execute("SELECT count(*) FROM coc_register where aadhar=%s",(aadhar,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM coc_register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            uname="AT"+str(maxid)
            p1=randint(1000,9999)
            pass1="123456"
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO coc_register(id,name,designation,mobile,email,aadhar,location,city,uname,pass,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,designation,mobile,email,aadhar,location,city,uname,pass1,'1')
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            act="1"
            mess="Dear "+name+", Authorized Party - User ID: "+uname+", Password: "+pass1
            ###
            mycursor.execute('SELECT * FROM coc_register WHERE id=%s', (maxid,))
            dd = mycursor.fetchone()
            dtime=str(dd[11])
            bdata="ID:"+str(maxid)+", User ID:"+uname+", Status:Authorized User Created, Aadhar:"+aadhar+", Date: "+dtime
            ###
            
        else:
            
            msg='fail'

    
    
    return render_template('add_auth.html',msg=msg,email=email,mess=mess,act=act,bc=bc,bdata=bdata)

@app.route('/add_case', methods=['GET', 'POST'])
def add_case():
    msg=""
    act=""
    email=""
    mess=""

    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        district=request.form['district']
        station=request.form['station']
        title=request.form['title']
        cdate=request.form['cdate']
        details=request.form['details']
        suspect=request.form['suspect']
        name=request.form['name']
        fname=request.form['fname']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        district2=request.form['district2']
        pincode=request.form['pincode']
        mobile=request.form['mobile']
        email=request.form['email']
        aadhar=request.form['aadhar']
        
        mycursor.execute("SELECT max(id)+1 FROM coc_case")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        mm=now.strftime("%m")
        yy=now.strftime("%Y")
        case_id="C"+mm+yy+str(maxid)
        
        sql = "INSERT INTO coc_case(id,case_id,district,station,title,cdate,details,suspect,name,fname,gender,dob,address,district2,pincode,mobile,email,aadhar,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,case_id,district,station,title,cdate,details,suspect,name,fname,gender,dob,address,district2,pincode,mobile,email,aadhar,'0')
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        act="1"
        
        mycursor.execute('SELECT * FROM coc_case WHERE id=%s', (maxid,))
        dd = mycursor.fetchone()
        dtime=str(dd[19])
        bdata="ID:"+str(maxid)+", Case ID:"+case_id+", Status:Case Registered, Complainant Name: "+name+", Date: "+dtime
        
     
    
    return render_template('add_case.html',msg=msg,email=email,mess=mess,act=act,bc=bc,bdata=bdata)

@app.route('/add_evidence', methods=['GET', 'POST'])
def add_evidence():
    msg = ""
    cid = request.args.get("cid")
    act = request.args.get("act")
    email = ""
    mess = ""
    efile = ""
    data2 = []
    st = ""
    case_id = ""    

    bdata = ""
    with open("bc.txt", "r") as f:
        bc = f.read()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_case WHERE id=%s", (cid,))
    data = mycursor.fetchone()
    
    if data:
        case_id = data[1]

        mycursor.execute("SELECT count(*) FROM coc_evidence WHERE case_id=%s", (case_id,))
        cnt = mycursor.fetchone()[0]
        
        if cnt > 0:
            st = "1"
            mycursor.execute("SELECT * FROM coc_evidence WHERE case_id=%s", (case_id,))
            data2 = mycursor.fetchall()

        if request.method == 'POST':
            details = request.form['details']
            file = request.files['file']
            now = date.today()
            rdate = now.strftime("%d-%m-%Y")

            if file:
                fname = file.filename
                filename = secure_filename(fname)
                efile = "E" + str(case_id) + filename
                file.save(os.path.join("static/upload1", efile))

                with open("static/upload1/" + efile, "rb") as image2string:
                    converted_string = base64.b64encode(image2string.read())
                print(converted_string)
                bfile1 = "E" + str(case_id) + ".hash"
                with open('static/upload/' + bfile1, "wb") as f:
                    f.write(converted_string)

            mm = now.strftime("%m")
            yy = now.strftime("%Y")

            sql = "INSERT INTO coc_evidence(case_id,details,filename,upload_by) VALUES (%s,%s,%s,%s)"
            val = (case_id, details, efile, 'admin')
            mycursor.execute(sql, val)
            mydb.commit()

            msg = "success"
            act = "1"
            mycursor.execute('SELECT * FROM coc_evidence WHERE case_id=%s ORDER BY id DESC LIMIT 1', (case_id,))
            dd = mycursor.fetchone()
            dtime = str(dd[4])
            bdata = "Evidence ID:" + str(dd[0]) + ", Case ID:" + case_id + ", Status: Evidence File: " + efile + ", Upload by admin, Date: " + dtime

        if act == "del":
            did = request.args.get("did")
            mycursor.execute("SELECT * FROM coc_evidence WHERE id=%s", (did,))
            dd = mycursor.fetchone()
            if dd:
                dtime = str(dd[4])
                bdata = "Evidence ID:" + str(did) + ", Case ID:" + case_id + ", Status:Evidence File Deleted, File: " + dd[3] + ", Date: " + dtime
                msg = "deleted"

                mycursor.execute("DELETE FROM coc_evidence WHERE id=%s", (did,))
                mydb.commit()

    return render_template('add_evidence.html', msg=msg, email=email, mess=mess, act=act, cid=cid, case_id=case_id, data2=data2, bc=bc, bdata=bdata, st=st)
@app.route('/allow', methods=['GET', 'POST'])
def allow():
    msg=""
    
    cid=request.args.get("cid")
    act=request.args.get("act")
    email=""
    mess=""
    efile=""
    data2=[]
    st=""
    q=""
    s1="0"
    s2="0"

    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_case where id=%s",(cid,))
    data = mycursor.fetchone()
    
    case_id=data[1]

    mycursor.execute("SELECT * FROM coc_register")
    data2 = mycursor.fetchall()



    if request.method=='POST':
        user=request.form['user']
        ch=request.form.getlist('ch[]')
        print(ch)
        l=len(ch)
        if l==2:
            s1="1"
            s2="1"
            q="View and Upload"
        elif l==1:
            if ch[0]=="1":
                s1="1"
                s2="0"
                q="View"
            else:
                s2="1"
                s1="1"
                q="View and Upload"

        mycursor.execute('SELECT count(*) FROM coc_allow WHERE uname=%s && case_id=%s', (user,case_id))
        c1 = mycursor.fetchone()[0]
        if c1==0:

            mycursor.execute("SELECT max(id)+1 FROM coc_allow")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                
            sql = "INSERT INTO coc_allow(id,uname,case_id,view_st,upload_st) VALUES (%s,%s,%s,%s,%s)"
            val = (maxid,user,case_id,s1,s2)
            mycursor.execute(sql, val)
            mydb.commit()

            ###
            mycursor.execute('SELECT * FROM coc_allow WHERE id=%s', (maxid,))
            dd = mycursor.fetchone()
            dtime=str(dd[5])
            bdata="Allow ID:"+str(maxid)+", Case ID:"+case_id+", Status:Allowed for "+q+", User:"+user+", Date: "+dtime
            ###
        else:
            mycursor.execute("update coc_allow set view_st=%s,upload_st=%s where uname=%s && case_id=%s", (s1,s2,user,case_id))
            mydb.commit()
            ###
            mycursor.execute("SELECT * FROM coc_allow WHERE uname=%s && case_id=%s", (user,case_id))
            dd = mycursor.fetchone()
            dtime=str(dd[5])
            bdata="Allow ID:"+str(dd[0])+", Case ID:"+case_id+", Status:Allowed for "+q+", User:"+user+", Date: "+dtime
            ###

            
        msg="allow"
        
        
    
    return render_template('allow.html',msg=msg,data=data,act=act,cid=cid,case_id=case_id,data2=data2,bc=bc,bdata=bdata,st=st)

@app.route('/access', methods=['GET', 'POST'])
def access():
    msg = ""
    cid = request.args.get("cid")
    act = request.args.get("act")
    
    # Query the database to find evidence ID based on the provided case ID
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM coc_evidence WHERE case_id = %s", (cid,))
    evidence_data = mycursor.fetchone()
    if evidence_data:
        eid = evidence_data[0]
    else:
        # Handle case where no evidence is found for the provided case ID
        return render_template('error.html', message="No evidence found for the specified case ID")

    email = ""
    mess = ""
    efile = ""
    data2 = []
    st = ""
    q = ""
    s1 = "0"
    s2 = "0"

    bdata = ""
    f1 = open("bc.txt", "r")
    bc = f1.read()
    f1.close()

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_evidence where id=%s", (eid,))
    data = mycursor.fetchone()

    if data:
        case_id = data[1]

        mycursor.execute("SELECT * FROM coc_register")
        data2 = mycursor.fetchall()

        if request.method == 'POST':
            user = request.form['user']
            ch = request.form.getlist('ch[]')
            print(ch)
            l = len(ch)
            if l == 2:
                s1 = "1"
                s2 = "1"
                q = "View and Download"
            elif l == 1:
                if ch[0] == 1:
                    s1 = "1"
                    q = "View"
                else:
                    s2 = "1"
                    if q == "":
                        q = "Download"
                    else:
                        q = "View and Download"

            mycursor.execute('SELECT count(*) FROM coc_access WHERE uname=%s && eid=%s', (user, eid))
            c1 = mycursor.fetchone()[0]
            if c1 == 0:
                mycursor.execute("SELECT max(id)+1 FROM coc_access")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid = 1

                sql = "INSERT INTO coc_access(id,uname,eid,case_id,view_st,download_st) VALUES (%s,%s,%s,%s,%s,%s)"
                val = (maxid, user, eid, case_id, s1, s2)
                mycursor.execute(sql, val)
                mydb.commit()

                mycursor.execute('SELECT * FROM coc_access WHERE id=%s', (maxid,))
                dd = mycursor.fetchone()
                dtime = str(dd[6])
                bdata = "Access ID:" + str(maxid) + ", Case ID:" + case_id + ", Status:Access for " + q + ", User:" + user + ", Date: " + dtime
                msg = "access"
            else:
                mycursor.execute("update coc_access set view_st=%s,download_st=%s where uname=%s && case_id=%s",
                                 (s1, s2, user, case_id))
                mydb.commit()

                mycursor.execute("SELECT * FROM coc_access WHERE uname=%s && eid=%s", (user, eid))
                dd = mycursor.fetchone()
                dtime = str(dd[6])
                bdata = "Access ID:" + str(dd[0]) + ", Case ID:" + case_id + ", Status:Access for " + q + ", User:" + user + ", Date: " + dtime

                msg = "access"

        return render_template('access.html', msg=msg, data=data, act=act, cid=cid, case_id=case_id, data2=data2,
                               bc=bc, bdata=bdata, st=st, eid=eid)
    else:
        # Handle the case where no data is found for the specified eid
        return "No data found for the specified eid", 404




@app.route('/view_auth', methods=['GET', 'POST'])
def view_auth():
    msg=""
    act=request.args.get("act")
    email=""
    mess=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_register")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from coc_register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_auth'))
    
    return render_template('view_auth.html',msg=msg,act=act,data=data)


@app.route('/view_case', methods=['GET', 'POST'])
def view_case():
    msg=""
    act=request.args.get("act")
    email=""
    mess=""
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_case order by id desc")
    data = mycursor.fetchall()

    if act == "del":
        did = request.args.get("did")
        
        # Update coc_case status
        try:
            mycursor.execute("UPDATE coc_case SET status = 0 WHERE id = %s", (did,))
            mydb.commit()
        except mysql.connector.Error as err:
            # Handle MySQL errors
            print(f"Error updating coc_case status: {err}")
            # Optionally, you can return an error message to the user
            return render_template('error.html', message="An error occurred while deleting the case.")

        # Fetch the deleted case data
        try:
            mycursor.execute("SELECT * FROM coc_case WHERE id = %s", (did,))
            dd = mycursor.fetchone()
            dtime = str(dd[19])  # Assuming the date is at index 19, adjust if needed
            bdata = f"ID: {did}, Case ID: {dd[1]}, Status: Case Deleted, Date: {dtime}"
        except mysql.connector.Error as err:
            # Handle MySQL errors
            print(f"Error fetching deleted case data: {err}")
            # Optionally, you can return an error message to the user
            return render_template('error.html', message="An error occurred while fetching case data.")

        # Delete related evidence records
        try:
            mycursor.execute("DELETE FROM coc_evidence WHERE case_id = %s", (dd[1],))
            mydb.commit()
        except mysql.connector.Error as err:
            # Handle MySQL errors
            print(f"Error deleting related evidence records: {err}")
            # Optionally, you can return an error message to the user
            return render_template('error.html', message="An error occurred while deleting related evidence records.")

        # Delete the case record
        try:
            mycursor.execute("DELETE FROM coc_case WHERE id = %s", (did,))
            mydb.commit()
        except mysql.connector.Error as err:
            # Handle MySQL errors
            print(f"Error deleting case record: {err}")
            # Optionally, you can return an error message to the user
            return render_template('error.html', message="An error occurred while deleting the case.")

        msg = "deleted"

    return render_template('view_case.html', msg=msg, act=act, data=data, bc=bc, bdata=bdata)




@app.route('/view_casefull', methods=['GET', 'POST'])
def view_casefull():
    msg=""
    cid = request.args.get("cid")
    data = None
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_case WHERE id=%s", (cid,))
    data = mycursor.fetchone()
    print(data)
    return render_template('view_casefull.html', msg=msg, data=data)

@app.route('/home', methods=['GET', 'POST'])
def home():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_register where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    return render_template('home.html',data=data,act=act)

@app.route('/a_view_case', methods=['GET', 'POST'])
def a_view_case():
    msg=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']

    data=[]
    email=""
    mess=""
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()

    st=""
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM coc_case c,coc_allow a where a.case_id=c.case_id && a.uname=%s order by c.id desc",(uname,))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM coc_case c,coc_allow a where a.case_id=c.case_id && a.uname=%s order by c.id desc",(uname,))
        data = mycursor.fetchall()

    
    
    return render_template('a_view_case.html',msg=msg,act=act,data=data,bc=bc,bdata=bdata)


@app.route('/a_upload', methods=['GET', 'POST'])
def a_upload():
    msg=""
    cid=request.args.get("cid")
    eid=request.args.get("eid")
    act=request.args.get("act")
    email=""
    mess=""
    efile=""
    data1=[]
    data2=[]
    bdata1=""
    msg1=""
    st=""

    uname=""
    if 'username' in session:
        uname = session['username']

    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_case where id=%s",(cid,))
    data = mycursor.fetchone()
    case_id=data[1]

    mycursor.execute("SELECT count(*) FROM coc_case c,coc_allow a where a.case_id=c.case_id && a.uname=%s order by c.id desc",(uname,))
    cnt1 = mycursor.fetchone()[0]
    if cnt1>0:
        st="1"
        mycursor.execute("SELECT * FROM coc_case c,coc_allow a where a.case_id=c.case_id && a.uname=%s && a.case_id=%s order by c.id desc",(uname,case_id))
        data1 = mycursor.fetchone()

        

    mycursor.execute("SELECT count(*) FROM coc_evidence where case_id=%s",(case_id,))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM coc_evidence where case_id=%s",(case_id,))
        dd2 = mycursor.fetchall()
        for ds2 in dd2:
            dt2=[]
            dt2.append(ds2[0])
            dt2.append(ds2[1])
            dt2.append(ds2[2])
            dt2.append(ds2[3])
            dt2.append(ds2[4])
            dt2.append(ds2[5])
            dt2.append(ds2[6])

            mycursor.execute("SELECT count(*) FROM coc_access where eid=%s && uname=%s",(ds2[0],uname))
            n3 = mycursor.fetchone()[0]
            if n3>0:
                mycursor.execute("SELECT * FROM coc_access where eid=%s && uname=%s",(ds2[0],uname))
                d3 = mycursor.fetchone()
                if d3[5]==1:
                    dt2.append("1")
                elif d3[5]==2:
                    dt2.append("2")
                else:
                    dt2.append("3")
            else:
                dt2.append("3")

            data2.append(dt2)
            

    if request.method=='POST':
        details=request.form['details']
        file=request.files['file']
        
        
        mycursor.execute("SELECT max(id)+1 FROM coc_evidence")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        if file:
            fname = file.filename
            filename = secure_filename(fname)
            efile="E"+str(maxid)+filename
            file.save(os.path.join("static/upload1", efile))

            with open("static/upload1/"+efile, "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())
            print(converted_string)
            bfile1="E"+str(maxid)+".hash"
            with open('static/upload/'+bfile1, "wb") as file:
                file.write(converted_string)

        mm=now.strftime("%m")
        yy=now.strftime("%Y")
        
        
        sql = "INSERT INTO coc_evidence(id,case_id,details,filename,upload_by) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid,case_id,details,efile,uname)
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        act="1"
        #mess="Dear "+name+", User ID: "+uname+", Password: "+pass1
        ###
        mycursor.execute('SELECT * FROM coc_evidence WHERE id=%s', (maxid,))
        dd = mycursor.fetchone()
        dtime=str(dd[4])
        bdata="Evidence ID:"+str(maxid)+", Case ID:"+case_id+", Status: Evidence File: "+efile+", upload by "+uname+", Date: "+dtime
        #################


        ####Fuzzy hash similarity verification######
        mycursor.execute('SELECT * FROM coc_evidence WHERE id=%s', (maxid,))
        dt = mycursor.fetchall()
        cutoff=10
        for rr in dt:
            hash0 = imagehash.average_hash(Image.open("static/upload1/"+rr[3])) 
            hash1 = imagehash.average_hash(Image.open("static/upload1/"+efile))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                pre_id=str(rr[0])
                
                break
            else:
                ss="no"
        if ss=="ok":
            mycursor.execute('SELECT * FROM coc_evidence where id=%s',(maxid,))
            sp3 = mycursor.fetchone()
            dtime=str(sp3[4])
            mycursor.execute('SELECT * FROM coc_evidence where id=%s',(pre_id,))
            sp1 = mycursor.fetchone()
            pre_user=sp1[6]
            mycursor.execute('SELECT * FROM coc_register where uname=%s',(pre_user,))
            sp2 = mycursor.fetchone()
            pre_vid=sp2[0]
            

            bdata1="ID:"+str(pre_vid)+", Case ID:"+sp3[1]+", Status:Attack Found, Similar Evidence uploaded by "+uname+", Evidence ID:"+str(maxid)+", File: "+sp3[3]+" (Previous ID:"+str(pre_id)+"), Date:"+dtime
            #bdata11="Evidence ID:"+str(maxid)+", User ID:"+uname+", Status:Evidence already exist, Previous ID:"+str(pre_id)+", Date:"+dtime
            msg1="attack"

            mycursor.execute("SELECT max(id)+1 FROM coc_attack")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
                
            sql2 = "INSERT INTO coc_attack(id,uname,eid,efile,case_id,status) VALUES (%s,%s,%s,%s,%s,%s)"
            val2 = (maxid2,uname,str(maxid),sp3[3],sp3[1],'0')
            mycursor.execute(sql2, val2)
            mydb.commit()
            
        ########
    ##########################
    if act=="req":
        mycursor.execute("SELECT * FROM coc_evidence where id=%s",(eid,))
        dd4 = mycursor.fetchone()
        mycursor.execute('SELECT count(*) FROM coc_access WHERE uname=%s && eid=%s', (uname,eid))
        c1 = mycursor.fetchone()[0]
        if c1==0:

            mycursor.execute("SELECT max(id)+1 FROM coc_access")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                
            sql = "INSERT INTO coc_access(id,uname,eid,case_id,view_st,download_st) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (maxid,uname,eid,case_id,'1','2')
            mycursor.execute(sql, val)
            mydb.commit()

            ###
            mycursor.execute('SELECT * FROM coc_access WHERE id=%s', (maxid,))
            dd = mycursor.fetchone()
            dtime=str(dd[6])
            bdata="Evidence ID:"+eid+", Case ID:"+case_id+", Status: "+dd4[3]+", Download Request by "+uname+", Date: "+dtime
            ###
        else:
            mycursor.execute("update coc_access set view_st='1',download_st='2' where uname=%s && case_id=%s", (uname,case_id))
            mydb.commit()
            ###
            mycursor.execute("SELECT * FROM coc_access WHERE uname=%s && eid=%s", (uname,eid))
            dd = mycursor.fetchone()
            dtime=str(dd[6])
            bdata="Evidence ID:"+eid+", Case ID:"+case_id+", Status: "+dd4[3]+", Download Request by "+uname+", Date: "+dtime
            ###

        mycursor.execute("SELECT max(id)+1 FROM coc_request")
        maxid2 = mycursor.fetchone()[0]
        if maxid2 is None:
            maxid2=1

        msgg="Evidence ID:"+eid+", Case ID:"+case_id+", File: "+dd4[3]+", Download Request by "+uname
        sql = "INSERT INTO coc_request(id,uname,message,reply,status) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid2,uname,msgg,'','0')
        mycursor.execute(sql, val)
        mydb.commit()
        msg="req"



    #####################

        
    
    return render_template('a_upload.html',msg=msg,email=email,mess=mess,act=act,cid=cid,case_id=case_id,data1=data1,data2=data2,bc=bc,bdata=bdata,st=st,bdata1=bdata1,msg1=msg1)

@app.route('/a_req', methods=['GET', 'POST'])
def a_req():
    msg=""
    st=""
    st2=""
    data=[]
    data3=[]
    uname=""
    if 'username' in session:
        uname = session['username']

    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM coc_request where uname=%s order by id desc",(uname,))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM coc_request where uname=%s order by id desc",(uname,))
        data = mycursor.fetchall()

    mycursor.execute("SELECT count(*) FROM coc_request where cname=%s order by id desc",(uname,))
    cnt2 = mycursor.fetchone()[0]
    if cnt2>0:
        st2="1"
        mycursor.execute("SELECT * FROM coc_request where cname=%s order by id desc",(uname,))
        data3 = mycursor.fetchall()

    if request.method == 'POST':
        
        message = request.form['message']
        mycursor.execute("SELECT max(id)+1 FROM coc_request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO coc_request(id,uname,message,reply,status) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid,uname,message,'','0')
        mycursor.execute(sql, val)
        mydb.commit()
        ###
        mycursor.execute('SELECT * FROM coc_request WHERE id=%s', (maxid,))
        dd = mycursor.fetchone()
        dtime=str(dd[5])
        bdata="Request ID:"+str(maxid)+", User ID:"+uname+", Status:Request, Date: "+dtime
        ###
        msg="send"

    return render_template('a_req.html',msg=msg,data=data,data3=data3,st=st,st2=st2,bc=bc,bdata=bdata)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    msg=""
    cnt=0
    uname=""
    mess=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    act=request.args.get("act")
    st=""
    pmode=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM coc_login")
    data = mycursor.fetchone()
    
    key=data[2]
    
    return render_template('verify.html',msg=msg,data=data,mess=mess,act=act,bc=bc,uname=uname,key=key)

@app.route('/down', methods=['GET', 'POST'])
def down():
    try:
        eid=request.args.get('eid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM coc_evidence where id=%s",(eid,))
        data = mycursor.fetchone()
        if not data:
            return "Evidence not found", 404
            
        fn=data[3]
        ff="E"+eid+".hash"
        
        # Ensure upload file exists
        upload_path = 'static/upload/'+ff
        if not os.path.exists(upload_path):
            return "Evidence file not found", 404
            
        # Ensure download directory exists
        down_dir = 'static/down'
        if not os.path.exists(down_dir):
            os.makedirs(down_dir)
            
        # Read and decode file
        file = open(upload_path, 'rb')
        byte = file.read()
        file.close()
        
        down_path = os.path.join(down_dir, fn)
        decodeit = open(down_path, 'wb')
        decodeit.write(base64.b64decode((byte)))
        decodeit.close()
        
        return send_file(down_path, as_attachment=True)
        
    except Exception as e:
        return str(e), 500

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
