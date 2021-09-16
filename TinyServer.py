import ZODB, ZODB.FileStorage
import persistent
import transaction
import requests
import xmlrpc.client
import time
import datetime
import logging
import inspect


from flask import request

import pika
from flask import Flask
app = Flask(__name__)

#Student class for setting and getting student details
class Student(persistent.Persistent):
    studentName = ''
    lastName = ''
    studentNumber = ''
    #Setter for student first name
    def setStudentName(self, sName):
        self.studentName = sName

    #Getter for student first name    
    def getStudentName(self):
        return self.studentName

    #Setter for student last name
    def setLastName(self, sLastName):
    	self.lastName = sLastName

    #Getter for student last name
    def getLastName(self):
        return self.lastName

    #Setter for student number
    def setStudentNumber(self, sNumber):
        self.studentNumber = sNumber

    #Getter for student number
    def getStudentNumber(self):
        return self.studentNumber

#Function to print hello world when the / URL is called
@app.route("/")
def hello():
	#Log function name that was called
	#log_calls(str(inspect.stack()[0][3]))
	return "Hello World!"


#Function to view records of users
@app.route('/viewrecords')
def view():
	#log_calls(str(inspect.stack()[0][3]))
	#Create object database and open/connect
	storage = ZODB.FileStorage.FileStorage('mydata.fs')
	db = ZODB.DB(storage)
	connection = db.open()
	root = connection.root

	#Return student details
	return root.s1.getStudentName() + '-' + root.s1.getLastName() + '-' + root.s1.getStudentNumber()

#Function to insert name and student number entered into postman or through URL browser
@app.route('/insert')
def login():
	#log_calls(str(inspect.stack()[0][3]))
	firstName = request.args.get('firstname')
	lastName = request.args.get('lastname')
	studentid = request.args.get('studentid')

	#Store in object database
	storage = ZODB.FileStorage.FileStorage('mydata.fs')
	db = ZODB.DB(storage)
	connection = db.open()
	root = connection.root

	#Commit student details to the object database
	root.s1 = Student()
	root.s1.setStudentName(firstName)
	root.s1.setLastName(lastName)
	root.s1.setStudentNumber(studentid)
	transaction.commit()
	connection.close()
	db.close()

	#Log user info
	user_details = 'First Name: ' + firstName + 'Last Name: ' + lastName + 'StudentID: ' + studentid
	log_users(user_details)

	#Return student details
	return firstName + '-' + lastName + '-' + studentid



buffer = ''
def callback(ch, method, properties, body):
	#log_calls(str(inspect.stack()[0][3]))
	global buffer
	buffer = body
	print(" [x] Received %r" % body)

#Function to let the user connect to service and talk with different languages (Python and PHP)
#Uses rabbitmq
@app.route('/read')
def readRabbit():
	#log_calls(str(inspect.stack()[0][3]))
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='hello')
	channel.basic_consume(callback,queue='hello',no_ack=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()
	global buffer
	return buffer


#Function to send back the temperature entered by the user
@app.route("/callClient/<temp>")
def call_client(temp):
	#log_calls(str(inspect.stack()[0][3]))
	content = ''
	if(int(temp) >= 0 and int(temp) <= 10):
		content = 'cold'
	elif(int(temp) >= 11 and int(temp) <= 20):
		content = 'warm'
	else:
		content = str(temp)
	with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy:
		content = str(proxy.is_even(content))
	return content

#Function to send back the current weather
@app.route('/justweather')
def justweather_call():
	#log_calls(str(inspect.stack()[0][3]))

	#Request to get weather from said address
	x = requests.get('http://kylegoslin1.pythonanywhere.com/').json()

	#parsed JSON content
	forecast = x['forecast']
	print(forecast)

	#Return the weather
	return '{forecast:"'+forecast+ '"}'

#Function to update updates.txt text file
@app.route('/updates')
def justupdates_call():
	#log_calls(str(inspect.stack()[0][3]))

	#Open and read updates.txt file
	f = open('updates.txt', 'r')
	x = f.readlines()
	output = '{'
	#print(x)
	print(type(x))
	print(x)
	for item in x:

		output = output + '"line": "'+item+ '",'
	f.close()

	#remove the last trailing comma
	output = output[:-1]
	output = output + '}'
	return output

#Function to send back a pong when a ping is receieved 
@app.route('/ping')
def send_pong():
	#log_calls(str(inspect.stack()[0][3]))
	#Get time and date
	time_stamp = time.time()
	date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
	pong = 'pong ' + date_stamp
	return pong


#Function to create and write who is currently using the service including time stamp
def log_users(userInfo):
	#log_calls(str(inspect.stack()[0][3]))
	time_stamp = time.time()
	date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
	#Create file and log info
	logging.basicConfig(filename='users.log', level=logging.INFO)
	logging.info(userInfo + ' ' + str(date_stamp))


#Function to create and write to log file with the name of whatever function was called
def log_calls(function_name):
	#Get the function name that was called from the stack
	#log_calls(str(inspect.stack()[0][3]))
	time_stamp = time.time()
	date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
	logging.basicConfig(filename='calls.log', level=logging.INFO)
	#Log info
	logging.info('Function Called: ' + function_name + 'Time: ' + str(date_stamp))