# Written and developed by Gil Kogan and Lionel Fafchamps
# Throws pairs of random postcodes into google maps and calculates the straight line distance and the walking distance between the two points. Then calculates an average of the ratio of these two number.


import random
import urllib
from googlemaps import GoogleMaps
import json
import math as m
import os
import time
from numpy import *


def distances(start_address,end_address):
	gmaps = GoogleMaps()
	
	base_url = 'http://maps.googleapis.com/maps/api/directions/json?'
	
	travel_mode='mode=walking'
	
	if start_address==end_address:
		return False
	
	start_lat, start_longt = gmaps.address_to_latlng(start_address+', New York, USA')	#Getting the longtitudes and lattitudes of given addresses
	end_lat, end_longt = gmaps.address_to_latlng(end_address+', New York, USA')
	sensor='sensor=false'
	
	test_url=base_url+'&'+travel_mode+'&'+'origin='+str(start_lat)+','+str(start_longt)+'&destination='+str(end_lat)+','+str(end_longt)+'&'+sensor	#Constructs the url to query google maps for walking directions
	print test_url
	
	result = json.load(urllib.urlopen(test_url)) 
	
	met_distance = result['routes'][0]['legs'][0]['distance']['value']	#obtain the walking distance in km
	print 'Metropolitan distance between ', start_address, 'and', end_address , ' is ',met_distance, 'm'
	
	#calculate the straight line distance (over the surface of the Earth) assuming the Earth is a sphere of radius 6378100m
	dlat = m.radians(end_lat-start_lat)
	dlongt = m.radians(end_longt-start_longt)
	
	a = ((m.sin(dlat/2))*(m.sin(dlat/2)))+(m.cos(m.radians(start_lat)) * m.cos(m.radians(end_lat)) * (m.sin(dlongt/2))*(m.sin(dlongt/2)) )
	c = 2 * m.atan2(m.sqrt(a), m.sqrt(1-a))
	d = 6378100 * c
	print 'Whereas line of flight distance is' , d,'m'
	if d == 0 : return False
	rat = met_distance/d
	if rat < 1 : rat = 1
	return rat




#read in a list of postcodes for a given city

f=open('NYC_PC.txt')
a = f.read()
a = a.split(", ")
f.close()

#easy way to get two different points
b=list(a)
random.shuffle(b)

#keeps a record of every attempt without overwriting a file
fout_name_base, fout_name = 'nyc_results','nyc_results.txt'
ver = 1
while os.path.exists(fout_name):
	fout_name = fout_name_base + str(ver)+'.txt'
	ver += 1
outf = file(fout_name, "w")
print 'Writing output to ', outf.name

ratios=[]
for i,v in enumerate(a):
	print 'Pairing ',v,' with ',b[i]
	if v==b[i]: 
		b.append(b[i])
		b.pop(i)
	ratio = distances(v,b[i])
	if ratio == False : 
		print 'American postcodes are retarded'
		time.sleep(1)
		continue
	ratios.append(ratio)
	outf.write(v+',')
	outf.write(b[i]+',')
	outf.write(str(ratio))
	outf.write("\n")
	time.sleep(1)
#print ratios

outf.close()

print 'The average raito is ', average(ratios)
print 'The standard deviation is ', std(ratios)