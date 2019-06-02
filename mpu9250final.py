from __future__ import print_function
import time, sys, signal, atexit, socket
from upm import pyupm_mpu9150 as sensorObj

def main():
    # Instantiate an MPU9250 on I2C bus 0
    sensor = sensorObj.MPU9250()

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    sensor.init()

    x = sensorObj.new_floatp()
    y = sensorObj.new_floatp()
    z = sensorObj.new_floatp()
    a = sensorObj.new_floatp()
    b = sensorObj.new_floatp()
    c = sensorObj.new_floatp()
    i = sensorObj.new_floatp()
    j = sensorObj.new_floatp()
    k = sensorObj.new_floatp()

    HOST = ''
    PORT = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    
    try:
        s.bind((HOST, PORT))
    except socket.error:
        print("Bind failed")

    s.listen(1)
    (conn, addr) = s.accept()

     print("Connected")

    while conn is not None:
        try:
            if conn is not None:
                sensor.update()
                sensor.getAccelerometer(x, y, z)
                sensor.getGyroscope(a, b, c)
                sensor.getMagnetometer(i, j, k)
                conn.sendall("%.1f--n--%.1f--n--%.1f--n--%.1f--n--%.1f--n--%.1f--n--%.1f--n--%.1f--n--%.1f\n" % (sensorObj.floatp_value(x), sensorObj.floatp_value(y), sensorObj.floatp_value(z), sensorObj.floatp_value(a), sensorObj.floatp_value(b), sensorObj.floatp_value(c), sensorObj.floatp_value(i), sensorObj.floatp_value(j), sensorObj.floatp_value(k)))
        except Exception as e:
            conn.close()
            conn = None
            print("Connection closed")


        time.sleep(.5)

if __name__ == '__main__':
    main()
