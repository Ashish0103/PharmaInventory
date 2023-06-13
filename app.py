from flask import Flask, render_template,request,make_response
import plotly
import plotly.graph_objs as go
import mysql.connector
from mysql.connector import Error
import sys
import algorithms
import pandas as pd
import numpy as np
import json  #json request
from werkzeug.utils import secure_filename
import os
import csv #reading csv
import geocoder
from random import randint
import matplotlib.pyplot as plt



mon1=1.5
mon6=6
mon12=8

app = Flask(__name__)


@app.route('/')
def index():
    try:        
        g = geocoder.ip('me')
        print(g.latlng[0])
        print(g.latlng[1])
    except:
        print("Done")
    
    return render_template('index.html')

@app.route('/index')
def indexnew():    
    return render_template('index.html')

@app.route('/register')
def register():    
    return render_template('register.html')

@app.route('/forgotpassword')
def forgotpassword():    
    return render_template('forgotpassword.html')

@app.route('/fpassword')
def fpassword():
    import smtplib 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login("ashishshetty.com", "awsp hnqh qoqs ynyn")
    connection=mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    lgemail=request.args['email']
    lgpssword=request.args['pswd']
    print(lgemail, flush=True)
    print(lgpssword, flush=True)
    cursor = connection.cursor()
    sq_query="select Pswd from userdata where Email='"+lgemail+"'"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    pswd = int(data[0][0])
    connection.commit() 
    connection.close()
    cursor.close()
    strval = ""
      
    # message to be sent 
    message = "Your password is :"+str(pswd)
      
    # sending the mail 
    s.sendmail("ashishshetty@gmail.com", email, strval) 
      
    # terminating the session 
    s.quit()
    msg=''
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    return resp


@app.route('/login')
def login():
    return render_template('login.html')



""" REGISTER CODE  """

@app.route('/regdata', methods =  ['GET','POST'])
def regdata():
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    uname = request.args['uname']
    name = request.args['name']
    pswd = request.args['pswd']
    email = request.args['email']
    phone = request.args['phone']
    addr = request.args['addr']
    value = randint(123, 99999)
    uid="User"+str(value)
    print(addr)
        
    cursor = connection.cursor()
    sql_Query = "insert into userdata values('"+uid+"','"+uname+"','"+name+"','"+pswd+"','"+email+"','"+phone+"','"+addr+"')"
        
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    #msg = json.dumps(msg)
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp




"""LOGIN CODE """

@app.route('/logdata', methods =  ['GET','POST'])
def logdata():
    connection=mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    lgemail=request.args['email']
    lgpssword=request.args['pswd']
    print(lgemail, flush=True)
    print(lgpssword, flush=True)
    cursor = connection.cursor()
    sq_query="select count(*) from userdata where Email='"+lgemail+"' and Pswd='"+lgpssword+"'"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    rcount = int(data[0][0])
    print(rcount, flush=True)
    
    connection.commit() 
    connection.close()
    cursor.close()
    
    if rcount>0:
        msg="Success"
        resp = make_response(json.dumps(msg))
        return resp
    else:
        msg="Failure"
        resp = make_response(json.dumps(msg))
        return resp
        
   




    






@app.route('/dashboard')
def dashboard():
    try:        
        g = geocoder.ip('me')
        print(g.latlng[0])
        print(g.latlng[1])
    except:
        print("Done")
    connection=mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    cursor = connection.cursor()
    sq_query="select count(*) from userdata"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    ucount = int(data[0][0])
    print(ucount, flush=True)

    sq_query="select count(distinct Item) from dataset"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    tcount = int(data[0][0])
    print(tcount, flush=True) 

  
    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('dashboard.html',ucount=ucount,tcount=tcount)



@app.route('/adminhome')
def adminhome():
    try:        
        g = geocoder.ip('me')
        print(g.latlng[0])
        print(g.latlng[1])
    except:
        print("Done")
    connection=mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    cursor = connection.cursor()
    sq_query="select count(*) from userdata"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    rcount = int(data[0][0])
    print(rcount, flush=True)

###########



    sq_query="select count(distinct Vendor) from bikedata"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    regcount = int(data[0][0])
    print(regcount, flush=True)

    sq_query="select count(distinct Dated) from bikedata"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    ccount = int(data[0][0])
    print(ccount, flush=True)

    sq_query="select count(*) from bikedata"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    dscount = int(data[0][0])
    print(dscount, flush=True)






    vcostgraph=[]
    ucostgraph=[]
    rcostgraph=[]
    bcostgraph=[]



    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-01-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])


    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-02-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-03-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-04-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-05-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-06-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-07-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-08-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-09-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-10-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-11-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Vogo' and Dated like '%-12-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    vcostgraph.append(data[0][0])

    print('-----------------------')
    print(vcostgraph)








    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-01-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])


    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-02-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-03-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-04-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-05-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-06-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-07-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-08-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-09-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-10-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-11-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Rapido' and Dated like '%-12-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    rcostgraph.append(data[0][0])

    print('-----------------------')
    print(rcostgraph)










    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-01-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])


    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-02-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-03-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-04-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-05-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-06-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-07-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-08-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-09-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-10-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-11-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Bounce' and Dated like '%-12-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    bcostgraph.append(data[0][0])

    print('-----------------------')
    print(bcostgraph)









    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-01-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])


    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-02-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-03-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-04-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-05-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-06-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-07-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-08-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-09-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-10-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-11-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    sq_query="select Sum(Fare)as aa from dataset where Vendor='Uber' and Dated like '%-12-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    ucostgraph.append(data[0][0])

    print('-----------------------')
    print(ucostgraph)


    
    
    data1=[]

    sq_query="select Count(*) as aa from dataset where Vendor='Vogo' and Dated like '%2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    data1.append(data[0][0])
        

    sq_query="select Count(*) as aa from dataset where Vendor='Rapido' and Dated like '%2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    data1.append(data[0][0])
        

    sq_query="select Count(*) as aa from dataset where Vendor='Bounce' and Dated like '%2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    data1.append(data[0][0])   
        

    sq_query="select Count(*) as aa from dataset where Vendor='Uber' and Dated like '%2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    data1.append(data[0][0])

    
    
    connection.commit() 
    connection.close()
    cursor.close()
    return render_template('adminhome.html',pplcount=rcount,regcount=regcount,ccount=ccount,dscount=dscount,vcostgraph=vcostgraph,rcostgraph=rcostgraph,bcostgraph=bcostgraph,ucostgraph=ucostgraph,data1=data1)


@app.route('/manusers')
def manusers():
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    cursor = connection.cursor()
    sq_query="select * from userdata"
    cursor.execute(sq_query)
    print(sq_query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()        
    return render_template('manusers.html',data=data)

@app.route('/delete')
def delete():    
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    cursor = connection.cursor()
    email=request.args["Email"]
    
    sq_query="delete from userdata where Email='"+email+"'"
    cursor.execute(sq_query)
    connection.commit() 

    sq_query="select * from userdata"
    cursor.execute(sq_query)
    print(sq_query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()        
    return render_template('manusers.html',data=data)    


@app.route('/dataloader')
def dataloader():
    return render_template('dataloader.html')



@app.route('/cleardataset', methods = ['POST'])
def cleardataset():
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    cursor = connection.cursor()
    query="delete from dataset"
    cursor.execute(query)
    connection.commit()      
    connection.close()
    cursor.close()
    return render_template('dataloader.html')



@app.route('/uploadajax', methods = ['POST'])
def upldfile():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
        cursor = connection.cursor()
    
        prod_mas = request.files['prod_mas']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("E:\\Upload\\", filename))

        #csv reader
        fn = os.path.join("E:\\Upload\\", filename)

        # initializing the titles and rows list 
        fields = [] 
        rows = []
        
        with open(fn, 'r') as csvfile:
            # creating a csv reader object 
            csvreader = csv.reader(csvfile)  
  
            # extracting each data row one by one 
            for row in csvreader:
                rows.append(row)
                print(row)

        try:     
            #print(rows[1][1])       
            for row in rows[1:]: 
                # parsing each column of a row
                if row[0][0]!="":                
                    query="";
                    query="insert into dataset values (";
                    for col in row: 
                        query =query+"'"+col+"',"
                    query =query[:-1]
                    query=query+");"
                print("query :"+str(query), flush=True)
                cursor.execute(query)
                connection.commit()
        except:
            print("An exception occurred")
        csvfile.close()
        
        print("Filename :"+str(prod_mas), flush=True)       
        
        
        connection.close()
        cursor.close()
        return render_template('dataloader.html',data="Data loaded successfully")



@app.route('/planning')
def planning():
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    sql_select_Query = "Select * from dataset"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


   
    
    return render_template('planning.html', data=data)




@app.route('/forecast')
def forecast():
    
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    sql_select_Query = "select * from dataset limit 100"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()  
    
    return render_template('forecast.html', data=data)



@app.route('/locdata')
def locdata():
    cloc = request.args['loc']
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    sql_select_Query = "select * from dataset"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()

    opdt=[]
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-01-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    jandata = cursor.fetchall()
    if(len(jandata))>0:
        opdt.append(jandata[0][0])
    else:
        opdt.append(0)

    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-02-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    febdata = cursor.fetchall()
    if(len(febdata))>0:
        opdt.append(febdata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-03-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    mardata = cursor.fetchall()
    if(len(mardata))>0:
        opdt.append(mardata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-04-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    aprdata = cursor.fetchall()
    if(len(aprdata))>0:
        opdt.append(aprdata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-05-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    maydata = cursor.fetchall()
    if(len(maydata))>0:
        opdt.append(maydata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-06-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    jundata = cursor.fetchall()
    if(len(jundata))>0:
        opdt.append(jundata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-07-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    juldata = cursor.fetchall()
    if(len(juldata))>0:
        opdt.append(juldata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-08-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    augdata = cursor.fetchall()
    if(len(augdata))>0:
        opdt.append(augdata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-09-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    sepdata = cursor.fetchall()
    if(len(sepdata))>0:
        opdt.append(sepdata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-10-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    octdata = cursor.fetchall()
    if(len(octdata))>0:
        opdt.append(octdata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-11-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    novdata = cursor.fetchall()
    if(len(novdata))>0:
        opdt.append(novdata[0][0])
    else:
        opdt.append(0)
    sql_select_Query = "select PurQTY from dataset where Item like'%"+cloc+"%' and SalesDate like '%-12-%'"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    decdata = cursor.fetchall()
    if(len(decdata))>0:
        opdt.append(decdata[0][0])
    else:
        opdt.append(0)

    print(opdt)
    connection.close()
    cursor.close()  

    mdf = pd.read_csv('newdata.csv')
    print(mdf)
    for i in range(1,13):
        df=mdf.query("Month=="+str(i))
        print("--------------Month"+str(i)+"-------------------")

        # Calculate the total sales value
        total_sales_value = df['SalesVALUE'].sum()

        # Calculate the percentage contribution of each item to the total sales value
        df['Contribution'] = df['SalesVALUE'] / total_sales_value * 100

        # Sort the items in descending order based on their sales value
        df = df.sort_values('SalesVALUE', ascending=False)

        # Calculate the cumulative percentaage of the sales value
        df['CumulativePercentage'] = df['Contribution'].cumsum()

        # Categorize the items based on their cumulative percentage
        df['Category'] = pd.cut(df['CumulativePercentage'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])

        # Display the ABC analysis
        print(df[['Items', 'SalesVALUE', 'Contribution', 'CumulativePercentage', 'Category']])

    print('-------------------Completed--------------------------')
    print('--------------------------ABC Graph Code-------------------')
    items=mdf.Items.unique()
    salesqty=mdf.groupby('Items').sum().SalesQTY.tolist()
    sales_qty=[]
    for i in range(len(salesqty)):
        sales_qty.append(salesqty[i])
    group_a_items = items[:5]
    group_b_items = items[5:15]
    group_c_items = items[15:25]
    plt.figure(figsize=(10, 6))
    plt.bar(group_a_items, sales_qty[:5], color='green', label='Group A')
    plt.bar(group_b_items, sales_qty[5:15], color='orange', label='Group B')
    plt.bar(group_c_items, sales_qty[15:25], color='red', label='Group C')

    # Customize the graph
    plt.xlabel('Items')
    plt.ylabel('Sales Quantity')
    plt.title('ABC Analysis based on SalesQTY')
    plt.xticks(rotation=90)
    plt.legend()

    # Display the graph
    plt.tight_layout()
    plt.savefig("ABCGraph.png")
    plt.show()


    print('=============ABC Analysis=========================')
    sqty=mdf.groupby('Items').sum().SalesQTY.tolist()
    pqty=mdf.groupby('Items').sum().PurQTY.tolist()
    cqty=mdf.groupby('Items').sum().ClosQTY.tolist()  

    
    product=group_a_items

    # Calculate inventory turnover ratio for each product
    turnover_ratios = []
    product_names = []
    for i  in range(len(group_a_items)):
        OSQ = sqty[i]
        CSQ = pqty[i]
        COGS = cqty[i]
        average_stock = (OSQ + CSQ) / 2
        turnover_ratio = COGS / average_stock
        turnover_ratios.append(turnover_ratio)
        product_names.append(group_a_items[i])

    # Plot the inventory turnover ratios as a line graph
    plt.figure(figsize=(12, 6))
    plt.plot(product_names, turnover_ratios, marker='o')
    plt.xlabel('Product')
    plt.ylabel('Inventory Turnover Ratio')
    plt.title('Inventory Turnover Ratio for Products')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("ABCGraph1.png")
    plt.show()


    from scipy.special import erfinv

    # Given data
    lead_time = 7
    demand_variability = 0.1
    desired_service_level = 0.95
    reorder_points = []

    items=[]
    for i  in range(len(group_a_items)):
        temp=[]
        temp.append(group_a_items[i])
        temp.append(sqty[i])
        temp.append(pqty[i])
        temp.append(cqty[i])
        items.append(tuple(temp))

    # Calculate reorder points and plot the graph
    plt.figure(figsize=(12, 6))

    for item in items:
        item_name, pur_qty, sales_qty, clos_qty = item
        
        # Calculate average daily demand
        avg_daily_demand = sales_qty / 1
        
        # Calculate z-score
        z_score = np.abs(np.round(np.sqrt(2) * erfinv(2 * desired_service_level - 1), 2))
        
        # Calculate standard deviation of demand during lead time
        std_dev_demand_during_lead_time = demand_variability * np.sqrt(lead_time)
        
        # Calculate reorder point
        reorder_point = (avg_daily_demand * lead_time) + (z_score * std_dev_demand_during_lead_time)
        reorder_points.append(reorder_point)
        
        # Plot inventory level over time
        days = np.arange(1, 31)  # Assuming 30 days of inventory
        demand = np.random.normal(avg_daily_demand, demand_variability * avg_daily_demand, len(days))
        inventory_level = np.zeros(len(days))
        inventory_level[0] = clos_qty + reorder_point
        
        for i in range(1, len(days)):
            inventory_level[i] = inventory_level[i-1] - demand[i-1]
            if inventory_level[i] < reorder_point:
                inventory_level[i] += reorder_point
        
        plt.plot(days, inventory_level, label=item_name)
        plt.axhline(reorder_point, color='r', linestyle='--')
        plt.xlabel('Days')
        plt.ylabel('Inventory Level')
        plt.title('Inventory Level over Time')
        plt.legend()
        
        plt.savefig("ABCGraph2.png")
        plt.show()
    print("=======================================================================")
    print("========================Reorder Conclusion==============================")
    print("========================================================================")
    # Conclusion statements for each reorder point
    for i, item in enumerate(items):
        item_name = item[0]
        rp = reorder_points[i]
        print(f"The reorder point for {item_name} is approximately {rp:.2f}.")


    return render_template('forecast.html', data=data,opdt=opdt)









@app.route('/gencluster')
def gencluster():
    ven = request.args['ven']
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    #sql_select_Query = "select * from dataset where Area='"+cloc+"' and Month='"+month+"' and (DYear='2018' or DYear='2019')"
    sql_select_Query = "select Count(*) from dataset where Vendor='"+ven+"' and Dated like '%2019' group by Vendor"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    regCluster=[]
    data = cursor.fetchall()
    regCluster.append(data[0][0])
    regCluster.append(data[0][1])
    print('----------------')
    print(regCluster)


    daycluster=[]



    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-01-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])


    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-02-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])

 
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-03-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-04-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-05-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-06-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-07-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-08-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-09-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-10-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-11-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-12-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])   

    print('----------------')
    print(daycluster)


    sql_select_Query="Select * from dataset ORDER BY Dated LIMIT 100"

    

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()

    connection.close()
    cursor.close()  
    
    return render_template('planning.html', ven=ven,regCluster=regCluster,daycluster=daycluster,data=data)
    







@app.route('/genforecast')
def genforecast():
    ven = request.args['ven']
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    #sql_select_Query = "select * from dataset where Area='"+cloc+"' and Month='"+month+"' and (DYear='2018' or DYear='2019')"
    sql_select_Query = "select Count(*) from dataset where Vendor='"+ven+"' and Dated like '%2019' group by Vendor"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    regCluster=[]
    data = cursor.fetchall()
    try:
        regCluster.append(data[0][0])
        regCluster.append(data[1][0])
    except:
        print('----------------')
    print(regCluster)


    daycluster=[]

    

    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-01-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])


    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-02-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])

 
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-03-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-04-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-05-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-06-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-07-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-08-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-09-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-10-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-11-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-12-2019%' group by Vendor"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    daycluster.append(data[0][0])   

    print('----------------')
    print(daycluster)



    
    

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()

    connection.close()
    cursor.close()


    
    g = geocoder.ip('me')
    print(g.latlng[0])
    print(g.latlng[1])
    print(g)
    
    abc=str(g[0])
    xyz=abc.split(', ')
    print(xyz[0][1:])
    print(xyz[1])
    loc=xyz[0][1:]+", "+xyz[1]
    lons=str(g.latlng[1])
    lons=lons[:4]
    connection = mysql.connector.connect(host='localhost',database='pharmadb',user='root',password='')
    sql_select_Query = "select * from dataset where Dated like '%2019%' and (Pickup_Longitude like '"+lons+"%' or Drop_Longitude like '"+lons+"%') "
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()





    import datetime
    today = datetime.datetime.today()
    stoday=str(today)
    dateval = stoday.split("-")
    print(dateval[1])

    monrides=[]
    
    sq_query="select Count(*)as aa from dataset where Vendor='"+ven+"' and Dated like '%-"+dateval[1]+"-%' and (Pickup_Longitude like '"+lons+"%' or Drop_Longitude like '"+lons+"%') group by Vendor"
    print(sq_query)
    cursor.execute(sq_query)
    datax = cursor.fetchall()
    try:        
        monrides.append(datax[0][0])
        if int(dateval[1])%2==0:
            monrides.append(int(monrides[0]*mon1))
            monrides.append(int(monrides[0]*mon6))
            monrides.append(int(monrides[0]*mon12))
        else:        
            monrides.append(int(monrides[0]*(mon1-1)))
            monrides.append(int(monrides[0]*(mon6-1)))
            monrides.append(int(monrides[0]*(mon12-1)))
    except:
        monrides.append(0)
        monrides.append(0)
        monrides.append(0)
        monrides.append(0)

    print(monrides)
    connection.close()
    cursor.close()  
        
    return render_template('forecast.html', ven=ven,data=data,glat=g.latlng[0],glon=g.latlng[1],curloc=loc,monrides=monrides)
    











    

@app.route('/ABCdata',methods=['GET'])
def procABC():
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    selVal = request.args['selected']
    
    print("Selected Val :"+str(selVal), flush=True)
    sql_select_Query=""

    if(selVal=='All'):
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset"
    else:
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset where Inv_Class='"+selVal+"'"

    
    print("Query :"+str(sql_select_Query), flush=True)

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


    A,B,C=getTilesdata1()
    A1,B1,C1=getTilesdata2()
    AC,BC,CC=getTilesdata3()
    X,Y,Z=getTilesdata4()
    xyzTot=X+Y+Z
    xper=X/xyzTot

    
    AX,AY,AZ,BX,BY,BZ,CX,CY,CZ=getHybridData()
    
    
    xper=xper*100;
    xper=round(xper)
    
    yper=Y/xyzTot
    yper=yper*100;
    yper=round(yper)
    
    zper=Z/xyzTot
    zper=zper*100;
    zper=round(zper)
    
    return render_template('planning.html', data=data,aval=A,bval=B,cval=C,aper=A1,bper=B1,cper=C1,X=X,Y=Y,Z=Z,xper=xper,yper=yper,zper=zper,AX=AX,AY=AY,AZ=AZ,BX=BX,BY=BY,BZ=BZ,CX=CX,CY=CY,CZ=CZ)



@app.route('/XYZdata',methods=['GET'])
def procXYZ():
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    selVal = request.args['selected1']
    
    print("Selected Val :"+str(selVal), flush=True)
    sql_select_Query=""

    if(selVal=='All'):
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset"
    else:
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset where XYZ_Class='"+selVal+"'"

    
    print("Query :"+str(sql_select_Query), flush=True)

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


    A,B,C=getTilesdata1()
    A1,B1,C1=getTilesdata2()
    AC,BC,CC=getTilesdata3()
    X,Y,Z=getTilesdata4()
    xyzTot=X+Y+Z
    xper=X/xyzTot


    
    AX,AY,AZ,BX,BY,BZ,CX,CY,CZ=getHybridData()
    
    xper=xper*100;
    xper=round(xper)
    
    yper=Y/xyzTot
    yper=yper*100;
    yper=round(yper)
    
    zper=Z/xyzTot
    zper=zper*100;
    zper=round(zper)
    
    return render_template('planning.html', data=data,aval=A,bval=B,cval=C,aper=A1,bper=B1,cper=C1,X=X,Y=Y,Z=Z,xper=xper,yper=yper,zper=zper,AX=AX,AY=AY,AZ=AZ,BX=BX,BY=BY,BZ=BZ,CX=CX,CY=CY,CZ=CZ)


@app.route('/HybridData',methods=['GET'])
def procHybrid():
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    selVal = request.args['selected2']
    
    print("Selected Val :"+str(selVal), flush=True)
    sql_select_Query=""

    if(selVal=='All'):
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset"
    else:
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset where CONCAT(Inv_Class,XYZ_Class)='"+selVal+"'"

    
    print("Query :"+str(sql_select_Query), flush=True)

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


    A,B,C=getTilesdata1()
    A1,B1,C1=getTilesdata2()
    AC,BC,CC=getTilesdata3()
    X,Y,Z=getTilesdata4()

    
    AX,AY,AZ,BX,BY,BZ,CX,CY,CZ=getHybridData()
    
    xyzTot=X+Y+Z
    xper=X/xyzTot
    
    xper=xper*100;
    xper=round(xper)
    
    yper=Y/xyzTot
    yper=yper*100;
    yper=round(yper)
    
    zper=Z/xyzTot
    zper=zper*100;
    zper=round(zper)
    
    return render_template('planning.html', data=data,aval=A,bval=B,cval=C,aper=A1,bper=B1,cper=C1,X=X,Y=Y,Z=Z,xper=xper,yper=yper,zper=zper,AX=AX,AY=AY,AZ=AZ,BX=BX,BY=BY,BZ=BZ,CX=CX,CY=CY,CZ=CZ)


def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'], # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )]


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
	



def create_forecastplot(feature):
    
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')   
    #connection = mysql.connector.connect(host='182.50.133.84',database='ascdb',user='ascroot',password='ascroot@123')  
    #sql_select_Query ="Select Prod_Val from category  where Description='Cold & Flu Tablets' order by Month asc"
    #"Select Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Forecasting from dataset where Part_desc='BIOCOOL 100-P 205 Ltrs Barrel' "

    ordered=[]
    consumed=[]
    sql_select_Query ="Select sum(Ordered_qty),sum(Cons_qty) from dataset1 where Mon='M03' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    ordered.append(records[0][0])
    consumed.append(records[0][1])

    
    sql_select_Query ="Select sum(Ordered_qty),sum(Cons_qty) from dataset1 where Mon='M02' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    ordered.append(records[0][0])
    consumed.append(records[0][1])

    
    sql_select_Query ="Select sum(Ordered_qty),sum(Cons_qty) from dataset1 where Mon='M01' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    ordered.append(records[0][0])
    consumed.append(records[0][1])

    
        
    x=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    ordy=[21422,20437,19737,19327,21422,20437,19737,19327,20111,ordered[2],ordered[1],ordered[0]]
    consy=[20422,21437,20737,19827,20422,21437,18737,20327,20221,consumed[2],consumed[1],consumed[0]]
    #x=["Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Forecasting"]
    ##y=[]
    #y=[22,33,44,88,55,66,22,33,44,88,55,66]
	
    #print("Y Axis :"+str(y), flush=True)

    
    ##for r in records:
        #row = cursor.fetchone()
        ##print(r, flush=True)
        ##y.append(int(r[0])*1000)
        
    ##print("Y Axis :"+str(y), flush=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=ordy, mode='lines+markers',   name='lines+markers'))
    fig.add_trace(go.Scatter(x=x, y=consy, mode='lines+markers',   name='lines+markers'))
    #fig.update_layout(title='Order v/s Consumption',width=1000,xaxis_title='Month',yaxis_title='Count')
    #fig.update_layout(plot_bgcolor='rgba(192,192,192,1)',width=1000,xaxis=dict(title='Count'),yaxis=dict(title='Month'),)


    #data=[go.Scatter(x=x, y=y)],layout = go.Layout(xaxis=dict(title='Count'),yaxis=dict(title='Month'))
    ##fig = go.Figure(data=[go.Scatter(x=x, y=y)],layout=go.Layout(plot_bgcolor='rgba(192,192,192,1)',width=1000,xaxis=dict(title='Count'),yaxis=dict(title='Month'),))
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='white',showgrid=True, gridwidth=1, gridcolor='white')
    fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='white',showgrid=True, gridwidth=1, gridcolor='white')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON,ordy,consy


#from dataset where CONCAT(Inv_Class,XYZ_Class)='"+selVal+"'	


def getTilesdata1():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')         
    sql_select_Query = "Select count(*) from cpsoilinfo Group By SoilName"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][0]
    
    print("A Val :"+str(aval), flush=True)

    
    sql_select_Query = "Select count(*) from cpsoilinfo Group By CropInfo"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    bval=records[0][0]
    print("B Val :"+str(bval), flush=True)
    
    
    sql_select_Query = "Select count(*) from cpsoilinfo Group By Location"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    cval=records[0][0]
    print("C Val :"+str(cval), flush=True)



    
    connection.close()
    cursor.close()   

    return aval,bval,cval



def getHybridData():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    
    #from dataset where CONCAT(Inv_Class,XYZ_Class)='"+selVal+"'
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='AX'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    AX=records[0][0]
    

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='AY'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    AY=records[0][0]
    
    
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='AZ'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    AZ=records[0][0]

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='BX'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    BX=records[0][0]
    

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='BY'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    BY=records[0][0]
    
    
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='BZ'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    BZ=records[0][0]


    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='CX'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    CX=records[0][0]
    

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='CY'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    CY=records[0][0]
    
    
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='CZ'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    CZ=records[0][0]
    
   


    
    connection.close()
    cursor.close()   

    return AX,AY,AZ,BX,BY,BZ,CX,CY,CZ



	
def getTilesdata2():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')

    sql_select_Query = "Select count(*) from dataset"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    tval=records[0][0]

    
    sql_select_Query = "Select count(Inv_Class) from dataset where Inv_Class='A'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][0]
    aval=aval/tval
    aval=aval*100;
    aval=round(aval)
    
    print("A % :"+str(aval), flush=True)

    
    sql_select_Query = "Select count(Inv_Class) from dataset where Inv_Class='B'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    bval=records[0][0]
    bval=bval/tval
    bval=bval*100;
    bval=round(bval)
    
    print("B % :"+str(bval), flush=True)
    
    
    sql_select_Query = "Select count(Inv_Class) from dataset where Inv_Class='C'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    cval=records[0][0]
    cval=cval/tval
    cval=cval*100;
    cval=round(cval)
    
    print("C % :"+str(cval), flush=True)



    
    connection.close()
    cursor.close()   

    return aval,bval,cval	
	




	
def getTilesdata3():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    
    sql_select_Query = "Select sum(Grand_Tot) from dataset where Inv_Class='A'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][0]
    aval=round(aval,2)
    
    
    sql_select_Query = "Select sum(Grand_Tot) from dataset where Inv_Class='B'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    bval=records[0][0]
    bval=round(bval,2)
    
    
    
    sql_select_Query = "Select sum(Grand_Tot) from dataset where Inv_Class='C'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    cval=records[0][0]
    cval=round(cval,2)
    
    
    connection.close()
    cursor.close()   

    return aval,bval,cval	
	


def getTilesdata4():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')         
    sql_select_Query = "Select count(XYZ_Class) from dataset where XYZ_Class='X'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    xval=records[0][0]
    

    
    sql_select_Query = "Select count(XYZ_Class) from dataset where XYZ_Class='Y'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    yval=records[0][0]
    
    
    sql_select_Query = "Select count(XYZ_Class) from dataset where XYZ_Class='Z'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    zval=records[0][0]
    
    connection.close()
    cursor.close()   

    return xval,yval,zval



def getdbTilesdata4():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    mdata=[]


    
    sql_select_Query = "Select sum(Total_cost) from dataset1 where Mon='M03' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    mdata.append(records[0][0])
    

    
    sql_select_Query = "Select sum(Total_cost) from dataset1 where Mon='M02' and Qtr='Q9'"   
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    mdata.append(records[0][0])
    
    sql_select_Query = "Select sum(Total_cost) from dataset1 where Mon='M01' and Qtr='Q9'"   
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    mdata.append(records[0][0])
    
    connection.close()
    cursor.close()   
    print("Month Data :"+str(mdata), flush=True)

    return mdata
	

def create_category():        
    #connection = mysql.connector.connect(host='localhost',database='poc_db',user='root',password='')
    connection = mysql.connector.connect(host='182.50.133.84',database='croppreddb',user='ascroot',password='ascroot@123')        
    sql_select_Query = "Select distinct xyz,count(xyz) from datavalues group by xyz order by xyz asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    xval=records[0][1]
    yval=records[1][1]
    zval=records[2][1]
    connection.close()
    cursor.close()
    if feature == 'All':
        labels = ['X','Y','Z']
        values = [xval, yval, zval]
        data=[go.Pie(labels=labels, values=values)]        
    elif feature == 'X':
        labels = ['X']
        values = [xval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'Y':
        labels = ['Y']
        values = [yval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'Z':
        labels = ['Z']
        values = [zval]
        data=[go.Pie(labels=labels, values=values)]
    else:
        labels = ['X','Y','Z']
        values = [xval, yval, zval]
        data=[go.Pie(labels=labels, values=values)] 


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_geography():
    connection = mysql.connector.connect(host='182.50.133.84',database='croppreddb',user='ascroot',password='ascroot@123')   
    sql_select_Query = "Select distinct abc,count(abc) from datavalues group by abc order by abc asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][1]
    bval=records[1][1]
    cval=records[2][1]
    connection.close()
    cursor.close()
    if feature == 'All':
        labels = ['A','B','C']
        values = [aval, bval, cval]
        data=[go.Pie(labels=labels, values=values)]        
    elif feature == 'A':
        labels = ['A']
        values = [aval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'B':
        labels = ['B']
        values = [bval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'C':
        labels = ['C']
        values = [cval]
        data=[go.Pie(labels=labels, values=values)]
    else:
        labels = ['A','B','C']
        values = [aval, bval, cval]
        data=[go.Pie(labels=labels, values=values)] 


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
	

def create_moving(feature):
    connection = mysql.connector.connect(host='182.50.133.84',database='croppreddb',user='ascroot',password='ascroot@123')   
    sql_select_Query = "Select distinct fsn,count(fsn) from datavalues group by fsn order by fsn asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    fval=records[0][1]
    nval=records[1][1]
    sval=records[2][1]
    connection.close()
    cursor.close()
    if feature == 'All':
        labels = ['F','N','S']
        values = [fval, nval, sval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]        
    elif feature == 'F':
        labels = ['F']
        values = [fval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]
    elif feature == 'S':
        labels = ['S']
        values = [sval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]
    elif feature == 'N':
        labels = ['N']
        values = [nval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]
    else:
        labels = ['F','N','S']
        values = [fval, nval, sval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]   


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)




    return graphJSON
	
@app.route('/xyz', methods=['GET', 'POST'])
def change_features1():

    feature = request.args['selected']
    graphJSON= create_xyzplot(feature)




    return graphJSON


@app.route('/forecast', methods=['GET', 'POST'])
def fetchforecast():
    forecasttype = request.args['selected']
    graphJSON,oy,cy= create_forecastplot(forecasttype)
    return graphJSON
	

if __name__ == '__main__':
    UPLOAD_FOLDER = 'D:/Upload'
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
