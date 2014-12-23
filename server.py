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
from hashlib import sha1
import time, os, json, base64, hmac, urllib
from werkzeug import secure_filename
from datetime import date
import humanize

execfile('../credentials_DO_NOT_PUSH_TO_REMOTE.py')

UPLOAD_FOLDER = './photos/'
ALLOWED_EXTENSIONS = set(['jpg'])

# cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')


geolocator = Nominatim()



app = Flask(__name__, static_url_path='')
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# openings=[]
# cursor = cnx.cursor()
# cursor.execute("""select * from galleries_formatted_5 where start_date > 20141201 order by start_date asc""") 
# t = date.today()
# cutoff = str(t.year) + str(t.month) + str(t.day)
# openings_new = []
# #Get list of JSON openings
# for row in cursor:
#     try:
#         #location = geolocator.geocode(row[5]+' NYC')
#         #lat = location.latitude
#         #long = location.longitude
#                     # "date":humanize.naturalday(datetime.date(row[1][:4], row[1][4:6], row[1][6:])),
#         print row
#         dict = {"artist":row[0],
#         "date": row[1],
#         "start_time": "6:00",
#         "end_time":row[3],
#         "gallery":row[4],
#         "address":row[5],
#         "neighborhood":row[6],
#         "end_date":row[7],
#         "lat":row[8],
#         "long":row[9]
#         }
#         openings.append(dict)
#     except:
#        print 'table row not read'

    #print openings

def get_most_recent_upcoming_events():
    cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')
    cursor = cnx.cursor()
    cursor.execute("""select * from galleries_formatted_5 where start_date > 20141010 order by start_date asc""") 
    t = date.today()
    cutoff = str(t.year) + str(t.month) + str(t.day)
    openings_new = []
    #Get list of JSON openings
    for row in cursor:
        # print row
        try:
            #location = geolocator.geocode(row[5]+' NYC')
            #lat = location.latitude
            #long = location.longitude
                        # "date":humanize.naturalday(datetime.date(row[1][:4], row[1][4:6], row[1][6:])),
            dict = {"artist":row[0],
            "date": row[1],
            "start_time": "6:00",
            "end_time":row[3],
            "gallery":row[4],
            "address":row[5],
            "neighborhood":row[6],
            "end_date":row[7],
            "lat":row[8],
            "long":row[9]
            }
            openings_new.append(dict)
        except:
           print 'table row not read'
    openings = openings_new
    cursor.close()
    cnx.close()
    return openings_new



@app.route('/openings')
def get_openings():
    global openings
    openings = get_most_recent_upcoming_events()
    return(jsonify(result=openings))


@app.route('/')
def index():
    global openings
    openings = get_most_recent_upcoming_events()
    return render_template('index.html', events=openings)


@app.route('/form', methods=['POST', 'GET'])
def form():
    cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')
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
        lat = request.form['lat']
        lng = request.form['lng']

        cursor = cnx.cursor()
        row = [artist,date,start_time,end_time,gallery,address,neighborhood,end_date,lat,lng]
        print row
        stmt = "INSERT INTO galleries_formatted_5 (shows,start_date,start,end,gallery,address,nbhood,end_date,lat,lng) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print stmt
        cursor.execute(stmt,row)
        cnx.commit()
        #Add to DB

        files = ['p1']

        conn = tinys3.Connection(AWS_ACCESS_KEY,AWS_SECRET_KEY,tls=True,endpoint="s3-us-west-1.amazonaws.com")

        url_list = []

        for f in files:
            try:
                file = request.files[f]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    sthree_name = artist.replace(" ", "_") + ".jpg"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], sthree_name))
                    f = open(os.path.join(app.config['UPLOAD_FOLDER'], sthree_name), 'rb')
                    print f
                    conn.upload(os.path.join(app.config['UPLOAD_FOLDER'], sthree_name),f,'galleryhop')
                    tmp = 'https://s3.amazonaws.com/galleryhop/'+sthree_name
                    url_list.append(tmp)
            except:
                print "not a file"

        print url_list

        #add url list to DB
        cursor.close()
        cnx.close()
        return index()
    else:
        return render_template('form.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
