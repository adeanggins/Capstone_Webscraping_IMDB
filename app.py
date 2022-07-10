from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'lister-list'})
movie_name = table.find_all('h3', attrs={'class':'lister-item-header'})
imdb_rating = table.find_all('div', attrs={'class':'inline-block ratings-imdb-rating'})
metascore_rating=table.find_all('div', attrs={'class':'ratings-bar'})
imdb_votes=table.find_all('p', attrs={'class':'sort-num_votes-visible'})

row_length = len(movie_name)

#initiating a list
movie_list = []
imdb_rating_list = []
metascore_list=[]
vote_list = [] 

for i in range(row_length):
#insert the scrapping process here
    movie_list.append(movie_name[i].find('a').text)
    imdb_rating_list.append(imdb_rating[i].find('strong').text)
    try:
        metascore_list.append(metascore_rating[i].find('div', attrs={'class':'inline-block ratings-metascore'}).find('span').text.strip())
    except:
        metascore_list.append('0')
    vote_list.append(imdb_votes[i].find('span', attrs={'name':'nv'}).text.replace(',','')) 

#change into dataframe
df = pd.DataFrame({'Movie_Name':movie_list,
                   'IMDB_Rating':imdb_rating_list,
                   'Metascore':metascore_list,
                   'Votes':vote_list,
                  })

#insert data wrangling here
df[['Metascore','Votes']]=df[['Metascore','Votes']].astype('int64')
df['IMDB_Rating']=df['IMDB_Rating'].astype('float64')
data = df.head(7).copy()

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["IMDB_Rating"].mean().round(2)}' #be careful with the " and '
	card_data1 = f'{int(data["Votes"].mean().round(0))}' #be careful with the " and '
	card_data2 = f'{int(data["Metascore"].mean().round(0))}' #be careful with the " and '

	# generate plot Movie Name vs IMDB Rating
	ax = data[['Movie_Name','IMDB_Rating']].sort_values(by='IMDB_Rating',ascending=False).plot(x='Movie_Name',kind='bar',color='c', rot=0, figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt. xlabel('Movie Name', fontsize=20)
	plt. ylabel('IMDB Rating', fontsize=20)
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# generate plot Movie Name vs IMDB Votes
	ax = data[['Movie_Name','Votes']].sort_values(by='Votes',ascending=False).plot(x='Movie_Name',kind='bar',color='r', rot=0, figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt. xlabel('Movie Name', fontsize=20)
	plt. ylabel('IMDB Votes', fontsize=20)
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result1 = str(figdata_png)[2:-1]

	# generate plot Movie Name vs Metascore
	ax = data[['Movie_Name','Metascore']].sort_values(by='Metascore',ascending=False).plot(x='Movie_Name',kind='bar',color='seagreen', rot=0, figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt. xlabel('Movie Name', fontsize=20)
	plt. ylabel('Metascore', fontsize=20)
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result2 = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data,
		card_data1 = card_data1,
		card_data2 = card_data2, 
		plot_result=plot_result,
		plot_result1=plot_result1,
		plot_result2=plot_result2
		)


if __name__ == "__main__": 
    app.run(debug=True)