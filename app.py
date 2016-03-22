from flask import Flask, render_template 
import RPi.GPIO as GPIO 
import picamera 
import sys

print "Python version" + sys.version

# Create app
app = Flask(__name__)

# Init camera
try:
    camera = picamera.PiCamera()
except:
    print "Failed to init camera"

################################
## Define static variables
################################

PIN_THERMOMETER = 2
PIN_MOISTURE = 3
PIN_LED = 6

CAMERA_LOCATION = '/dev/video0'
CAMERA_IMAGE_URL = '/static/snapshot.jpg'

################################
## Init GPIO stuff
################################

try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PIN_THERMOMETER, GPIO.IN)
    GPIO.setup(PIN_MOISTURE, GPIO.IN)

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
        'image_url' : CAMERA_IMAGE_URL,
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
                camera = picamera.PiCamera()
                camera.capture('/static/test.jpg')
                import os
                os.system('raspistill -o static/snapshot.jpg')
            except:
                message = 'Error in taking a snapshot!'

    # Read values to template data
    try:
        thermometer_value = GPIO.input(PIN_THERMOMETER)
        moisture_value = GPIO.input(PIN_MOISTURE)
        led_status = GPIO.input(PIN_LED)
    except:
        message = 'Error in reading pin values.'

    template_data = {                                                           
        'title' : 'Control page',
        'message' : message,
        'led_status' : led_status,
        'thermometer_value' : thermometer_value,
        'moisture_value' : moisture_value,
        'camera_image_url' : CAMERA_IMAGE_URL,                                             
    }
    return render_template('index.html', **template_data)

###########################
## Main function
###########################
if __name__ == '__main__':
    # Init camera
    #try:
    #    camera = picamera.PiCamera()
    #except:
    #    print "Failed to init camera"
    app.run(debug=True, host='0.0.0.0')
