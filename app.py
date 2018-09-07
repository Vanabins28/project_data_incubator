from flask import Flask, render_template, request, redirect
#from six.moves import urllib
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import os
import requests
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

app.vars={}


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/tickerselect',methods=['GET','POST'])
def sel_ticker():
#  app.vars['ticker'] = request.form['Ticker Name']
#  app.vars['time_a'] = request.form['Start Date']
#  app.vars['time_b'] = request.form['End Date']
  return render_template('tickerselect.html')

@app.route('/graph_data',methods=['GET','POST'])
def make_graph():
  ticker = request.form['ticker']
  time_a =  request.form['time_a']
  time_b =  request.form['time_b']
#  base_url="https://www.quandl.com/api/v3/datasets/WIKI/" 
  request_url="https://www.quandl.com/api/v3/datasets/WIKI/"+ticker+".csv"
 
  data=requests.get(request_url)
  open('tempq.csv', 'w').write(data.text)
#  with open('tempq.csv','w') as g:
#      g.writelines(data)
#  df= pd.read_csv('/temp.csv')
  df = pd.read_csv('tempq.csv')
  mask = (df['Date'] > time_a) & (df['Date'] <= time_b)
  dates=np.array([np.datetime64(dx) for dx in df[mask]['Date']])
  ploties=np.array([dx for dx in df[mask]['Open']])

  fig = figure(plot_width=600, plot_height=600,x_axis_type="datetime")
  fig.line(dates,ploties)
#  fig.vbar(x=[1, 2, 3, 4],width=0.5,bottom=0,top=[1.7, 2.2, 4.6, 3.9],color='navy')
  fig.xaxis.axis_label = 'Date'
  fig.yaxis.axis_label = 'Price ($)'
  js_resources = INLINE.render_js()
  css_resources = INLINE.render_css()
  script, div = components(fig)
  html = render_template('graph_data.html',plot_script=script,plot_div=div,js_resources=js_resources,css_resources=css_resources,)
  return encode_utf8(html)
   
   
#  return render_template('graph.html')

#os.system('rm temp.csv')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
#  app.run(port=5000)
#  app.run(port=5000,debug=True)
#  app.run(port=33507)
