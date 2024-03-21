from flask import Flask, render_template,request
import pyjokes

app=Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    
    if request.method == "POST":
        action = request.form["action"]
        
        if action == "next":
            joke = pyjokes.get_joke()
            
        
    else:
        joke = pyjokes.get_joke()
        
    return render_template("home.html", joke=joke)

@app.route("/multiplejokes")
def jokes():
    jokes = pyjokes.get_jokes()
    return render_template("jokes.html", jokes=jokes)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
