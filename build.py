from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import ast
from video import Video, VideoExtracter
import json
from analysis import *
from database import *

# init the program, create a cache file 
def get_cache_dict():
	CACHE_FNAME = 'youtube_cache.json'
	try:
		cache_file = open(CACHE_FNAME, 'r',encoding='utf-8')
		cache_contents = cache_file.read()
		CACHE_DICTION = json.loads(cache_contents)
		cache_file.close()
	except:
		CACHE_DICTION = {}
	return CACHE_DICTION

def write_to_cache(key,content):
	CACHE_FNAME = 'youtube_cache.json'
	cache_file = open(CACHE_FNAME, 'r',encoding='utf-8')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

	CACHE_DICTION[key] = content
	dumped_json_cache = json.dumps(CACHE_DICTION,indent=4)
	fw = open(CACHE_FNAME,"w",encoding='utf-8')
	fw.write(dumped_json_cache)
	fw.close()

def get_links(query = 'vlog'):
	CACHE_DICTION = get_cache_dict()
	url = "https://www.youtube.com/results?search_query="+query+"&sp=EgIQAQ%253D%253D"
	if url in CACHE_DICTION:
		print("get data from cache")
	else:
		driver = webdriver.Chrome() 
		driver.get(url)
		pageLen = driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);\
			var lenOfPage=document.documentElement.scrollHeight;\
			return lenOfPage;")
		match = False
		url_list = []
		time_list = []
		while not match:
			lastCount = pageLen
			time.sleep(3)
			pageLen = driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);\
			var lenOfPage=document.documentElement.scrollHeight;\
			return lenOfPage;")
			# print(pageLen)
			user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
			# time_data = driver.find_elements_by_xpath('//*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span')
			for i in user_data:
				url_list.append(i.get_attribute('href'))
				# time_list.append(time_data[i].get_attribute('innerhtml'))
			if lastCount == pageLen:
				match = True
		url_list 
		write_to_cache(key=url,content=url_list)
	url_list = list(set(CACHE_DICTION[url]))
	return url_list
	

def get_videos(vlinks):
	CACHE_DICTION = get_cache_dict()
	vlist = []
	for vlink in vlinks:
		if vlink in CACHE_DICTION:
			video_dict = CACHE_DICTION[vlink]
		else:
			print(vlink)
			video_dict = VideoExtracter(vlink).__dict__
			write_to_cache(key=vlink,content=video_dict)
		vlist.append(Video(video_dict))
	return vlist

def insert_database(query):
	vlinks = get_links(query)
	vlinks = list(set(vlinks))
	video_list = get_videos(vlinks[0:300])
	insert_author_records(video_list)
	insert_video_records(query,video_list)

def cache_query(query):
	vlinks = get_links(query)
	vlinks = list(set(vlinks))
	video_list = get_videos(vlinks)

if __name__ == '__main__':
	# create_dbs()
	insert_database('cook')






