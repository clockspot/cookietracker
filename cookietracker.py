print("Cookie tracker!");

#External modules
import RPi.GPIO as GPIO
import time

#Pin definitions
ledRed = 20
ledGreen = 21
button = 22

#Pin setup
GPIO.setmode(GPIO.BCM)
#outputs
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
#inputs
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #because it's connected to ground
#GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #if it's connected to V

#initial state
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledGreen, GPIO.LOW)

#event handler functions
def printFunction(channel):
	print("Button pressed!")
	print("Note how the bouncetime affects the button press")
	GPIO.output(ledRed, GPIO.HIGH)
	time.sleep(0.075)
	GPIO.output(ledRed, GPIO.LOW)

#event handlers
GPIO.add_event_detect(button, GPIO.FALLING, callback=printFunction, bouncetime=300)
#GPIO.remove_event_detect(23) #for when you need it

#let's go!
print("Here we go! Press Ctrl+C to exit")
try:
	while 1:
		if GPIO.input(button):
			GPIO.output(ledGreen, GPIO.LOW)
		else:
			GPIO.output(ledGreen, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(ledGreen, GPIO.LOW)
except KeyboardInterrupt:
	#exit cleanly
	GPIO.cleanup()
'''
while True:
	#if(GPIO.input(23)==1):
	#	print("Button 1 pressed")
	GPIO.wait_for_edge(23,GPIO.RISING)
	print("Button Pressed")
	GPIO.wait_for_edge(23, GPIO.FALLING)
	print("Button Released")
'''