from os import path
from wordcloud import WordCloud
import operator
from PIL import Image
from wordcloud import WordCloud
import requests
from flask  import Flask, render_template, request
from bs4 import BeautifulSoup
import numpy as np

app = Flask("DayEleven")


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/search")
def search():
  url = request.args.get('url').lower()
  pages = request.args.get('page')
  scrapp(url, pages)
  return render_template("home.html")
  
  

words = []
def scrapp (url, pages) :
  page_num = range(int(pages))
  for page in  page_num:
    page = page+1;
    url_ = url+ str(page)
    if page == 1:
      continue
    url_request = requests.get(url)
    sub_soup = BeautifulSoup(url_request.text, "html.parser")
    titles = sub_soup.find_all("td",{"class","title"})
    i = 0; 
    for title in titles :
      if i<7 :
        i = i+1
        continue
      words.extend(title.find("span").text.split())

  word_counts = {}

  for word in words:
    if word  not in word_counts:
      word_counts[word] = 1
    else :
      word_counts[word] += 1
      
  mask = np.array(Image.open('mask_.png'))


  wc = WordCloud(
    font_path='SDSwaggerTTF.ttf',
    background_color='black',
    mask=mask
  )
  
  wc_img = wc.generate_from_frequencies(word_counts)
  wc.to_file('test.jpg')
  


app.run(host="0.0.0.0")