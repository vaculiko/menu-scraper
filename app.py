import json
from json2html import json2html
from flask import Flask, render_template, jsonify

app = Flask(__name__)

with open('./data/202205_Taste_of_india_menu.json', 'r',
          encoding='utf-8') as menu:
    india = json.load(menu)

with open('./data/202205_Na_Purkynce_menu.json', 'r',
          encoding='utf-8') as menu:
    purk = json.load(menu)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html',
                           table_india=json2html.convert(india),
                           table_purk=json2html.convert(purk))


app.run(port=3333)