import tinys3

conn = tinys3.Connection(AWS_ACCESS_KEY,AWS_SECRET_KEY)

files = ['siegel.jpg']

url_list = []

for f in files:
	curr = open(f)
		conn.upload(f,curr,'galleryhop')

for f in files:
	curr = 'https://s3.amazonaws.com/galleryhop/'+f
	url_list.append(curr)

print url_list
