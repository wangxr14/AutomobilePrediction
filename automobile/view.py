#-*- coding: utf-8 -*
from django.http import HttpResponse
from django.shortcuts import render
import os
import httplib, urllib, base64
import urllib2
import json
import types
import base64
from django.template import RequestContext
import logging
from io import BytesIO

subscriptionKey = 'ff3211903f88418a84f773c333b95ecd' 
#My group ID
personGroupId = 'wxr2014011300'
personlist = []
persistedFaceList = []
FaceURL = 'westus.api.cognitive.microsoft.com'
imgUrl = 'http://168.63.209.202/pic.png'
picUrl = '/pic.png'

headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscriptionKey,
	}
	
def login(request):
    return render(request, 'login.html')
	
def loginWithFace(request):
	
	return render(request, 'login_face.html')

def signUpWithFace(request):
	
	return render(request, 'sign_up.html')
	
def signUp(request):
	username = request.POST.get('username','')
	photourl = request.POST.get('photourl','')
	mode = request.POST.get('mode','')
	
	data = {}
	personId = "" 
	persistedFaceId = ""
	params = urllib.urlencode({})

	#Get person ID
	body = {'name':username,'userData':'New User'}
	
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
		
	if(mode == "signup"):		
		#Get Persisted ID 
		imgData = base64.b64decode(photourl)
		file = open(picUrl,'wb')
		file.write(imgData)
		file.close()
		body = {'url':imgUrl}
		data = {}
		 
		try:
			conn = httplib.HTTPSConnection(FaceURL)
			conn.request("POST", ("/face/v1.0/persongroups/"+personGroupId+"/persons/"+personId+"/persistedFaces?%s") % params, json.dumps(body), headers)
			response = conn.getresponse()
			data = response.read()
			persistedFaceId = json.loads(data).get("persistedFaceId")
			conn.close()
			
		except Exception as e:
			print e	
	return render(request, 'sign_up.html',{'person':mode,'data':persistedFaceId})
	
def renderSearchPage(request):
	photourl = request.POST.get('photourl','')
	mode = request.POST.get('mode','')
	
	url = ''
	#Get the user's present face ID
	faceID = ''
	tmp = ''
	tmp1= ''
	tmp2=''
	tmp3=''
	params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender',
	})
	
		
	#Judge the mode 
	if(mode == 'shot'):
		headers = {	'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': subscriptionKey}
		imgData = base64.b64decode(photourl)
		file = open(picUrl,'wb')
		file.write(imgData)
		file.close()
		body ={'url':imgUrl}
		try:
			conn = httplib.HTTPSConnection(FaceURL)
			tmp1=json.dumps(body)
			conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
			response = conn.getresponse()
			data = response.read()
			tmp = data
			conn.close()
			faceID = json.loads(data)[0].get("faceId")
			
		except Exception as e:
			print e
	elif(mode == 'photo'):
		url = photourl
		body ={'url':url}
		try:
			conn = httplib.HTTPSConnection(FaceURL)
			conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
			response = conn.getresponse()
			data = response.read()
			tmp = data
			conn.close()
			faceID = json.loads(data)[0].get("faceId")
			
		except Exception as e:
			print e
	else:
		url = ''
	
	
	
		
		
	#Get person list
	personlist = []
	body ={}
	data=''
	params = urllib.urlencode({})
	try:
		conn = httplib.HTTPSConnection(FaceURL)
		conn.request("GET", ("/face/v1.0/persongroups/"+personGroupId+"/persons?%s") % params, json.dumps(body), headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		
		personlist = json.loads(data)
		
	except Exception as e:
		print e
	
	#verify
	isIdentical = ''
	data = ''
	for i in personlist:
		pId = i.get("personId")
		body = {"faceId":faceID,"personId":pId,"personGroupId":personGroupId}
		data = '' 
		try:
			conn = httplib.HTTPSConnection(FaceURL)
			tmp2 = json.dumps(body)
			conn.request("POST", "/face/v1.0/verify?%s" % params, json.dumps(body), headers)
			response = conn.getresponse()
			data = response.read()
			tmp3=data
			isIdentical = json.loads(data).get("isIdentical")		
			if(isIdentical): 
				break
			conn.close()
		except Exception as e:
			print e
	if(isIdentical):
		return render(request, 'searchPage.html',{"personlist":personlist,"faceList":tmp,"isIdentical":data})
	else:
		
		return render(request, 'login_face.html',{"logininfo":"login failed! Data:"+data+'     Tmp:'+tmp+'   TMP2:'+tmp2+'   TMP3:'+tmp3})
		
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
	result = ''
	try:
		response = urllib2.urlopen(req)

		# If you are using Python 3+, replace urllib2 with urllib.request in the above code:
		# req = urllib.request.Request(url, body, headers) 
		# response = urllib.request.urlopen(req)

		result = response.read()
		
		resultlist = json.loads(result).get("Results").get("output1").get("value").get("Values")[0]
		length = len(resultlist)
		result = resultlist[length-1]
		
	except urllib2.HTTPError, error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())

		print(json.loads(error.read()))                 
        return render(request, 'result.html',{'result':result})

def getPic(request):
	image_data = open(picUrl,"rb").read()
	return HttpResponse(image_data,content_type="image/png")
