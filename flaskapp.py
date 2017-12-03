import os
import sys
import boto
import boto.s3
from boto.s3.key import Key
from boto.s3.connection import S3Connection
conn = S3Connection('AKIAJY6MPYPEUU42JFRA', '8zSZiEhDgf6Q7xb3FIdkKtWzNFCvs08a8ZyH6cac')
from flask import Flask,render_template,request, make_response, flash
app = Flask(__name__)
import botocore

bucket_name='sarika92bucket'

try:
	bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
	loginfile=bucket.get_key("login.txt")
	'''bucket_list1=bucket.list()
	for i in bucket_list1:
		name=str(i.key)
		if name=="login.txt":
			loginfile=i.key'''
except:
	'''bucket_list1=bucket.list()
	for i in bucket_list1:
		name=str(i.key)
		if name=="login.txt":
			loginfile=i'''
	loginfile=bucket.get_key("login.txt")


@app.route('/')
def index():
	return render_template('index.html')
	
@app.route("/login", methods=['GET','POST'])
def login():
	cred=""
	if  request.method=='POST':
		uname=request.form['uname']
		passwd=request.form['pass']
		for i in loginfile.read():
			#print i
			#for word in i.split(" "):
			cred=cred+i
			print cred
		credtn=cred.split(" ")
		if uname==credtn[0] and passwd==credtn[1]:
			#flash('Logged in successfully')
			return render_template('index1.html')
		else:
			#flash('Logged failed')
			return render_template('index.html')
				
			
	

	
@app.route("/upfile", methods=['GET','POST'])
def upload():
	if request.method=='POST':
		file_name=request.files['fileup'].filename
		#file = open('/home/ubuntu/flaskapp/hello.txt', 'r+')
		file=request.files['fileup']
		filecontent=request.files['fileup'].read()
		file.seek(0)
		key=file_name
		k=Key(bucket)
		k.key=key
		#if content_type:
		k.set_metadata('Content-Type', "application/exe")
		sent = k.set_contents_from_file(file)
	return 'done'
	
@app.route("/list",methods=['GET','POST'])
def list():
	allfiles=""
	for key in bucket.list():
		allfiles=allfiles+'object: {0}\t'.format(key.name.encode('utf-8'))
	return allfiles
	
@app.route("/deletefile",methods=['GET','POST'])
def delete():
    if request.method=='POST':
		file_name2=request.form['filedelete']
		for key in bucket.list():
			if key.name==file_name2:
				key.delete()
		return "deleted"
		
@app.route("/downfile",methods=['GET','POST'])
def retrieve():
    if request.method=='POST':
		file_name1=request.form['filedown']
		bucket_list=bucket.list()
		
		for i in bucket_list:
			keyString = str(i.key)
			#i.get_contents_to_filename('S:/Sem4/Cloud/newAss3/')
			if file_name1==keyString:
				response=make_response()
				response.headers["Content-Disposition"] = "attachment; filename="+file_name1
				#return make_response()
		return response
			

if __name__ == '__main__':
  app.run()


#http://stackabuse.com/example-upload-a-file-to-aws-s3/
#http://stackoverflow.com/questions/27628053/uploading-and-downloading-files-with-flask
#sftp://ec2-35-160-16-131.us-west-2.compute.amazonaws.com