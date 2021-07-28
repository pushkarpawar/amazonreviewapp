import pandas as pd
import requests
from bs4 import BeautifulSoup

import warnings
from flask import request,redirect, url_for
warnings.filterwarnings('ignore')


import flask




import collections
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
plt.switch_backend('agg')
from matplotlib.colors import ListedColormap
plt.switch_backend('agg')
import seaborn as sns
import matplotlib.colors as colors
plt.switch_backend('agg')

#from datetime import datetime

import warnings
#from scipy import stats
warnings.filterwarnings('ignore')

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk import sent_tokenize, word_tokenize, pos_tag

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

import string


app = flask.Flask(__name__, template_folder='templates' )
#app.config['UPLOAD_FOLDER'] = PLOT_FOLDER

@app.route('/')
def main():
    return(flask.render_template('opening1.html'))
#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=80)


@app.route('/first',methods = ['GET','POST'])
def general():

    if flask.request.method == 'GET':
        return(flask.render_template('general_search.html'))

    
    if flask.request.method == 'POST':

        reviews = []
        search_query=''

        search_query = request.form.get("search_query")
        search_query = search_query.replace(' ', '+')

        base_url="https://www.amazon.in/s?k="

        url=base_url+search_query


        header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.amazon.in/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'}


        search_response=requests.get(url,headers=header)
        search_response.status_code


        #function to get the content of the page of required query
        #orig search page with all products

        cookie={} # insert request cookies within{}
        def getAmazonSearch(search_query):
            url="https://www.amazon.in/s?k="+search_query
            #print(url)
            page=requests.get(url,headers=header)
            if page.status_code==200:
                return page
            else:
                return "Error"


        #function to get the contents of individual product pages using 'data-asin' number (unique identification number)
        #individual product page

        def Searchasin(asin):
            url="https://www.amazon.in/dp/"+asin
            #print(url)
            page=requests.get(url,cookies=cookie,headers=header)
            if page.status_code==200:
                return page
            else:
                return "Error"


        #function to pass on the link of 'see all reviews' and extract the content
        #review page

        def Searchreviews(review_link):
            url="https://www.amazon.in"+review_link
            #print(url)
            page=requests.get(url,cookies=cookie,headers=header)
            if page.status_code==200:
                return page
            else:
                return "Error"




        #EXTRACT ASIN
        data_asin=[]
        response=getAmazonSearch(search_query)
        soup=BeautifulSoup(response.content)
        for i in soup.findAll("div",{'class':["sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20","s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"]}):
            data_asin.append(i['data-asin'])


        #extract price & avg rating
        price=[]
        average_rating=[]
        for i in range(len(data_asin)):
            response=Searchasin(data_asin[i])
    
            soup=BeautifulSoup(response.content)
    
            h1=0
            for l in soup.findAll("span",{'data-hook':"rating-out-of-text"}):
                h1=l.text
                h1=h1[:h1.index(' ')]
                h1=float(h1)
                #average_rating.append(l.text)
            average_rating.append(h1)


            h2=0
            for l in soup.findAll("span",{'id':["priceblock_ourprice","priceblock_dealprice"]}):
                h2=l.text
                h2=h2.replace(',','')
                h2=h2[1:h2.index('.')]
                h2=float(h2)
                #price.append("₹"+l.text[2:])
            price.append(h2)



        #EXTRACT PRODUCT NAME

        product_name=[]
        response=getAmazonSearch(search_query)
        soup=BeautifulSoup(response.content)
        for i in soup.findAll("span",{'class':["a-size-medium a-color-base a-text-normal","a-size-base-plus a-color-base a-text-normal"]}):
            product_name.append(i.text)


        #make length of all equal
        data_asin1=[]
        product_name1=[]
        price1=[]
        average_rating1=[]

        for i in range(len(data_asin)):
            if(data_asin[i]=='0' or product_name[i]=='0' or price[i]==0 or average_rating[i]==0):
                o=0
            else:
                data_asin1.append(data_asin[i])
                product_name1.append(product_name[i])
                price1.append(price[i])
                average_rating1.append(average_rating[i])


        #EXTRACT SEE ALL REVIEW LINK

        link=[]
        data_asin2=[]
        product_name2=[]
        price2=[]
        average_rating2=[]

        for i in range(len(data_asin1)):
            response=Searchasin(data_asin1[i])
            soup=BeautifulSoup(response.content)

            for l in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
                if(l['href']):         #choose only those products whose see all reviews option is available
                    link.append(l['href'])
                    data_asin2.append(data_asin1[i])
                    product_name2.append(product_name1[i])
                    price2.append(price1[i])
                    average_rating2.append(average_rating1[i])


        link1=[]
        [link1.append(x) for x in link if x not in link1]


        data_asin3=[]
        product_name3=[]
        price3=[]
        average_rating3=[]
        k=1

        for i in range (len(data_asin2)):
            c=data_asin2[i]
            k=1
            for j in range (i+1,len(data_asin2)):
                if(c==data_asin2[j]):
                    k=0
                    break

            if(k==1):
                data_asin3.append(data_asin2[i])
                product_name3.append(product_name2[i])
                price3.append(price2[i])
                average_rating3.append(average_rating2[i])



        reviews=[]
        brand_name= []
        brand_name1= []
        #product_name=[]
        product_name4=[]
        rating=[]
        review_length=[0]
        length1=0
        price4=[]
        average_rating4=[]

        for j in range(len(link1)):
        #for j in range(6):
            for k in range(1,3):
                response=Searchreviews(link1[j]+'&pageNumber='+str(k))
                soup=BeautifulSoup(response.content)

                #for i in soup.findAll("a",{'class':"a-size-base a-link-normal"}):
                    #brand_name.append(i.text)

                #for i in soup.findAll("a",{'data-hook':"product-link"}):
                    #product_name.append(i.text)

                for i in soup.findAll("span",{'data-hook':"review-body"}):
                    reviews.append(i.text)
                    price4.append(price3[j])
                    product_name4.append(product_name3[j])
                    average_rating4.append(average_rating3[j])

                    pos = link1[j].index('-')
                    brand_name1.append(link1[j][1:pos])
            
            
                    #pos1 = link[j].index('/',1)
                    #product_name1.append(link[j][1:pos1])

                review_length.append(len(reviews))

                #for h in range(review_length[j+1]-review_length[j]):
                    #product_name1.append(product_name[j])
                    #brand_name1.append(brand_name[j])

                for i in soup.findAll("i",{'data-hook':["review-star-rating","cmps-review-star-rating"]}):
                    if(i.text):
                        rating.append(i.text)

           


        rating1=[]
        average_rating5=[]
        for i in range(len(rating)):
            rating1.append(int(rating[i][0]))
            average_rating5.append(average_rating4[i])


        rev={'Brand':brand_name1,'Product':product_name4,'Price':price4,'Average Rating':average_rating5,'Reviews':reviews,'Review Rating':rating1}

        review_data=pd.DataFrame.from_dict(rev)
        pd.set_option('max_colwidth',800)

        
        
        review_data['Brand'] = review_data['Brand'].str.upper()
        review_data['Product'] = review_data['Product'].str.upper()

        def sentiment(n):
            if n>2:
                #return 1
                return 'Positive'
            else:
                #return 0
                return 'Negative'
            #return 1 if n >= 3 return 0 elif n==3 else 0
        review_data['Sentiment'] = review_data['Review Rating'].apply(sentiment)

        reviews = review_data.head()

        #Most common rating in reviews.

        plt.figure(figsize=(11,6))
        sns.countplot(review_data['Review Rating'])
        #review_data['rating'].value_counts().sort_index().plot(kind='bar')
        plt.title('Distribution of Rating')
        plt.xlabel('Rating')
        plt.ylabel('Number of Reviews')
        #plt.savefig(/usr/src/app/\\templates\\rating_distribution.png')
        plt.savefig('./static/rating_distribution.png')


            


        if(review_data.Brand.nunique() > 2):

            #Most reviewed brand
            plt.figure(figsize=(11,6))
            sns.countplot(y="Brand", data=review_data, order=review_data['Brand'].value_counts().iloc[:10].index, palette="Wistia_r")
            plt.title('Distribution of Brands')
            plt.ylabel('Brands')
            plt.xlabel('Number of Reviews')
            plt.savefig('./static/brand_distribution.png')
            plt.close()

        else:

            #Most reviewed product
            plt.figure(figsize=(11,6))
            sns.countplot(y="Product", data=review_data, order=review_data['Product'].value_counts().iloc[:10].index, palette="Wistia_r")
            plt.title('Distribution of Brands')
            plt.ylabel('Product Name')
            plt.xlabel('Number of Reviews')
            plt.savefig('./static/brand_distribution.png')
            plt.close()


        #Price Distribution
        plt.figure(figsize=(11,6))
        plt.title('Price Distribution')
        x=review_data['Price']
        sns.distplot(x, bins='auto', kde=False, color='g')
        plt.ylabel('No of Products')
        plt.xlabel('Price (₹)')
        plt.savefig('./static/price_distribution.png')
        


        if(review_data.Brand.nunique() > 2):

            #Highest avg_rating
            plt.figure(figsize=(11,6))
            x=review_data.nlargest(len(review_data), ['Average Rating'])
            plt.barh(x['Brand'],x['Average Rating'],color='navajowhite')
            sns.barplot(y="Brand", x="Average Rating", data=review_data, palette="cool_r")
            #plt.xticks(rotation=90)
            plt.ylabel('Brand Name')
            plt.xlabel('Rating')
            plt.title('Average Ratings of Brands')
            plt.savefig('./static/avgrating_brands.png')

        else:
            
            #Highest avg_rating
            plt.figure(figsize=(11,6))
            x=review_data.nlargest(len(review_data), ['Average Rating'])
            plt.barh(x['Product'],x['Average Rating'],color='navajowhite')
            sns.barplot(y="Product", x="Average Rating", data=review_data, palette="cool_r")
            #plt.xticks(rotation=90)
            plt.ylabel('Product Name')
            plt.xlabel('Rating')
            plt.title('Average Ratings of Products')
            plt.savefig('./static/avgrating_brands.png')
        

   
        if(review_data.Brand.nunique() > 2):

            #Sentiment
            plt.figure(figsize=(11,6))
            sns.countplot(y="Brand", data=review_data,hue="Sentiment", order=review_data['Brand'].value_counts().iloc[:10].index, palette="Reds_r")
            plt.title('Sentiments of Brands')
            plt.ylabel('Brands')
            plt.xlabel('Number of Reviews')
            plt.savefig('./static/sentiment.png')

        else:

            #Sentiment
            plt.figure(figsize=(11,6))
            sns.countplot(y="Product", data=review_data,hue="Sentiment", order=review_data['Product'].value_counts().iloc[:10].index, palette="Reds_r")
            plt.title('Sentiments of Brands')
            plt.ylabel('Product')
            plt.xlabel('Number of Reviews')
            plt.savefig('./static/sentiment.png')


        review_data['Review'] = review_data['Reviews'].str.lower()
        all_reviews = review_data['Reviews'].str.split(' ')
        all_reviews_cleaned = []

        for text in all_reviews:
            text = [x.strip(string.punctuation) for x in text]
            all_reviews_cleaned.append(text)

        text_review = [" ".join(text) for text in all_reviews_cleaned]
        final_text_review = " ".join(text_review)
        
        wordcloud_spam = WordCloud(background_color="white").generate(final_text_review)
        plt.figure(figsize = (11,6))
        plt.imshow(wordcloud_spam, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most common words appearing in the reviews')
        plt.savefig('./static/word_cloud.png')


        def cleanText(raw_text, remove_stopwords=True, stemming=False, split_text=False):
    
    
            #text = BeautifulSoup(raw_text, 'lxml').get_text()  #remove html
            letters_only = re.sub("[^a-zA-Z]", " ", raw_text)  # remove non-character
            words = letters_only.lower().split() # convert to lower case
            if remove_stopwords: # remove stopword
                stops = set(stopwords.words("english"))
                words = [w for w in words if not w in stops]

            if stemming==True: # stemming
                stemmer = PorterStemmer()
                #stemmer = SnowballStemmer('english')
                words = [stemmer.stem(w) for w in words]

            if split_text==True:  # split text
                return (words)

            return( " ".join(words))


        X_train, X_test, y_train, y_test = train_test_split(review_data['Reviews'], review_data['Sentiment'], test_size=0.2, random_state=0)

        # Preprocess text data in training set and validation set
        X_train_cleaned = []
        X_test_cleaned = []

        for d in X_train:
            X_train_cleaned.append(cleanText(d))

        for d in X_test:
            X_test_cleaned.append(cleanText(d))


        tfid = TfidfVectorizer() 
        tf_xtr = tfid.fit_transform(X_train)
        tf_xte = tfid.transform(X_test)
        model_tf = LogisticRegression()
        model_tf.fit(tf_xtr, y_train)
        feature_names = np.array(tfid.get_feature_names())
        sorted_coef_index = model_tf.coef_[0].argsort()

        negative = feature_names[sorted_coef_index[:30]].tolist()
        positive = feature_names[sorted_coef_index[:-31:-1]].tolist()

        #text_review = [" ".join(text) for text in negative]
        final_text_review = " ".join(positive)

                       
        wordcloud_spam = WordCloud(max_font_size=50, background_color="white").generate(final_text_review)
        plt.figure(figsize = (11,6))
        plt.imshow(wordcloud_spam, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most common words appearing in positive reviews')
        plt.savefig('./static/positive.png')

        final_text_review = " ".join(negative)

                      
        wordcloud_spam = WordCloud(max_font_size=50, background_color="white").generate(final_text_review)
        plt.figure(figsize = (11,6))
        plt.imshow(wordcloud_spam, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most common words appearing in negative reviews')
        plt.savefig('./static/negative.png')

            
        
        #reviews = data.to_dict()
        reviews = reviews.values.tolist()

                      
        return flask.render_template('general_search.html', search_query = search_query, reviews = reviews, length = len(reviews),negative=negative, positive=positive )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
