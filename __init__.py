from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

# Exercice 2 - Création de la route /contact/
@app.route("/contact/")
def contact():
    return render_template("contact.html")



# Exercice 2 - Création de la route /Tawarano/
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
    
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/histogramme/')
def histogramme():
    return render_template('histogramme.html')

@app.route('/commits/')
def commits():
    return render_template('commits.html')

@app.route('/api/commits_data')
def commits_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    data = response.json()

    # Extraire les minutes des dates de commit
    minute_counter = Counter()
    for commit in data:
        try:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_obj.minute
            minute_counter[minute] += 1
        except (KeyError, ValueError):
            continue

    # Convertir en liste de dicts pour le frontend
    results = [{'minute': k, 'commits': v} for k, v in sorted(minute_counter.items())]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
