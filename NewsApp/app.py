from flask import Flask,render_template,request
from newsapi import NewsApiClient

app=Flask(__name__)

newsapi= NewsApiClient(api_key='c474659cc91c473c8b0ffeb9418bbda3')



@app.route("/",methods=['GET','POST'])
def home():
    if request.method=="POST":
        pass
    else:
        top_headlines=newsapi.get_top_headlines(country='in',language="en")
        print(top_headlines)
        total_results=top_headlines['totalResults']

        total_results = min(total_results, 100)

        all_headlines=newsapi.get_top_headlines(country="in", 
                                                language="en", 
                                                page_size=total_results)['articles']
    return render_template("index.html", all_headlines = all_headlines) 
  
if __name__ == "__main__": 
    app.run(debug = True)

