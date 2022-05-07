import mysql.connector
#------------------------------------------------------------------------------#  
def choose_time(dep,des):
    conn=mysql.connector.connect(host='localhost', user='root', password='root', database='airways')
    cursor=conn.cursor()
    if conn.is_connected() == False:
      return 'Error connecting to the MySQL Database. Please try again after some time.'
    else:
        try:
            sql_cmd = " select * from schedule where Departure = '{}' and Arrival = '{}'".format(dep,des)
            cursor.execute(sql_cmd)
            Data = cursor.fetchall()
            global flight1,flight2,Airline1,ETD1,ETA1,Price1,Airline2,ETD2,ETA2,Price2
            flight1 = Data[0]
            flight2 = Data[1]
            Airline1 = flight1[0]
            ETD1 = flight1[3]
            ETA1 = flight1[4]
            Price1 = flight1[5]
            Airline2 = flight2[0]
            ETD2 = flight2[3]
            ETA2 = flight2[4]
            Price2 = flight2[5]
            print([flight1,flight2,Airline1,ETD1,ETA1,Price1,Airline2,ETD2,ETA2,Price2])
            return flight1,flight2,Airline1,ETD1,ETA1,Price1,Airline2,ETD2,ETA2,Price2
        except:
            return 'ERROR 404. Please try again.'
    conn.close()
#------------------------------------------------------------------------------#  
def booking_ticket(names,ages,genders,un,phone_number,dep,des,ETD,ETA,dat,aw):
    error_message_main = 'ERROR 404. Please try again.'
    success_message_booking = 'Your ticket has been booked successfully. Thank you for choosing Aviagency. '
    import mysql.connector
    conn=mysql.connector.connect(host='localhost', user='root', password='root', database='airways')
    cursor=conn.cursor()
    name={}
    gender={}
    age={}
    if conn.is_connected() == False:
        return 'Error connecting to the MySQL Database. Please try again after some time.'
    else:
        try:          
            if ticket_available1 == 0:
                print('Sorry the plane is full')
                conn.close()
            elif ticket_available2 == 0:
               print('Sorry the plane is full')
               conn.close()
            else:
                for i in range(0,len(names)):  #loop to find names
                    name['name{0}'.format(i)] = names[i]
                    gender['gender{0}'.format(i)] = genders[i]
                    age['age{0}'.format(i)] = ages[i]
                    sql_cmd2 = "insert into booked_tickets values ('{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}')".format(name['name{0}'.format(i)],un,gender['gender{0}'.format(i)],phone_number,age['age{0}'.format(i)],dep,des,ETD,ETA,dat,aw)
                    cursor.execute(sql_cmd2)
                    conn.commit()
                print(success_message_booking)
                conn.close()
        except: 
            print(error_message_main)
            conn.close()
#------------------------------------------------------------------------------#  
def get_ticket(un):
    global info,d
    info=[]
    import mysql.connector
    conn=mysql.connector.connect(host='localhost', user='root', password='root', database='airways')
    cursor=conn.cursor()
    if conn.is_connected() == False:
        print('error_message_conn')
    else:
        try:
            sql_cmd = "select * from booked_tickets where username = '{}'".format(un)
            cursor.execute(sql_cmd)
            d = cursor.fetchall()
            return d
        except:
            print('error_message_main')
#------------------------------------------------------------------------------#  
def tk_available(des,dep,dat):
    error_message_main = 'ERROR 404. Please try again.'
    error_message_conn = 'Error connecting to the MySQL Database. Please try again after some time.'
    import mysql.connector
    conn=mysql.connector.connect(host='localhost', user='root', password='root', database='airways')
    cursor=conn.cursor()
    if conn.is_connected() == False:
        print(error_message_conn)
    else:
        try:
            global ticket_available2,ticket_available1
            sql_cmd = "select * from booked_tickets where Destination = '{}' and Departure = '{}' and ETA = '{}' and ETD = '{}' and Date = '{}'".format(des,dep,ETA1,ETD1,dat)
            cursor.execute(sql_cmd)
            cursor.fetchall()
            ticket_available1 = 20-cursor.rowcount #ticket_available must be the limit of the booking ticket number only then it will work properly
            sql_cmd1 = "select * from booked_tickets where Destination = '{}' and Departure = '{}' and ETA = '{}' and ETD = '{}' and Date = '{}'".format(des,dep,ETA2,ETD2,dat)
            cursor.execute(sql_cmd1)
            cursor.fetchall()
            ticket_available2 = 20-cursor.rowcount
            conn.close()
            return ticket_available2,ticket_available1
        except:
           print(error_message_main)
           conn.close()
#------------------------------------------------------------------------------#   
def cancelling(b):
    #error_message_main = 'ERROR 404. Please try again.'
    #error_message_conn = 'Error connecting to the MySQL Database. Please try again after some time.'
    success_message_cancel = 'Your ticket has been cancelled successfully. Thank you for choosing Aviagency. '
    import mysql.connector
    conn=mysql.connector.connect(host='localhost', user='root', password='root', database='airways')
    cursor=conn.cursor()
    if conn.is_connected() == False:
        return 'Error connecting to the MySQL Database. Please try again after some time.'
    else:
       #('Dhanya', 'Josh', 'Female', 9442200019, 17, 'Mumbai', 'New Delhi', '21:35', '23:40', datetime.date(2020, 12, 2)
       print(b)
       name=b[0]
       gender=b[2]
       age=b[4]
       dep=b[5]
       des=b[6]
       ETA=b[8]
       ETD=b[7]
       dat=b[9]
       print(name,gender,age,dep,des,ETA,ETD,dat)
       sql_cmd1 = "delete from booked_tickets where Name = '{}' and Gender = '{}' and Age = {} and Departure = '{}' and Destination = '{}' and date = '{}' and ETA = '{}' and ETD = '{}'".format(name,gender,age,dep,des,dat,ETA,ETD)
       cursor.execute(sql_cmd1)
       conn.commit()
       print(success_message_cancel)
       conn.close()
       return True
#------------------------------------------------------------------------------#  