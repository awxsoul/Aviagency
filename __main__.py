import csv
from flask import Flask, render_template, request
import mysql.connector
from flaskwebgui import FlaskUI
from newpack import manageticket  #module  created
from datetime import date
#--------------------------------------------------------------------#
Aviagency = Flask(__name__)
Avi=FlaskUI(Aviagency)
t=date.today() #getting current date from system
un="0"
des="0"
dep="0"
dat="0"
data=[]
flight1=[]
flight2=[]
Airline1="0"
ETD1="0"
ETA1="0"
Price1=0
Airline2="0"
ETD2="0"
ETA2="0"
Price2=0
aw="0"
ETA="0"
ETD="0"
prc=0
price=0
d=[]
info=[]
phone_number="0"
ticket_available2="0"
ticket_available1="0"
names=[]
ages=[]
genders=[]
#-------------------------------------------------#
def loop1():
    global names,genders,ages,data
    names=tuple(names)
    genders=tuple(genders)
    ages=tuple(ages)
    data = zip(names,genders,ages)
    return tuple(data)
#----------------------------------------------#
@Aviagency.route('/')
def start():
   return render_template("homepage.html")

@Aviagency.route('/Aviagency/home/login')
def homepage():
   return render_template("homepage.html")

@Aviagency.route('/Aviagency/home/signup')
def signup():
   return render_template ("signup.html")

@Aviagency.route('/Aviagency/home/contact')
def contact_h():
   return render_template('contacthome.html')

@Aviagency.route('/Aviagency/home/aboutus')
def aboutus_h():
   return render_template('aboutushome.html')

@Aviagency.route('/Aviagency/home/welcome')
def afterauthen():
   return render_template ("afterauthen.html", n=un)
 
#render cancel page
@Aviagency.route('/Aviagency/home/welcome/cancelticket')
def cancelticket():
   global d
   d=manageticket.get_ticket(un)
   if len(d)==0:
      return render_template('cancel.html',
      notickets=" You have not booked any tickets ")
   else:
      return render_template('cancel.html',info=d)

@Aviagency.route('/Aviagency/home/welcome/bookticket')
def bookticket():
   return render_template ("bookticket.html", t=t )

@Aviagency.route('/Aviagency/home/welcome/bookticket/flg_avail')
def flg_avail():
   return render_template ("flg_avail.html")

@Aviagency.route('/Aviagency/home/welcome/bookticket/flg_avail/bookdetails')
def bookdetails():
   return render_template ("bookdetails.html")

@Aviagency.route('/Avigency/home/welcome/bookedticket')
def bookedticket():
   d=manageticket.get_ticket(un)
   if len(d)==0:
      return render_template('booked.html',
      notickets=" You have not booked any tickets ")
   else:
      return render_template('booked.html',info=d)

@Aviagency.route('/Aviagency/home/welcome/cancelticket')
def cancelticket1():
   d=manageticket.get_ticket(un)
   if len(d)==0:
      return render_template('cancel.html',
      notickets=" You have not booked any tickets ")
   else:
      return render_template('cancel.html',info=d)

@Aviagency.route('/Aviagency/home/welcome/cancelticket2',methods=["POST"])
def cancel__ticket2():
   info=manageticket.get_ticket(un)
   v=request.form.get("cancel")
   x=info[int(v)]
   manageticket.cancelling(x)
   return render_template("cancelpage.html",c=x)

@Aviagency.errorhandler(404)
def page_not_found():
    return render_template('404pg.html')

@Aviagency.route('/Aviagency/contact')
def contact():
   return render_template('contact.html')

@Aviagency.route('/Aviagency/aboutus')
def aboutus():
   return render_template('aboutus.html')
#-------------------------------------------------------------------#
#for login check
@Aviagency.route('/Aviagency/home/login',methods = ['POST'])
def login():
   global un,phone_number
   un=request.form["username"]
   pw=request.form["psw"]

   file=open("login_details.csv","r")
   r=csv.reader(file)

   for row in r:
      if len(row)==0:
            continue
      else:
         if row[0]==un and row[1]==pw:
            phone_number=row[3]
            return render_template("afterauthen.html", n=un)
   else:
      return render_template("error.html")
   global username
   if username!=un:
      username=un 
   file.close() 

#for signup, adding users
@Aviagency.route('/Aviagency/home/signup',methods = ["POST"])
def signupcheck():
   global un,phone_number
   un=request.form["username"]
   em=request.form["email"]
   pw=request.form["psw"]
   pwc=request.form["psw-repeat"]
   phone_number=request.form["ph-no"]
   data=[un,pw,em,phone_number]
   #check password
   if pw!=pwc:
      return render_template("signuperror.html",
      o ="Password incorrect, Try again")
   else:
      #check username
      file2=open("login_details.csv","r")
      r=csv.reader(file2)
      for row in r:
         if len(row)==0:
            continue
         elif len(row)!=0:
            if row[0]==un :
               return render_template("signuperror.html", 
               o ="Username already exist")
      else:
         #write details in csv
         file1=open("login_details.csv","a")
         w=csv.writer(file1)
         w.writerow(data)
         file1.close()
         return render_template("afterauthen.html", n=un)
      file2.close()

@Aviagency.route('/Aviagency/home/welcome/bookticket', methods=["POST"])
def dedp():
   global flight1,flight2,Airline1,ETD1,ETA1,Price1,Airline2,ETD2,ETA2,Price2
   global des,dep,dat,prc1,prc2,aw1,aw2
   global ticket_available2,ticket_available1
   des=request.form.get('Destination')
   dep=request.form.get('Departure')
   dat=request.form.get('date')
   if des==dep:
      return render_template('bookticket.html' ,i="check your departure and destination")
   else:
      flight1,flight2,Airline1,ETD1,ETA1,Price1,Airline2,ETD2,ETA2,Price2=manageticket.choose_time(dep,des)
      ticket_available2,ticket_available1=manageticket.tk_available(des,dep,dat) 
      prc2,prc1,aw1,aw2=Price2,Price1,Airline1,Airline2
      return render_template('flg_avail.html',
      dep=dep,
      des=des,
      date=dat,
      aw1=Airline1,
      ETD1=ETD1,
      ETA1=ETA1,
      prc1=Price1,
      aw2=Airline2,
      ETD2=ETD2,
      ETA2=ETA2,
      prc2=Price2,
      ticket_available1=ticket_available1,
      ticket_available2=ticket_available2)

@Aviagency.route('/Aviagency/home/welcome/bookticket/flg_avail', methods=["POST"])
def seat():
   global ETD,ETA,prc,aw,price,seat
   seat=request.form.get("seats")
   seat=int(seat)
   fl1=request.form.get("b1")
   if fl1=='1': 
      ETD=ETD1
      ETA=ETA1
      prc=prc1
      aw=aw1
   elif fl1=='2':
      ETD=ETD2
      ETA=ETA2
      prc=prc2
      aw=aw2
   else:
      pass
   price=prc*seat  
   return render_template("bookdetails.html", x=seat, )

@Aviagency.route('/Aviagency/home/welcome/bookticket/flg_avail/bookdetails',methods=["POST"])
def details():
   global names,ages,genders,data
   names=request.form.getlist('name')
   ages=request.form.getlist('Age')
   genders=request.form.getlist('Gender')
   manageticket.booking_ticket(names,ages,genders,un,phone_number,dep,des,ETD,ETA,dat,aw)
   data=loop1()
   return render_template('confirmed.html',
   aw=aw,
   des=des,
   dep=dep,
   ETA=ETA,
   ETD=ETD,
   prc=price,
   dat=dat,
   data=data)

#use incase of debugging
#if __name__ == '__main__':
#   Aviagency.run(debug = True)
Avi.run()