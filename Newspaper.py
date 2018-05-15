
from requests import get
from bs4 import BeautifulSoup
import smtplib

#define some beginner variables
title_list = []
url_list = []


def read_NYT():
	global title_list
	global url_list
	url = "https://www.nytimes.com"
	website = get(url) 
	website_text = website.text
	
	#parse through the html with beautiful soup
	use_me = BeautifulSoup(website_text, "html.parser")
	list_o_articles = use_me.find_all("h2", class_ = "story-heading")
	
	#time to make the url and title lists
	for article in list_o_articles:
		#title list is made by appending stripped text
		title_list.append(article.get_text().strip())
	#goes into each indices a value and finds the links
	for article in list_o_articles:
		a = article.find_all("a")
		for i in a:
			url_list.append(i.get("href"))
	return title_list

def get_key_words():
	key_words = [] 
	word = "placeholder"
	while word != "":
		word = input("What words do you want to look for: ")
		key_words.append(word)
	key_words = key_words[:len(key_words) - 1]
	return key_words


read_NYT()
key_words = get_key_words()

#NEEDS FIXING
results = []
for i in range(len(title_list)):
	for word in key_words:
			if word in title_list[i]:
				results.append(title_list[i])

#Email stuff!
username = input("Enter your email username: ")
password = input("Enter your email password: ")

server = smtplib.SMTP_SSL("smtp.gmail.com:465")
server.set_debuglevel(False)
server.login(username, password)
message = "\n\n".join(results).replace("\u2019", "'")
#print(message)
server.sendmail("jonas.kolker@gmail.com", username, ("Here are your titles!\n\n" + message))
server.quit()
print("\n\ndone!")

