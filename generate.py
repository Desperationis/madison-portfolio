import json
import os

f = open("./config.json")
confstr = f.read()
f.close()

conf = json.loads(confstr)
artdir = conf['artfolder']
print("generating art for folder: ", artdir)

exts = ['png', 'jpg', 'jpeg']
list1 = os.listdir(artdir)
list2 = []

for f in list1:
	for ext in exts:
		if f.endswith(ext):
			list2.append(f)


def parseFile(f):
	parts = f.split("_")
	if not len(parts) == 4:
		return None
	try:
		data = dict()
		data["id"] = int(parts[0][3:])
		data["dom"] = int(parts[1])
		data["mon"] = int(parts[2])
		data["year"] = int((parts[3].split("."))[0])
		data["filename"] = f

		nfo = artdir + "/" + f.split(".")[0] + ".json"
		try:
			if os.path.isfile(nfo):
				f = open(nfo)
				jsstr = f.read()
				f.close()
				data["info"] = json.loads(jsstr)
		except Exception as e:
			print("failed reading info file: ", nfo, ":", e)
	except Exception as e:
		print("Failed parsing data for: ", f, ":", e)
		return None
	return data

def formEntry(d):
	# Form html for gallery page
	html1 = '<div class="col-sm-6 col-md-4 col-lg-3 item"><a href="https://art.plantmonster.net/pieces/'
	html1 += str(d["id"]) + '.html"'
	html1 += 'data-lightbox="photos"><img class="img-fluid" src="'
	html1 += 'https://plantmonster.net/art/' + d["filename"] + '"></a></div>\n'
	d["html1"] = html1

# Writes the main gallery view HTML document
def writeGalleryPage(data):
	f = open('portfolio.template', 'r')
	html = f.read()
	f.close()

	gallery_html = ""
	for d in data:
		gallery_html += d["html1"]

	html = html.replace('REPLACE_GALLERY', gallery_html)

	f = open('portfolio.html', 'w')
	f.write(html)
	f.close()

# Writes a new HTML document for one specific artwork
def writePiecePage(d):
	fname = 'pieces/' + str(d['id']) + '.html'

	f = open('artwork.template', 'r')
	html = f.read()
	f.close()

	license = '<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.'

	title_extra = ""
	extra_images = ""
	url_prefix = "https://plantmonster.net/art/"

	if 'info' in d:
		desc = d['info']['description'].replace("\n", "</br>")
		html = html.replace('REPLACE_DESCRIPTION', desc)
		if 'extra_images' in d['info']:
			extra = d['info']['extra_images']
			if isinstance(extra, list):
				for img in extra:
					extra_images += '<a href="' + url_prefix + img + '"><img src="' + url_prefix + img + '"/></a>'
		if 'license' in d['info']:
			if d['info']['license'] == "copyleft":
				pass
			elif d['info']['license'] == "copyright":
				license= '<p>Copyright &copy; ' + str(d['year']) + ' Jesse Kaukonen / Farstrider Oy. All rights reserved.</p>'
		if 'title' in d['info']:
			title_extra = d['info']['title']
	else:
		html = html.replace('REPLACE_DESCRIPTION', '')

	html = html.replace('REPLACE_LICENSE', license)
	title_str = 'Art piece #' + str(d["id"])
	if len(title_extra) > 0:
		title_str = title_str + ": " + title_extra

	html = html.replace('REPLACE_TITLE', title_str)
	html = html.replace('REPLACE_DATE', str(d['dom']) + '.' + str(d['mon']) + '.' + str(d['year']))

	link = url_prefix + d['filename']
	html = html.replace('REPLACE_DATA', '<a href="' + link + '"><img src="' + link + '"/></a>')
	html = html.replace('REPLACE_OG_IMAGE', link)
	html = html.replace('REPLACE_EXTRA_IMAGES', extra_images)

	f = open(fname, 'w')
	f.write(html)
	f.close()

parsedFiles = []
for f in list2:
	d = parseFile(f)
	if d != None:
		parsedFiles.append(d)

for f in parsedFiles:
	formEntry(f)

parsedFiles.sort(key=lambda it: it["id"], reverse=True)
writeGalleryPage(parsedFiles)
for d in parsedFiles:
	writePiecePage(d)
