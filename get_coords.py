import mysql.connector
from geopy.geocoders import Nominatim
from instagram.client import InstagramAPI
import json
import urllib2
import flickr

INSTAGRAM_CLIENT_ID = '5d56eb1e594c420997c394d1dca7fcea'
INSTAGRAM_CLIENT_SECRET = 'd0d78baa1e4e4f4b8af9fd9588379968'

api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,client_secret=INSTAGRAM_CLIENT_SECRET)

cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')

cursor = cnx.cursor()

cursor.execute("""select * from galleries""")

geolocator = Nominatim()

coords = []

for row in cursor:
	try:
		location = geolocator.geocode(row[5]+' NYC')
		coords.append((location.latitude,location.longitude))
	except:
		print 'error'

print coords

for i in coords:
	photos = flickr.photos_search(lat=i[0],lon=i[1],per_page=5,radius=0.25)
	for p in photos:
		str = 'https://farm'+p.farm+'.staticflickr.com/'+p.server+'/'+p.id+'_'+p.secret+'.jpg'
		print str
