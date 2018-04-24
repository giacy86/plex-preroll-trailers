from __future__ import unicode_literals
import json
import youtube_dl
import tmdbsimple as tmdb
import os

###################################################################################
#	Settings
###################################################################################

tmdb.API_KEY = "your TMDB API key"
language = "it-IT"
region = "it"
max_trailers = 10						# max number of trailers to download

###################################################################################



youtube_keys = []

def getKey(item):
    return item[1]

movies = tmdb.Movies()

movies.now_playing(page=1, language=language, region=region)

i = 0
for s in movies.results:
	if i == max_trailers:
		break
	print(s['title'], s['id'], s['release_date'], s['popularity'])
	x = tmdb.Movies(s['id'])
	try:
		trailer = x.videos(language='it-IT')
		youtube_keys.append([trailer['results'][0]['key'],s['popularity']])
	except IndexError:
		try:
			trailer = x.videos()
			youtube_keys.append([trailer['results'][0]['key'],s['popularity']])
		except IndexError:
			break
	i = i+1
	

movies.upcoming(language=language, region=region)

j = 0
for s in movies.results:
	if j == max_trailers:
		break
	print(s['title'], s['id'], s['release_date'], s['popularity'])
	x = tmdb.Movies(s['id'])
	try:
		trailer = x.videos(language='it-IT')
		youtube_keys.append([trailer['results'][0]['key'],s['popularity']])
	except IndexError:
		try:
			trailer = x.videos()
			youtube_keys.append([trailer['results'][0]['key'],s['popularity']])
		except IndexError:
			break
	j = j+1

trailers = sorted(youtube_keys, key=getKey, reverse=True)		


trailers_filename = {}	#list with the filename of the trailers
k = 0

for k in range(0,max_trailers):
	ydl_opts = {
		'outtmpl': '%(id)s.%(ext)s',
		'format': 'best[ext=mp4]',
		}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		video=ydl.extract_info('https://www.youtube.com/watch?v='+trailers[k][0], download=True)
		filename=ydl.prepare_filename(video)
		trailers_filename[k+1] = filename

# Write the filename of the trailers into a JSON file
print json.dumps(trailers_filename, ensure_ascii=False, sort_keys=True, indent=4)
with open("preroll_trailers.json", 'w') as f:
	json.dump(trailers_filename, f)
f.close	