#import requests
from __future__ import unicode_literals
import json
import youtube_dl
import tmdbsimple as tmdb
import os

###################################################################################
#	Settings
###################################################################################

tmdb.API_KEY = "635fa65913bd0eca7a06e6722ca71e1c"
language = "it-IT"						# Pass a ISO 639-1 value to display translated data for the fields that support it.
region = "IT"							# Specify a ISO 3166-1 code to filter release dates. Must be uppercase.
max_trailers = 10						# max number of trailers to download. 
										# NOTE: change this setting to mix_preroll_trailers.py
query_region = "ita"					# a string to append at the query for searching localized trailer. ie: 
							# "<movie name> + trailer + <ita>"

###################################################################################



youtube_keys = []

def getKey(item):
    return item[1]

movies = tmdb.Movies()

# Get movies NOW PLAYING
movies.now_playing(page=1, language=language, region=region)

i = 0
for s in movies.results:
	if i == max_trailers:
		break
	print(s['title'], s['id'], s['release_date'], s['popularity'])
	x = tmdb.Movies(s['id'])
	try:	# if there is a localized trailers into ThMovieDB response
		trailer = x.videos(language='it-IT')
		youtube_keys.append(['https://www.youtube.com/watch?v='+trailer['results'][0]['key'],s['popularity']])
		#print("youtube_keys: ")	# for debug
		#print(youtube_keys)		# for debug
	except IndexError:
		try:
			youtube_keys.append([s['title']+" trailer "+query_region,s['popularity']])
			print("Localized trailer not found. Searching for \""+s['title']+" trailer "+query_region+"\"")
		except IndexError:
			break
	i = i+1
	
# Get movies UPCOMING
movies.upcoming(language=language, region=region)

j = 0
for s in movies.results:
	if j == max_trailers:
		break
	print(s['title'], s['id'], s['release_date'], s['popularity'])
	x = tmdb.Movies(s['id'])
	try:	# if there is a localized trailers into ThMovieDB response
		trailer = x.videos(language='it-IT')
		youtube_keys.append(['https://www.youtube.com/watch?v='+trailer['results'][0]['key'],s['popularity']])
		#print("youtube_keys: ")	# for debug
		#print(youtube_keys)		# for debug
	except IndexError:
		try:
			youtube_keys.append([s['title']+" trailer "+query_region,s['popularity']])
			print("Localized trailer not found. Searching for \""+s['title']+" trailer "+query_region+"\"")
		except IndexError:
			break
	j = j+1

trailers = sorted(youtube_keys, key=getKey, reverse=True)		


trailers_filename = {}	#list with the filename of the trailers
k = 0

for k in range(0,max_trailers):
	filename = 'trailer_'+str(k)+'.mp4'
	ydl_opts = {
		'outtmpl': filename,
		'format': 'best[ext=mp4]',
		'default_search': 'ytsearch1:',
		'restrict-filenames': 'TRUE',
		}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		video=ydl.extract_info(trailers[k][0], download=True)
		#filename=ydl.prepare_filename(video)
		trailers_filename[k+1] = filename
	

# Write the filename of the trailers into a JSON file
print json.dumps(trailers_filename, ensure_ascii=False, sort_keys=True, indent=4)
with open("preroll_trailers.json", 'w') as f:
	json.dump(trailers_filename, f)
f.close	
