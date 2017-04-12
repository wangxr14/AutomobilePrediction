from django.http import HttpResponse
from django.shortcuts import render
 
import httplib, urllib, base64
import urllib2
import json
import types

subscriptionKey = 'eb08b2853536476ea05335d5dd269293' 
#My group ID
personGroupId = 'wxr2014011300'

FaceURL = 'westus.api.cognitive.microsoft.com'

def login(request):
    return render(request, 'login.html')
	
def loginWithFace(request):
	

	return render(request, 'redirect_back.html')

def signUp(request):
	username = request.GET.get('username','')
	photourl = request.GET.get('photourl','')
	
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscriptionKey,
	}

	params = urllib.urlencode({})

	#Get person ID
	body = {'name':username,'userData':'New User'}
	data = {}
	personId = "" 
	try:
		conn = httplib.HTTPSConnection(FaceURL)
		conn.request("POST", ("/face/v1.0/persongroups/"+personGroupId+"/persons?%s") % params, json.dumps(body), headers)
		response = conn.getresponse()
		data = response.read()
		personId = json.loads(data).get("personId")
		conn.close()
	except Exception as e:
		print e
		data = e
	
	#Get Persisted ID 
	body = {'url':photourl}
	data = {}
	persistedFaceId = "" 
	try:
		conn = httplib.HTTPSConnection(FaceURL)
		conn.request("POST", ("/face/v1.0/persongroups/"+personGroupId+"/persons/"+personId+"/persistedFaces?%s") % params, json.dumps(body), headers)
		response = conn.getresponse()
		data = response.read()
		persistedFaceId = json.loads(data).get("persistedFaceId")
		conn.close()
	except Exception as e:
		print e	
	return render(request, 'sign_up.html',{'data':persistedFaceId})
	
def renderSearchPage(request):
	
	answerlist = []
	
	return render(request, 'searchPage.html')

def renderResult(request):
	make = request.GET.get('make','')
	bodystyle = request.GET.get('bodystyle','')
	wheelbase = request.GET.get('wheelbase','')
	enginesize = request.GET.get('enginesize','')
	horsepower = request.GET.get('horsepower','')
	peakrpm = request.GET.get('peakrpm','')
	highwaympg = request.GET.get('highwaympg','')
	price = request.GET.get('price','')
	
	data =  {

			"Inputs": {

					"input1":
					{
						"ColumnNames": ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style", "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight", "engine-type", "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"],
						"Values": [ [ "0", "0", make, "value", "value", "value", bodystyle, "value", "value", wheelbase, "0", "0", "0", "0", "value", "value", enginesize, "value", "0", "0", "0", horsepower, peakrpm, "0", highwaympg, price ], [ "0", "0", "value", "value", "value", "value", "value", "value", "value", "0", "0", "0", "0", "0", "value", "value", "0", "value", "0", "0", "0", "0", "0", "0", "0", "0" ], ]
					},        },
				"GlobalParameters": {
	}
		}

	body = str.encode(json.dumps(data))

	url = 'https://ussouthcentral.services.azureml.net/workspaces/cc42249fc9bf47c99258ff24cfdd4c01/services/65f0f43a352b4d73bfbc6d71ea273c90/execute?api-version=2.0&details=true'
	api_key = '6rVIvDu+/KoeK25mZAyCWS0uhhq05HMy4SlzVrrpny+9Umj7vbw6aAAUY7uibk3HGKYkhqJ+eE/FQSfOfHkF7g==' # Replace this with the API key for the web service
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

	req = urllib2.Request(url, body, headers) 

	try:
		response = urllib2.urlopen(req)

		# If you are using Python 3+, replace urllib2 with urllib.request in the above code:
		# req = urllib.request.Request(url, body, headers) 
		# response = urllib.request.urlopen(req)

		result = response.read()
		print(result) 
	except urllib2.HTTPError, error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())

		print(json.loads(error.read()))                 
        return render(request, 'result.html',{'result':result})

