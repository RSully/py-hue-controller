#!/usr/local/bin/python

from phue import Bridge
import threading
import random
import time
import datetime

br = Bridge('192.168.11.7')

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
		# print res
		time.sleep((trans / 1000.0) * 1.05)

for light in lights:
	print 'Setting up thread for light'
	print vars(light)

	# light_fun(br, light)
	thread = threading.Thread(target=light_fun, args = (br,light))
	thread.daemon = True
	thread.start()


while True:
	pass
