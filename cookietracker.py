#Cookie tracker
#For tracking the number of cookies taken from the jar. Button presses are
#interpreted as cookies. A pause after a set of clicks will group those clicks
#into a visit.
#http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
#https://learn.sparkfun.com/tutorials/raspberry-gpio
#http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
#http://nicomiceli.com/tracking-your-home-with-google-analytics/
#https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide
#threading.Event.wait ?
print("Cookie Tracker! View source for details; press Ctrl+C to exit.")

#Settings
import settings

#Broadcom pin definitions
led_red = 20
button = 22

#External modules
import RPi.GPIO as GPIO
import time
from time import asctime, localtime
import urllib2
from threading import Thread

#Pin setup
GPIO.setmode(GPIO.BCM)
#outputs
GPIO.setup(led_red, GPIO.OUT)
#inputs
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #because it's connected to ground
#GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #if it's connected to V

#initial state
GPIO.output(led_red, GPIO.LOW)

visit_count = 0
cookie_count = 0
cookie_total_count = 0
#cookie_last = 0
timeout_thread_count = 0

#event handler functions
def handleBtnPress(channel):
	global cookie_count, cookie_total_count, timeout_thread_count
	cookie_count = cookie_count + 1
	timeout_thread_count = timeout_thread_count + 1
	#print "Button pressed! "+str(timeout_thread_count)+" timeout thread(s)"
	print "Cookie!"
	cookie_total_count = cookie_total_count + 1
	#cookie_last = time.time() #don't need this maybe
	GPIO.output(led_red, GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(led_red, GPIO.LOW)
	timeout().start()

class timeout(Thread):
	def run(self):
		time.sleep(2)
		global timeout_thread_count, visit_count, cookie_count, cookie_total_count
		timeout_thread_count = timeout_thread_count - 1
		#print "Timeout expire! "+str(timeout_thread_count)+" timeout thread(s)"
		if timeout_thread_count == 0:
			visit_count = visit_count + 1
			#build strings with external variables
			ga_url = "http://www.google-analytics.com/collect?v=1&tid="+settings.ga_tracking_id+"&cid="+settings.ga_client_id+"&t=event&ec="+settings.ga_event_category+"&ea="+settings.ga_event_action+"&el="+settings.ga_event_label+"&ev="+str(cookie_count)
			#print ga_url
			log_line = asctime(localtime())+": Visit "+str(visit_count)+": "+str(cookie_count)+" cookie(s), "+str(cookie_total_count)+" since launch"
			#clear external variables
			cookie_count = 0
			#write to GA
			urllib2.urlopen(ga_url).close
			#write to shell and log
			print log_line
			with open("cookietracker-log", "a") as f:
				f.write(log_line+"\n")

#event handlers
GPIO.add_event_detect(button, GPIO.FALLING, callback=handleBtnPress, bouncetime=300)
#GPIO.remove_event_detect() #for when you need it

#let's go!
try:
	while 1:
		time.sleep(60)
except KeyboardInterrupt:
	print("Keyboard interrupt. Bye bye")
except:
	print("Error")
finally:
	GPIO.cleanup()
