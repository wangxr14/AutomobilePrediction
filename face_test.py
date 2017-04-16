import httplib, urllib, base64
import json

personGroupId = 'wxr2014011300'
imgUrl = 'http://168.63.209.202/pic.png'
#imgUrl='https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'ff3211903f88418a84f773c333b95ecd',
}

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age',
})

body ={}
#personId = 'ded07a12-7344-405a-a2bd-9e2385f76fc6'
try:
	body ={'url':imgUrl}
	conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	#conn.request("GET", "/face/v1.0/persongroups/"+personGroupId+"/persons?%s" % params, json.dumps(body), headers)
	conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
	response = conn.getresponse()
	data = response.read()
	print(data)
	conn.close()
except Exception as e:
	print e
