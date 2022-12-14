import feedparser
import re

feedlist=['http://feeds.nytimes.com/nyt/rss/HomePage',
		'http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml',
		'http://rss.cnn.com/rss/edition.rss',
		'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml',
		'http://rssfeeds.usatoday.com/usatoday-NewsTopStories',
		'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=h&num=3&output=rss',
		'http://pheedo.msnbc.msn.com/id/3032091/device/rss',
		'http://feeds.abcnews.com/abcnews/topstories',
		':http://www.npr.org/rss/rss.php?id=1001']

def stripHTML(h):
	p=''
	s=0

	for c in h:
		if c=='<':s=1
		elif c=='>':
			s=0
			p+=' '
		elif s==0:
			p+=c
	return p

def separatewords(text):
	splitter=re.compile('\\W*')
	return [s.lower() for s in splitter.split(text) if len(s)>3]

def getarticlewords():
	allwords={}
	articlewords=[]
	articletitles=[]
	ec=0

	# loop over all feeds
	for feed in feedlist:
		f=feedparser.parse(feed)

		# Now loop over each article
		for e in f.entries:
			# ignore identical
			if e.title in articletitles: continue

			# extract words
			txt=e.title.encode('utf8')+stripHTML(e.description.encode('utf8'))
			words=separatewords(txt)
			articlewords.append({})
			articletitles.append(e.title)

			# word counts
			for word in words:
				allwords.setdefault(word,0)
				allwords[word]+=1
				articlewords[ec].setdefault(word,0)
				articlewords[ec][word]+=1
			ec+=1

	return allwords,articlewords,articletitles

def makematrix(allw,articlew):
	wordvec=[]

	# words which are common, but not *too* common
	for w,c in allw.items():
		if c>2 and c<len(articlew)*0.8:
			wordvec.append(w)
	
	# word matrix
	l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
	return l1,wordvec
		
