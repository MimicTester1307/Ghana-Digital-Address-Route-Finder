from flask import Flask, render_template, escape, request
import requests
from helpers import is_valid_input

app = Flask(__name__)


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    error: str = None
    if request.method == 'POST':
        if is_valid_input(escape(request.form['source-address']), escape(request.form['destination-address'])):
            source_address: str = escape(request.form['source-address'])
            dest_address: str = escape(request.form['destination-address'])
            return '<h1> Source: {} Destination: {} </h1>'.format(source_address, dest_address)
        else:
            error = 'Invalid search input(s)'
    elif request.method == 'GET':
        return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
