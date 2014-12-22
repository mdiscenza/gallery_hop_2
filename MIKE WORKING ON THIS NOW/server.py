""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

import mysql.connector
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
        print request.form

        AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
        AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
        S3_BUCKET = "what is the name"
        object_name = request.args.get('s3_object_name')
        mime_type = request.args.get('s3_object_type')
        expires = long(time.time()+10)
        amz_headers = "x-amz-acl:public-read"
        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        signature = urllib.quote_plus(signature.strip())

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)


        return render_template('form.html')
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
