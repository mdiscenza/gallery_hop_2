import tinys3

execfile('../credentials_DO_NOT_PUSH_TO_REMOTE.py')
conn = tinys3.Connection(AWS_ACCESS_KEY,AWS_SECRET_KEY)

files = ['Jasper_Johns.jpg']

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
