import pycurl, json
from StringIO import StringIO

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
    json_fields = {
        "where": {
            "deviceType": deviceType
        },
        "data": {
            "alert": "This is a push note for " + deviceType
        }
    }
    postfields = json.dumps(json_fields)
    curl.setopt(curl.POSTFIELDS, postfields)
    curl.setopt(curl.WRITEFUNCTION, responseBuffer.write)
    if verbose:
        curl.setopt(curl.VERBOSE, True)
    return curl

# send push note
curl_ios = setUpCurl("ios", buffer_ios, True)
curl_android = setUpCurl("android", buffer_android, True)

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

# cleanup
curl_ios.close()
curl_android.close()
