import os

from flask import Flask, render_template, escape, request, session, redirect, url_for
from helpers import is_valid_input, query_ghpost_api, get_location_details
from dotenv import load_dotenv

# application setup
load_dotenv()
API_KEY = os.environ.get('MAPS_API_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)
app.config['MAPS_API_KEY'] = API_KEY
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    error = None

    if request.method == 'GET':
        origin, destination = None, None
        if session.get('source-details'):
            origin = session.get('source-details')[1]
        if session.get('dest_details'):
            destination = session.get('dest_details')[1]
        return render_template('home.html', api_key=API_KEY, origin=origin, destination=destination)
    else:
        if is_valid_input(escape(request.form['source-address'].strip()),
                          escape(request.form['destination-address'].strip())):
            source_input: str = escape(request.form['source-address'])
            dest_input: str = escape(request.form['destination-address'])

            geolocation_data = query_ghpost_api(source_input, dest_input)
            if geolocation_data:
                source_lat, source_long = geolocation_data['source_address']
                dest_lat, dest_long = geolocation_data['destination_address']

                source_details = get_location_details(source_lat, source_long)
                dest_details = get_location_details(dest_lat, dest_long)

                session['source-details'] = source_details
                session['dest_details'] = dest_details

            return redirect(url_for('home'))
        else:
            error = 'Invalid search input(s)'


if __name__ == '__main__':
    app.run(debug=True)
