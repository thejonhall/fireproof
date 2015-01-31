import pycurl, json
from StringIO import StringIO
from sseclient import SSEClient

# use this to capture the response from our push API call
buffer_ios = StringIO()
buffer_android = StringIO()

def setUpCurl(deviceType, responseBuffer, verbose):
    # use Curl to post
    curl = pycurl.Curl()
    #setup custom headers for authentication variables and content type
    curl.setopt(curl.URL, 'https://api.parse.com/1/push')
    curl.setopt(curl.HTTPHEADER, ['X-Parse-Application-Id: ' + 'hDYfKAEThkm2emN2IBpnGpWOizlz6o7lypTbHkJs',
        			'X-Parse-REST-API-Key: ' + 'zEV9JpG4Q8iwMGP9hrVxvbUK0fFm4Ly8UJW6YNGN',
        			'Content-Type: application/json'])
    return curl
    
def setUpPushNoteForCurl(curl, deviceType, responseBuffer, data, verbose):
    json_fields = {
        "where": {
            "deviceType": deviceType
        },
        "data": {
            "alert": "This is a push note for " + deviceType + " with data " + data
        }
    }
    postfields = json.dumps(json_fields)
    curl.setopt(curl.POSTFIELDS, postfields)
    curl.setopt(curl.WRITEFUNCTION, responseBuffer.write)
    if verbose:
        curl.setopt(curl.VERBOSE, True)

# send push note
curl_ios = setUpCurl("ios", buffer_ios, True)
curl_android = setUpCurl("android", buffer_android, True)

buffer_smoke = StringIO()

# deviceID = '54ff76066672524853170167'
accessToken = '1f85093f9be1f1f772804e19bf52e981c1d62bd5'
sparkURL = 'https://api.spark.io/v1/events/AerieSmokeDetected?access_token=' + accessToken
messages = SSEClient(sparkURL)
#
# deviceID = '53ff6d066667574857350967'
# accessToken = '1f85093f9be1f1f772804e19bf52e981c1d62bd5'
# sparkURL = 'https://api.spark.io/v1/devices/' + deviceID + '/events/?access_token=' + accessToken

# messages2 = SSEClient(sparkURL)

for msg in messages:
    if msg.data:
        print 'Processing Spark Event: ', msg

        setUpPushNoteForCurl(curl_ios, "ios", buffer_ios, msg.data, True)
        setUpPushNoteForCurl(curl_android, "android", buffer_ios, msg.data, True)

        curl_ios.perform()
        curl_android.perform()

        # capture the response from the server
        body= buffer_ios.getvalue()
        # print the response
        print(body)

        body= buffer_android.getvalue()
        # print the response
        print(body)

        # reset the buffer
        buffer_ios.truncate(0)
        buffer_ios.seek(0)
        buffer_android.truncate(0)
        buffer_android.seek(0)

        # reset the buffer
        buffer_smoke.truncate(0)
        buffer_smoke.seek(0)

        # cleanup
        # curl_event.close()
        # cleanup
        #curl_ios.close()
        #curl_android.close()

# for msg in messages2:
#     print 'Checking stuff'
#     if msg.data:
#         print 'Processing Spark Event: ', msg
#         setUpPushNoteForCurl(curl_ios, "ios", buffer_ios, msg.data, True)
#         setUpPushNoteForCurl(curl_android, "android", buffer_android, msg.data, True)
#
#         curl_ios.perform()
#         curl_android.perform()
#
#         # capture the response from the server
#         body= buffer_ios.getvalue()
#         # print the response
#         print(body)
#
#         body= buffer_android.getvalue()
#         # print the response
#         print(body)
#
#         # reset the buffer
#         buffer_ios.truncate(0)
#         buffer_ios.seek(0)
#         buffer_android.truncate(0)
#         buffer_android.seek(0)
#
#         # reset the buffer
#         buffer_smoke.truncate(0)
#         buffer_smoke.seek(0)
#
#         # cleanup
#         # curl_event.close()
#         # cleanup
#         #curl_ios.close()
#         #curl_android.close()