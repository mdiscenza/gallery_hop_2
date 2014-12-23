""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

import mysql.connector
import tinys3
from geopy.geocoders import Nominatim

cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')

cursor = cnx.cursor()

cursor.execute("""select * from galleries""")

geolocator = Nominatim()

openings = []

#Get list of JSON openings
for row in cursor:
        try:
                location = geolocator.geocode(row[5]+' NYC')
                lat = location.latitude
                long = location.longitude

                dict = {"artist":row[0],
                "date":row[1],
                "start_time":row[2],
                "end_time":row[3],
                "gallery":row[4],
                "address":row[5],
                "neighborhood":row[6],
                "end_date":row[7],
                "lat":lat,
                "long":long
                }

                openings.append(dict)
        except:
                print ''

OPENINGS = []

app = Flask(__name__, static_url_path='')
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/openings')
def get_openings():
    return(jsonify(result=openings))


@app.route('/')
def index(openings=openings):
    print(openings)
    return render_template('index.html', events=openings)


@app.route('/form', methods=['POST', 'GET'])
def form():
    if(request.method == 'POST'):
        #submit to db
        artist = request.form['artist']
        date  = request.form['dp1']
        start_time = request.form['tp1']
        end_time = request.form['tp2']
        gallery = request.form['gallery']
        address = request.form['address']
        neighborhood = request.form['nbhd']
        end_date = request.form['dp2']

        #Add to DB

        files = []
        if('p1' in request.form):
            files.append(request.form['p1'])
        if('p2' in request.form):
            files.append(request.form['p2'])
        if('p3' in request.form):
            files.append(request.form['p3'])


        conn = tinys3.Connection(AWS_ACCESS_KEY,AWS_SECRET_KEY)

        url_list = []

        for f in files:
            curr = open(f)
            try:
                conn.upload(f,curr,'galleryhop')
            except:
                files.remove(f)
        for f in files:
            curr = 'https://s3.amazonaws.com/galleryhop/'+f
            url_list.append(curr)

        print url_list

        #add url list to DB

        return index()
    else:
        return render_template('form.html')


@app.route('/openings/', methods=['POST'])
def opening_create():
    opening = request.get_json()
    opening['id'] = len(OPENINGS)
    OPENINGS.append(opening)
    return _opening_response(opening)


@app.route('/openings/<int:id>')
def opening_read(id):
    opening = _opening_get_or_404(id)
    return _opening_response(opening)


@app.route('/openings/<int:id>', methods=['PUT', 'PATCH'])
def opening_update(id):
    opening = _opening_get_or_404(id)
    updates = request.get_json()
    opening.update(updates)
    return _opening_response(opening)


@app.route('/openings/<int:id>', methods=['DELETE'])
def opening_delete(id):
    opening = _opening_get_or_404(id)
    OPENINGS[id] = None
    return _opening_response(opening)


def _opening_get_or_404(id):
    if not (0 <= id < len(OPENINGS)):
        abort(404)
    opening = OPENINGS[id]
    if opening is None:
        abort(404)
    return opening


def _opening_response(opening):
    return jsonify(**opening)


if __name__ == '__main__':
    app.run(port=8000)
