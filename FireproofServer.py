import pycurl, json
from StringIO import StringIO
#import RPi.GPIO as GPIO

#setup GPIO using Broadcom SOC channel numbering
# GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
# GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# use this to capture the response from our push API call
buffer = StringIO()

# use Curl to post
c = pycurl.Curl()

# set API URL
c.setopt(c.URL, 'https://api.parse.com/1/push')

#setup custom headers for authentication variables and content type
c.setopt(c.HTTPHEADER, ['X-Parse-Application-Id: ' + 'hDYfKAEThkm2emN2IBpnGpWOizlz6o7lypTbHkJs',
			'X-Parse-REST-API-Key: ' + 'zEV9JpG4Q8iwMGP9hrVxvbUK0fFm4Ly8UJW6YNGN',
			'Content-Type: application/json'])


# create a dict structure for the JSON data to post
json_fields = {
        "where": {
          "deviceType": "ios"
        },
        "data": {
          "alert": "This is from a python script!"
        }
}

# setup JSON post
postfields = json.dumps(json_fields)

# make sure to send the JSON with post
c.setopt(c.POSTFIELDS, postfields)

# set this so we can capture the resposne in our buffer
c.setopt(c.WRITEFUNCTION, buffer.write)

# uncomment to see the post sent
c.setopt(c.VERBOSE, True)

# while True:

# GPIO.wait_for_edge(23, GPIO.RISING)
print("Sent a push note!\n")

# send push note
c.perform()

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
