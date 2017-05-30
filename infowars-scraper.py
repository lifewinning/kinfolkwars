from bs4 import BeautifulSoup
import json, os, urllib2

def scrape(f,a):
	headers = { 'User-Agent' : 'Mozilla/5.0' }
	soup = BeautifulSoup(open(f))
	#id, description, price
	td = soup.find_all('table',attrs={"id":"product-attribute-specs-table"})
	itemid = ""		
	if td is None:
		os.remove(f)
		print "not a product page"
	else:
		for t in td:
			th = t.find('th')
	 		if th.getText() == 'SKU':
				d = t.find('td',attrs={"class":"data"})
				itemid = d.getText()
				print itemid
			else:
				print "nope!"
	if itemid == "":
		os.remove(f)
		print "not a product page"
	else:
		desc = soup.find('div', attrs={"class":"tab-content"}).getText()
		price = soup.find('span', attrs={"class": "price"}).getText().strip()
		# get images!
		imgs=[]
		imgdiv = soup.find('div', attrs={"class":"product-media-gallery"})
		img = imgdiv.find_all('img')
		finddir = os.path.exists('./imgs/'+itemid)
		if finddir:
			for i in img: 
				headers = {'User-Agent' : 'Mozilla/5.0'}
				src= i['src']
				filename = src.split('/')[-1]
				imgs.append(filename)
		else:
			newdir = os.mkdir('./imgs/'+itemid)
			for i in img: 
				headers = {'User-Agent' : 'Mozilla/5.0'}
				src= i['src']
				filename = src.split('/')[-1]
				imgs.append(filename)
				file = open('./imgs/'+itemid+'/'+filename, 'w')
				req = urllib2.Request(src, None, headers)
				file.write(urllib2.urlopen(req).read())
				file.close()
			print imgs
		# getting product name/category
		path = soup.find('nav', attrs={"class":"breadcrumbs"})
		name = path.find('li',attrs={"class":"product"}).getText().strip()
		secondary = path.find_all('li')
		if len(secondary) > 2:
			secondary=secondary[2].getText().strip().replace('/n','')
		else:
			secondary="N/A"
		obj = {
			"itemid":itemid,
			"name": name,
			"img": imgs,
			"desc":desc,
			"subcat": secondary,
			"price":price
		}
		print "added "+name
		a.append(obj)


products = ['health-and-wellness','preparedness','infowars-media','gear','specials-clearance','alex-recommends']

store = 'www.infowarsstore.com'
for p in products:
	arr=[]
	for root, dirs, files in os.walk(store+'/'+p):
		j = open('products/'+p+'.json','w')
		for d in dirs:
			for f in os.listdir(os.path.join(root,d)):
				path = os.path.join(root,d,f)
				print path
				scrape(path,arr)
		for f in files:
		 	path = os.path.join(root,f)
		 	if path.endswith('html'):
		 		print path
				scrape(path,arr)
	with j as outfile:
		json.dump(arr,outfile)
	print "finished "+p

