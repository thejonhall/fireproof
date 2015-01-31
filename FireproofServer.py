import pycurl, json
from StringIO import StringIO

# use this to capture the response from our push API call
buffer_ios = StringIO()
buffer_android = StringIO()

# use Curl to post
curl_ios = pycurl.Curl()
curl_android = pycurl.Curl()

# set API URL
curl_ios.setopt(curl_ios.URL, 'https://api.parse.com/1/push')
curl_android.setopt(curl_android.URL, 'https://api.parse.com/1/push')

#setup custom headers for authentication variables and content type
curl_ios.setopt(curl_ios.HTTPHEADER, ['X-Parse-Application-Id: ' + 'hDYfKAEThkm2emN2IBpnGpWOizlz6o7lypTbHkJs',
			'X-Parse-REST-API-Key: ' + 'zEV9JpG4Q8iwMGP9hrVxvbUK0fFm4Ly8UJW6YNGN',
			'Content-Type: application/json'])
curl_android.setopt(curl_android.HTTPHEADER, ['X-Parse-Application-Id: ' + 'hDYfKAEThkm2emN2IBpnGpWOizlz6o7lypTbHkJs',
			'X-Parse-REST-API-Key: ' + 'zEV9JpG4Q8iwMGP9hrVxvbUK0fFm4Ly8UJW6YNGN',
			'Content-Type: application/json'])


# create a dict structure for the JSON data to post
json_fields_ios = {
        "where": {
          "deviceType": "ios"
        },
        "data": {
          "alert": "This is a push note for iOS!"
        }
}
json_fields_android = {
        "where": {
          "deviceType": "android"
        },
        "data": {
          "alert": "This is a push note for Android!"
        }
}

# setup JSON post
postfields_ios = json.dumps(json_fields_ios)
postfields_android = json.dumps(json_fields_android)

# make sure to send the JSON with post
curl_ios.setopt(curl_ios.POSTFIELDS, postfields_ios)
curl_android.setopt(curl_android.POSTFIELDS, postfields_android)

# set this so we can capture the resposne in our buffer
curl_ios.setopt(curl_ios.WRITEFUNCTION, buffer_ios.write)
curl_android.setopt(curl_android.WRITEFUNCTION, buffer_android.write)

# uncomment to see the post sent
curl_ios.setopt(curl_ios.VERBOSE, True)
curl_android.setopt(curl_android.VERBOSE, True)

print("Sent a push note!\n")

# send push note
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
