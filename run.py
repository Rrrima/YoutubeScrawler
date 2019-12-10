from database import *
from analysis import *
from flask import Flask,render_template,request
import time
 
app = Flask(__name__)
# user input variables
query = ""
start = '2019-11-30'
end = '2017-11-30'
top = 10
# inst: author,time,video,word,cloud
def handle_inst(inst):
	if inst == 'author':
		data = get_popular_authors(query,top)
		return data
	elif inst == 'time':
		# print(query,start,end)
		data = get_number_by_date(query,start,end)
		# print(data)
		ana_month_trend(data)
	elif inst == 'video':
		print(query,start,end)
		data = get_ranked_videos(query,start,end,top)
		return data
	elif inst == 'word':
		titles = get_title_list(query)
		ana_word_freq(titles,query)
	elif inst == 'cloud':
		titles = get_title_list(query)
		generate_wordCloud(titles,query)
	else:
		print("please put valid inst!")
# if interact via terminal
def start_prop():
	e = 0
	while not e:
		inst = input("please put inst:")
		if inst == 'exit':
			print("goodbye")
			e = 1
			continue
		else:
			handle_inst(inst)

@app.route('/',methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		global query
		global start
		global end
		try:
			x = request.form['query']
			if x!='':
				query = x
		except:
			pass
		try:
			start = request.form['start']
		except:
			pass
		try:
			end = request.form['end']
		except:
			pass
	return render_template('index.html',query=query,start=start,end=end)

@app.route('/author')
def authorpage():
	data = handle_inst('author')
	return render_template('author.html',data=data)

@app.route('/video')
def videopage():
	print(start,end)
	data = handle_inst('video')
	return render_template('video.html',data=data,start=start,end=end)

@app.route('/word')
def wordpage():
	handle_inst('cloud')
	handle_inst('word')
	return render_template('word.html',query=query)

@app.route('/trend')
def trendpage():
	handle_inst('time')
	return render_template('trend.html',query=query,start=start,end=end)

if __name__ == '__main__':
	app.run(debug=True)
	# start_prop()








	