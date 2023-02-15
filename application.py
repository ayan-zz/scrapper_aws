from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
application = Flask(__name__)
app=application

@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/details", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            link = bs(flipkartPage, "html.parser")
            product_name = link.findAll("div" ,{"class":"_3pLy-c row"})
            product_price = link.findAll("div" ,{"class":"_3tbKJL"})
            product_high=link.findAll("div",{"class":"fMghEO"})
            product_rates=link.findAll("div", {"class":"gUuXy-"})


            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Search_Product, Product, Price, Rating, Highlights \n"
            fw.write(headers)
            detail = []
            for name in product_name:
                try:
                    #names.encode(encoding='utf-8')
                    names=name.div.div.text
                except:
                    logging.info("names")
            for price in product_price:
                try:
                    #prices.encode(encoding='utf-8')
                    prices=price.div.div.text
                except:
                    logging.info("prices")
            for rate in product_rates:
                try:
                    #rating.encode(encoding="utf-8")
                    rating=rate.div.text
                except:
                    logging.info("rating")
            for high in product_high:
                try:
                    #highlights.encode(encoding="utf-8")
                    highlights=high.text
                except:
                    logging.info("highlights")
                mydict={"Search_Product":searchString,"Product":names,"Price":prices, "Rating":rating, "Highlights":highlights}
                detail.append(mydict)
            logging.info("log my final result {}".format(detail))
            return render_template('result.html', detail=detail)
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")

