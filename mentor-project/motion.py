from gpiozero import MotionSensor
import logging
from twilio.rest import Client
from picamera import PiCamera
import time

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

pir = MotionSensor(14)

camera = PiCamera()
camera.resolution = (1024, 768)
camera.rotation = 180

logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Starting')

while True:
    if pir.motion_detected:
        camera.start_preview()
        camera.start_recording('./images/{time}.h264'.format(time = time.asctime(time.localtime())))
        pir.wait_for_no_motion()
        camera.stop_recording()
        camera.stop_preview()
        print('Motion detected.')
        logging.info('Motion detected')
        message = client.messages.create(
            body="Someone's here!",
            from_="",
            to=""
        )
