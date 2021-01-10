import mysql.connector

'''mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Diana123!!",
  database="loveis"
)'''


mydb = mysql.connector.connect(
  host="us-cdbr-east-02.cleardb.com",
  user="b11088f57988af",
  password="3d241aff",
  database="heroku_e91cf812cc22dfc"
)

print(mydb)


mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE clients (id INT AUTO_INCREMENT PRIMARY KEY, client_name VARCHAR(255), client_likes VARCHAR(255))")
'''
name = input("enter name")
name_likes = input ("who he like")
sql = "INSERT INTO clients (client_name, client_likes) VALUES (%s, %s)"
val = (name, name_likes)
mycursor.execute(sql, val)

mydb.commit()

#print(mycursor.rowcount, "record inserted.")


#mycursor.execute("CREATE DATABASE loveis")
#mycursor.execute("show tables")

#for x in mycursor:
#  print(x)


mycursor.execute("SELECT * FROM clients")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

print("LOOOL")

mycursor.execute("select client_name, GROUP_CONCAT(client_likes) from clients where client_likes in (select client_name from clients) group by client_name")
myresult = mycursor.fetchall()

for x in myresult:
  print(x)

'''
#mycursor.execute("drop TABLE chat_gender")
#mycursor.execute("CREATE TABLE clients_male (id INT AUTO_INCREMENT PRIMARY KEY, gender VARCHAR(255), photo VARCHAR(255), name VARCHAR(255), surname VARCHAR(255), age VARCHAR(255), ru VARCHAR(255),"
 #                "height VARCHAR(255), job VARCHAR(255), income VARCHAR(255), insta VARCHAR(255), about VARCHAR(255), chat_id VARCHAR(255), viewed VARCHAR(255))")
#mycursor.execute("CREATE TABLE clients_female (id INT AUTO_INCREMENT PRIMARY KEY, gender VARCHAR(255), photo VARCHAR(255), name VARCHAR(255), surname VARCHAR(255), age VARCHAR(255), ru VARCHAR(255),"
 #                "height VARCHAR(255), job VARCHAR(255), income VARCHAR(255), insta VARCHAR(255), about VARCHAR(255), chat_id VARCHAR(255), viewed VARCHAR(255))")

#mycursor.execute("CREATE TABLE chat_gender (id INT AUTO_INCREMENT PRIMARY KEY, chat_id VARCHAR(255), gender VARCHAR(255), username VARCHAR(255) )")
#mycursor.execute("show tables")
#for x in mycursor:
 #print(x)


#mycursor.execute("CREATE TABLE likes (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), liked_username VARCHAR(255))")
#mycursor.execute("show tables")
#for x in mycursor:
#  print(x)




def add (gender, photo, age, name, surname, ru, height, job, income, insta, about, chat_id):
    if gender == "Мужчина":
        sql = "INSERT INTO clients_male (gender, photo, name, surname, age, ru, height, job, income, insta, about, chat_id, viewed) " \
              "VALUES (%s, %s,  %s, %s, %s, %s, %s, %s,%s,%s,%s, %s, %s)"
        val = (gender, photo,  name, surname, age, ru, height, job, income, insta, about, chat_id, '0')
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted in male table.")

        #select for check
        mycursor.execute("SELECT * FROM clients_male")
        myresult = mycursor.fetchall()
        for x in myresult:
          print(x)


    elif gender == "Женщина":
        sql = "INSERT INTO clients_female (gender, photo, name, surname, age, ru, height, job, income, insta, about, chat_id, viewed) " \
              "VALUES (%s, %s,  %s, %s, %s, %s, %s, %s,%s,%s,%s, %s, %s)"
        val = (gender, photo,  name, surname, age, ru, height, job, income, insta, about, chat_id, '0')
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted in female table.")

        #select for checking
        mycursor.execute("SELECT * FROM clients_female")
        myresult = mycursor.fetchall()
        for x in myresult:
          print(x)

def add_chat_gender(chat_id, gender, username):
        sql = "INSERT INTO chat_gender (chat_id, gender, username) VALUES (%s, %s, %s)"
        val = (chat_id, gender, username)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted in chat_gender table.")

        #mycursor.execute("SELECT * FROM chat_gender")
        #myresult = mycursor.fetchall()
        #for x in myresult:
        #  print(x)


def show_parthers(chat_id):
    sql = "SELECT gender FROM chat_gender WHERE chat_id=%s" % (chat_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    parthers=[]
    for x in myresult:
        if x[0]=="Женщина":
            sql = "SELECT * FROM clients_male"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for male in myresult:
                parthers.append(male)
        elif x[0] == "Мужчина":
            sql = "SELECT * FROM clients_female"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for female in myresult:
                parthers.append(female)
    return parthers

def show_parthers_male():
    parthers=[]
    sql = "select * from clients_male"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for male in myresult:
        parthers.append(male)
    return parthers
print(show_parthers_male())

def show_parthers_female():
    parthers=[]
    sql = "select * from clients_female"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for male in myresult:
        parthers.append(male)
    return parthers


def like (username, liked_username):
        sql = "INSERT INTO likes (username, liked_username) " \
              "VALUES (%s, %s)"
        val = (username, liked_username)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted in like table.")

        mycursor.execute("select * from likes")
        print("who liked who")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

#print(like("diana", "alex"))

def send_liked_message_female(username):
    sql = "SELECT chat_id FROM clients_female WHERE name='%s'"%(username)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    result=[]

    for x in myresult:
        print("hello", x)

    return x


def send_liked_message_male(username):
    sql = "SELECT chat_id FROM clients_male WHERE name='%s'"%(username)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    result=[]

    for x in myresult:
        print("hello", x)
    return x

def get_username_by_chat_id(chat_id):
    print("chat id from database", chat_id)
    sql = "SELECT username FROM chat_gender WHERE chat_id='%s' " % (chat_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print("username to send", x)
    return x

#print(get_username_by_chat_id(426352620))

def match (username):
    sql = "SELECT username, GROUP_CONCAT(liked_username) from likes where username='%s' AND liked_username in (SELECT username from likes) group by username"%(username)

    #sql = "select * from likes where username='%s'"%(username)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    result=[]

    for x in myresult:
        print(x)
        result.append(x)

    return result

#print(match("Diana"))[0]


