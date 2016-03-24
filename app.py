# Connect DHT11 sensor to Pin 4 of raspberry pi

from flask import Flask, render_template 
from dht11 import DHT11Read
import RPi.GPIO as GPIO 
#import picamera 
import time
import sys

GPIO.setwarnings(False)
#print "Python version" + sys.version

# Create app
app = Flask(__name__)

# Init camera
#try:
    #camera = picamera.PiCamera()
#except:
#    print "Failed to init camera"

################################
## Define static variables
################################

PIN_LED = 6

################################
## Init GPIO stuff
################################

try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PIN_LED, GPIO.OUT)
    GPIO.output(PIN_LED, False)
except:
    print "There was an error while initializing GPIO access. Make sure to use sudo."
    exit()

################################
## Create locations
################################

@app.route('/login')
def index():
    template_data = {
        'title' : 'Login page',
    }
    return render_template('login.html', **template_data)

@app.route('/')
@app.route("/action/<action>") 
def pin(action=None):
    # init template data
    message = 'Nothing was done.'
    thermometer_value = 0
    moisture_value = 0
    led_status = 0

    # Perform the action if any
    if action != None:
        if action == 'toggle_led':
            try:
                led_value = GPIO.input(PIN_LED)
                GPIO.output(PIN_LED, not led_value)
                message = 'Led was toggled.'
            except:
                message = 'Error in toggling led!'
        elif action == 'take_snapshot':
            try:
                #camera = picamera.PiCamera()
                #camera.capture('/static/test.jpg')
                #import os
                os.system('raspistill -o static/snapshot.jpg')
            except:
                #message = 'Error in taking a snapshot!'

    # Read values to template data
    try:
        led_status = GPIO.input(PIN_LED)        
        dht_11_value = None
        while dht_11_value == None:
            print "Readin DHT11 sensor value from pin 4 failed. Trying again..""
            dht_11_value = DHT11Read()
            #time.sleep(3)
        thermometer_value = dht_11_value[1]
        moisture_value = dht_11_value[0]
    except:
        message = 'Error in reading pin values.'

    template_data = {
        'message' : message,
        'led_status' : led_status,
        'thermometer_value' : thermometer_value,
        'moisture_value' : moisture_value,                                             
    }
    return render_template('index.html', **template_data)

###########################
## Main function
###########################
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
