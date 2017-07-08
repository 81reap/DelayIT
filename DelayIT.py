#!/usr/bin/env python

# imports										------------------------
import praw as r
import json as j
import smtplib as s
import time as t
from datetime import datetime as d

# variables										------------------------
USER_AGENT = "DelayIT - Post Scheduler by /u/Hax0rDoge - v0.1"
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
	# load sms info
	sms = j.loads(open("sms.json",'r').read())

	# contimue if enabled
	if sms["enabled"] == "yes":
		# establish connection and send out msg
		server = s.SMTP(G["url"],G["port"])
		server.starttls()
		server.login(sms["user"],sms["pass"])
		server.sendmail("",str(sms["number"]) + S[sms["service"]],msg)

# inf loop										------------------------
k = 0
while k < 1:
	accounts = j.loads(open("accounts.json",'r').read())
	posts = j.loads(open("posts.json",'r').read())
	now = d.now().strftime("%Y %m %d %H:%M")

	for i in range(len(posts)):
		postTime = d.strptime(posts[i]["date"],"%Y %m %d %H:%M")
		postTime = postTime.strftime("%Y %m %d %H:%M")
		if posts[i]["status"] == "waiting": #and postTime == now:
			reddit = r.Reddit(
				client_id=accounts[posts[i]["account"]]["id"],
				client_secret=accounts[posts[i]["account"]]["secret"],
				password=accounts[posts[i]["account"]]["pass"],
				user_agent=USER_AGENT,
				usernmae=accounts[posts[i]["account"]]["user"]
				)
			print(reddit)
			if 0 == "success":
				posts[i]["status"] = "posted"
				j.dump(posts, indent=4)
	#sms("about to post")

	k = k+1
	t.sleep(1)
