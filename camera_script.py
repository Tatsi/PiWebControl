import picamera
import time
from DHT11 import DHT11Read

camera = picamera.PiCamera()
dhtvalues =Â[24*60]

f = open('/home/pi/controlapp/static/sensorvalues', 'w')
data = f.read()
f.seek(0)
f.write("0\n")
f.write(dhtvalues)
f.close()

while 1 == 1:
    # Take a snapshot and read sensor values every 10 minutes
    camera.capture('/home/pi/controlapp/static/snapshot.jpg')
    # print 'took picture'
    
    dhtdata = DHT11Read()
    while dhtdata == None:
        time.sleep(3)
        dhtdata = DHT11Read()    
    f = open('/home/pi/controlapp/static/sensorvalues', 'w')
    pointer = f.readline()
    data = f.read()
    data[int(pointer)] = dhtdata
    f.seek(0)
    f.write(int(pointer)+1)
    f.write('\n')
    f.write(data)
    f.close()

    time.sleep(60*10)
