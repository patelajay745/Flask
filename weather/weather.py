from flask import Flask,render_template,request

import json
import urllib.request

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def weather():
    if request.method =='Post':
        city=request.form['city']
    else:
        city='London,CA'
    
    api ='a2a1e5c51d389f23db1888c87272b729'

    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=' + api).read()

    list_of_data=json.loads(source)

    print(list_of_data)

    # data for variable list_of_data 
    data = { 
        "city":str(list_of_data['name']),
        "country_code": str(list_of_data['sys']['country']), 
        "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                    + str(list_of_data['coord']['lat']), 
        "temp": str(list_of_data['main']['temp']) + ' C', 
        "pressure": str(list_of_data['main']['pressure']), 
        "humidity": str(list_of_data['main']['humidity']), 
    } 
    print(data) 

    return render_template('index.html', data = data) 
  
  
  
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000) 