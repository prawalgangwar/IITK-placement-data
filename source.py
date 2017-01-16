#!/usr/bin/env python
import urllib
import string
import json
import subprocess
import os
from bs4 import BeautifulSoup
from time import sleep
from requests import session 

#after login : http://placement.iitk.ac.in/pas/student
#before login : http://placement.iitk.ac.in/pas/login
#in source action: /pas/userlogin_sessions

url = 'http://placement.iitk.ac.in/pas/login'

with session() as c:
	html = c.get(url)
	soup = BeautifulSoup(html.content)
	csrftoken  = soup.find("input")['value']
	print (csrftoken)
	
	payload = {
	'action' : 'login',
	'authenticity_token': csrftoken,
	'userlogin_session[login]': '<username>',
	'userlogin_session[password]': '<password>'
	}
		
	c.post('http://placement.iitk.ac.in/pas/userlogin_sessions', data = payload, headers= {"Referer": "http://placement.iitk.ac.in"})
	page = c.get('http://placement.iitk.ac.in/pas/')
	page = c.get('http://placement.iitk.ac.in/pas/student')
	page = c.get('http://placement.iitk.ac.in/student/company_profiles')
#	print page.content

	soup = BeautifulSoup(page.content)
	companies = soup.find_all("a")
	print (len(companies))
	i = 0;
	for company in companies:
		print (i)
		i = i+1
		if i>10:
			com_name = company.string	
			com_link = 'http://placement.iitk.ac.in' + company['href']
			print (com_link)
			page = c.get(com_link)
			if not os.path.exists(os.path.dirname('Companies/'+ com_name + '.html')):
   				os.makedirs(os.path.dirname('Companies/'+ com_name + '.html' ))
			file = open('Companies/'+ com_name + '.html', 'w')
			file.write(page.content)
			file.close()
			
