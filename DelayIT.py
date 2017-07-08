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
	# load stored info
	accounts = j.loads(open("accounts.json",'r').read())
	posts = j.loads(open("posts.json",'r').read())
	# get current time
	now = d.now().strftime("%Y %m %d %H:%M")

	# loop though all the posts
	for i in range(len(posts)):
		# parse preset post time
		postTime = d.strptime(posts[i]["date"],"%Y %m %d %H:%M")
		postTime = postTime.strftime("%Y %m %d %H:%M")

		# check if the post should go up
		if posts[i]["status"] == "waiting": #and postTime == now:
			# initialize reddit account
			reddit = r.Reddit(
				client_id=accounts[posts[i]["account"]]["id"],
				client_secret=accounts[posts[i]["account"]]["secret"],
				password=accounts[posts[i]["account"]]["pass"],
				user_agent=USER_AGENT,
				usernmae=accounts[posts[i]["account"]]["user"]
				)
			print(reddit.user.me())

			# create a reddit post
			submission = ""
			if posts[i]["link"] != "":
				submission = reddit.subreddit(posts[i]["subreddit"]).submit(
					posts[i]["title"],
					url=posts[i]["link"],
					)
			elif posts[i]["text"] != "":
				submission = reddit.subreddit(posts[i]["subreddit"]).submit(
					posts[i]["title"],
					selftext=posts[i]["text"],
					)

			print(submission)
			# if the submission type is an error
			if type(submission) is PRAWException:
				if type(submission) is ClientException:
					sms("The client failed to post")
				elif type(submission) is APIException:
					sms("Reddit failed to post")
				else:
					sms("Something went wrong")
			# if the submission was a success
			else:
				# adds a flair to the submission if specified
				if posts[i]["flair"] != "":
					choices = submission.flair.choices()
					print(choices)
					template_id = next(
						x for x in choices 
						if x['flair_text_editable']
						)['flair_template_id']
					print(template_id)
					submission.flair.select(
						template_id, 
						'custom value'
						)

				# follow up with a attached comment if specified
				if posts[i]["comment"] != "":
					submission.reply(posts[i]["comment"])

				# change the status in posts.json
				posts[i]["status"] = "posted"
				j.dump(posts, indent=4)
			
				# notify the user about the post
				sms("Your post, " + posts[i]["title"] + ", has been posted to /r/" + posts[i]["subreddit"] + " on " + now + ". Here's a link: " + submission.shortlink)

	k = k+1
	t.sleep(1)
