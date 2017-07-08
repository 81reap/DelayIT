#!/usr/bin/env python

# imports										------------------------
import praw as r
import json as j
import smtplib as s
import time as t

# variables										------------------------
G = { # g-mail info
	"url":	"smtp.gmail.com",
	"port":	587
}
S = { # services
	"alltel":	"@sms.alltelwireless.com",
	"at&t":		"@txt.att.net",
	"boost":	"@sms.myboostmobile.com",
	"metro":	"@mymetropcs.com",
	"sprint":	"@messaging.sprintpcs.com",
	"tMoblie":	"@tmomail.net",
	"USCell":	"@email.uscc.net",
	"verizon":	"@vtext.com",
	"virgin":	"@vmobl.com"
}
M = { # months
	1:  'Jan.',
	2:  'Feb.',
	3:  'Mar.',
	4:  'Apr',
	5:  'May',
	6:  'June',
	7:  'July',
	8:  'Aug.',
	9:  'Sept.',
	10: 'Oct.',
	11: 'Nov.',
	12: 'Dec.'
}

# functions										------------------------
# https://alexanderle.com/blog/2011/send-sms-python.html
# https://stackoverflow.com/questions/26852128/smtpauthenticationerror-when-sending-mail-using-gmail-and-python
def sms(msg):
	sms = j.loads(open("sms.json",'r').read())

	if sms["enabled"] == "yes":
		to = str(sms["number"]) + S[sms["service"]]

		print(to)

		server = s.SMTP(G["url"],G["port"])
		server.starttls()
		server.login(sms["user"],sms["pass"])
		server.sendmail("",to,msg)

# inf loop										------------------------
i = 0
while i < 1:
	#accounts = j.loads(open("accounts.json",'r').read())
	posts = j.loads(open("posts.json",'r').read())
	

	#for post in posts:
	#	if post["status"] == "waiting":
	#sms("about to post")
			

	#reddit = r.Reddit(
	#	client_id=,
	#	client_secret='',
	#	password='',
	#	user_agent='',
	#	usernmae=''
	#	)
	i = i+1
	t.sleep(1)







