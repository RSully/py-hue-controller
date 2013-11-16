#!/usr/local/bin/python

from phue import Bridge
import threading
import random
import time
import datetime
import json
import urllib2
import sys

def get_ip():
	# hacky one liner
	return json.loads(urllib2.urlopen("http://www.meethue.com/api/nupnp").read())[0]['internalipaddress']

# just get the first bridge we can find
br = Bridge(get_ip())

print 'Connected to bridge:'
print vars(br)

lights = br.get_light_objects()

print 'Got lights:'
print lights


def light_fun(br, light):
	while True:
		# command = {'effect': 'colorloop', 'sat': 255}
		# command = {'effect': 'none', 'sat': 0}

		# command = {'transitiontime': 300, 'on': True, 'bri': bri, 'hue': hue, 'sat': sat}

		# time in ms
		trans = random.randint(300, 1200)

		command = {
			'transitiontime': int(round(trans / 100.0)),
			'on': True,
			'bri': random.randint(50, 255),
			'hue': random.randint(0, 65534),
			'sat': random.randint(20, 252)
		}
		print '%s (%s): %s' % (
			time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), 
			light.light_id, 
			command
		)

		res = br.set_light(light.light_id, command)
		time.sleep((trans / 1000.0) * 1.05)


print 'Caching original light states'
original = {}
for light in lights:
	original[light.light_id] = {
		'hue': light._get('hue'),
		'sat': light._get('sat'),
		'bri': light._get('bri')
	}


print 'Starting threads'
for light in lights:
	print 'Setting up thread for light %s (%d)' % (light.name, light.light_id)

	thread = threading.Thread(target=light_fun, args = (br,light))
	thread.daemon = True
	thread.start()


# Wait until exit
try:
	while True:
		pass
except (KeyboardInterrupt, SystemExit):
	print 'Resetting lights to original HSB'
	for orig in original:
		br.set_light(orig, original[orig])
