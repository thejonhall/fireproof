import pycurl, json
from StringIO import StringIO
# import RPi.GPIO as GPIO

#setup GPIO using Broadcom SOC channel numbering
# GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
# GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# use this to capture the response from our push API call
buffer = StringIO()

# use Curl to post to the Instapush API
c = pycurl.Curl()

# set API URL
# c.setopt(c.URL, 'https://api.parse.com/1/push')
c.setopt(c.URL, 'https://api.spark.io/v1/events/AerieMotionDetected')

#setup custom headers for authentication variables and content type
c.setopt(c.HTTPHEADER, ['Authorization: Bearer ' + '1f85093f9be1f1f772804e19bf52e981c1d62bd5' ,
             'Content-Type: application/json'])

# create a dict structure for the JSON data to post
# json_fields = {}

# setup JSON values
# postfields = json.dumps(json_fields)

# make sure to send the JSON with post
# c.setopt(c.URL, postfields)

# set this so we can capture the response in our buffer
# c.setopt(c.WRITEFUNCTION, buffer.write)

# uncomment to see the post sent
c.setopt(c.VERBOSE, True)

c.setopt(pycurl.HTTPGET, 1)

# curl -H "Authorization: Bearer 1f85093f9be1f1f772804e19bf52e981c1d62bd5" https://api.spark.io/v1/events/AerieMotionDetected


# setup an indefinite loop that looks for the door to be opened / closed
while True:

    c.perform()
    # GPIO.wait_for_edge(23, GPIO.RISING)
    print("Waiting!\n")

    # send push note


    # capture the response from the server
    body= buffer.getvalue()

    # print the response
    print(body)

    # reset the buffer
    buffer.truncate(0)
    buffer.seek(0)

    # cleanup
    c.close()
    # GPIO.cleanup()
