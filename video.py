############################################
# This module defines 3 classes
# Author: for each video uploader
# Video: for each video
# VideoExtracter: tool for parsing video urls
############################################


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime as dt 

# Author Object
class Author(object):
	def __init__(self,name,channel,subnum):
		self.name = name
		self.channel = channel
		self.subnum = subnum
		self.convert_subnum()
	def convert_subnum(self):
		try:
			num = self.subnum.strip().split(' ')[0]
			if 'K' in num:
				try:
					self.subnum = float(num[0:-1]) * 1000
				except:
					self.subnum = 0
					print('cant convert subnum:',num)
			elif 'M' in num:
				try:
					self.subnum = float(num[0:-1]) * 1000000
				except:
					self.subnum = 0
					print('cant convert subnum:',num)
			else:
				try:
					self.subnum = float(num)
				except:
					self.subnum = 0
					print('cant convert subnum:',num)
		except:
			self.subnum = 0
			print('cant convert subnum:',self.subnum)


# Video Ectracter:
# parse urls into meaningful values
class VideoExtracter(object):

	XPATHS = {
		'author': '//*[@id="text"]/a',
		'title': '//*[@id="container"]/h1/yt-formatted-string',
		'viewers': '//*[@id="count"]/yt-view-count-renderer/span[1]',
		'duration':'//*[@id="movie_player"]/div[27]/div[2]/div[1]/div/span[3]',
		'date': '//*[@id="date"]/yt-formatted-string',
		'subscribers': '//*[@id="owner-sub-count"]',
		'comments': '//*[@id="count"]/yt-formatted-string',
		'category':'//*[@id="content"]/yt-formatted-string/a',
		'img':'//*[@id="img"]'
	}

	def __init__(self,url):
		self.url = url
		self.parse_url()

	def __str__(self):
		print(self.title)
		# print(self.duration)
		print(self.channel)
		print(self.author)
		print(self.vnums)
		print(self.date)
		print(self.subnum)
		# print(self.comnum)
		# print(self.cate)
		# print(self.port)
		return('-'*20)


	def parse_url(self):
		driver = webdriver.Chrome() 
		driver.get(self.url)
		time.sleep(3)
		try:
			self.title = driver.find_element(By.XPATH, self.XPATHS['title'])\
				.get_attribute('innerHTML')
		except:
			self.title='cant find title'
		
		try:
			self.subnum = driver.find_element(By.XPATH, self.XPATHS['subscribers'])\
				.get_attribute('innerHTML')
		except:
			self.subnum = None
		
		try:
			self.author = driver.find_element(By.XPATH, self.XPATHS['author'])\
				.get_attribute('innerHTML')
		except:
			self.author='cant find author'
		
		try:
			self.channel = driver.find_element(By.XPATH, self.XPATHS['author'])\
				.get_attribute('href')
		except:
			self.channel='cant find channel'

		try:
			self.vnums = driver.find_element(By.XPATH, self.XPATHS['viewers'])\
				.get_attribute('innerHTML')
		except:
			self.vnums = None

		try:
			self.date = driver.find_element(By.XPATH, self.XPATHS['date'])\
				.get_attribute('innerHTML')
			# print(self.date)
		except:
			self.date = None


# Video Object
class Video(object):
	MON = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,\
			'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
	def __init__(self,dict):
		self.dict = dict;
		self.url = dict['url']
		self.title = dict['title']
		self.convert_vnums(dict['vnums'])
		self.convert_date(dict['date'])
		self.author = Author(dict['author'],dict['channel'],dict['subnum'])

	def convert_vnums(self,vnums):
		try:
			num = vnums.split(' ')[0]
			num = num.replace(',','')
			self.vnums = int(num)
			print(self.vnums)
		except:
			print('cant convert subnum:',vnums)
			self.vnums = 0
			

	def convert_date(self,date):
		try:
			date = date.replace(',','')
			date = date.replace('Premiered','').strip()
			dl = date.split(' ')
			dl[0] = str(self.MON[dl[0]])
			date = dl[0]+'-'+dl[1]+'-'+dl[2]
			self.date = dt.datetime.strptime(date,'%m-%d-%Y')
			# print(self.date)
		except:
			self.date = dt.datetime.now()
			print('cant convert date:',date)








		
		
		
		
		

		


