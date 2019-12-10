############################################
# This module is for data processing 
###########################################


import nltk 
from nltk.corpus import stopwords
from collections import defaultdict, Counter
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# remove words that are not meaninggul using
# nltk package
def is_valid_word(word,query):
	stopWords = set(stopwords.words('english'))
	stopWords.add(query)
	alp = [chr(i) for i in range(97,123)]
	alp.extend([chr(i) for i in range(65,91)])
	word = word.lower()
	if word not in stopWords and word[0] in alp:
		return 1
	else:
		return 0

def get_titleTokens(title_list,query):
	all_tokens = []
	for title in title_list:
		tokens = nltk.word_tokenize(title)
		valid_tokens = []
		for each in tokens:
			if is_valid_word(each,query):
				valid_tokens.append(each)
		all_tokens.extend(valid_tokens)
	all_tokens = [x.lower() for x in all_tokens]
	return all_tokens
	# word_freq = nltk.FreqDist(all_tokens)
	# word_freq.plot(num)

def ana_month_trend(data):
	cal_dict = defaultdict(int)
	for each in data:
		date = each[0][0:-3]
		num = each[1]
		cal_dict[date] += num
	month = list(cal_dict.keys())
	num = list(cal_dict.values())
	# print(month,num)
	print(data)
	fig = go.Figure()
	fig.add_trace(go.Scatter(
	    x=month,
	    y=num,
	    connectgaps=True
	))
	fig.write_html('static/trend.html', auto_open=False)

def generate_wordCloud(title_list,query):
	all_words = get_titleTokens(title_list,query)
	text = ' '.join(all_words)
	wordcloud = WordCloud(width=800,height=500,font_path="FontRiffic.ttf",max_font_size=80, max_words=250, background_color="white").generate(text)
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	# plt.show()
	plt.savefig('static/cloud.png')


def ana_word_freq(title_list,query,top=20):
	all_words = get_titleTokens(title_list,query)
	cleaned = []
	for word in all_words:
		if query not in word:
			cleaned.append(word)
	common_words = Counter(cleaned).most_common(top)
	words = [x[0] for x in common_words]
	count = [x[1] for x in common_words]
	fig = go.Figure()
	fig.add_trace(go.Bar(
	    x=words,
	    y=count,
	    marker_color=count,
        textposition='auto'
	))
	fig.write_html('static/word.html', auto_open=False)










