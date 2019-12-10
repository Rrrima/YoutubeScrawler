import unittest
from database import *
from analysis import *
from run import *
from build import *
from tabulate import tabulate

class TestBuild(unittest.TestCase):
	pass

class TestDB(unittest.TestCase):
	def test_timefilter(self):
		start = '2019-11-30'
		end = '2018-11-30'
		result = filter_time(start,end)
		# print(tabulate(result[0:10]))
		self.assertTrue(len(result)>1)
	
	def test_numdate(self):
		start = '2019-11-30'
		end = '2018-11-30'
		result = get_number_by_date(start,end)
		# print(tabulate(result))
		self.assertTrue(len(result)==76)

	def test_ranked_videos(self):
		start = '2019-11-30'
		end = '2018-11-30'
		result = get_ranked_videos('vlog',start,end,10)
		# print(tabulate(result))
		self.assertTrue(len(result)==10)

	def test_popular_authors(self):
		query = 'vlog'
		result = get_popular_authors(query,10)
		print(tabulate(result))
		self.assertTrue(len(result)==10)
		query = 'cook'
		result = get_popular_authors(query,10)
		print(tabulate(result))
		self.assertTrue(len(result)==10)

	def test_title_list(self):
		title_list = get_title_list('cook')
		print(title_list)
		self.assertTrue(len(title_list)>50)

class TestAnalysis(unittest.TestCase):
	def test_monthtrend(self):
		start = '2019-11-30'
		end = '2018-11-30'
		result = get_number_by_date(start,end)
		ana_month_trend(result)

	def test_tokens(self):
		query = 'vlog'
		vlinks = get_links(query)
		# print(vlinks)
		videos = get_videos(vlinks[0:100])
		# print(videos)
		title_list = [v.title for v in videos]
		# print(title_list)
		tokens = get_titleTokens(title_list,query)
		print(tokens)

	def test_wordCloud(self):
		query = 'cook'
		vlinks = get_links(query)
		videos = get_videos(vlinks[0:100])
		title_list = [v.title for v in videos]
		generate_wordCloud(title_list,query)

	def test_wordFreq(self):
		titles = get_title_list('cook')
		ana_word_freq(titles,'cook')


class TestRun(unittest.TestCase):
	pass


if __name__ == "__main__":
	# unittest.main(verbosity=2)
	singletest = unittest.TestSuite()
	singletest.addTest(TestAnalysis('test_wordFreq'))
	# singletest.addTest(TestDB('test_title_list'))
	unittest.TextTestRunner().run(singletest)



