import json
import random
import os

###################################################################################
#	Settings
###################################################################################

quantity = 3			# number of trailers to concatenate. Only these trailers will be played
max_trailers = 10		# max number of trailers downloadED. 

###################################################################################

trailers = json.load(open('preroll_trailers.json'))
print json.dumps(trailers, ensure_ascii=False, sort_keys=True, indent=4)

selected_trailers = random.sample(xrange(1,max_trailers+1),quantity)
	
print selected_trailers

input_video = []

for x in selected_trailers:
	print trailers[str(x)]
	input_video.append(trailers[str(x)])

with open("selected_trailers.txt", "w") as f:
	for i in input_video:
		str = i.replace("'", "\\'")
		f.write('file \'' + str + '\'' + os.linesep)
f.close