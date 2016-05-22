from django.http import HttpResponse
from django.shortcuts import render


import json, httplib, urllib, os
from confidential.keys import PARSE_APP_ID, PARSE_API_KEY

def get_dilemme(dilemme_id):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"include":"pictures"})
	connection.connect()
	connection.request('GET', '/1/classes/Dilemmes/%s?%s' % (dilemme_id, params), '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_API_KEY
	})
	result = json.loads(connection.getresponse().read())
	return result

def get_user(user_id):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	#params = urllib.urlencode({"include":"pictures"})
	connection.connect()
	connection.request('GET', '/1/users/%s' % (user_id), '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_API_KEY
	})
	result = json.loads(connection.getresponse().read())
	return result

def index(request):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"include":"pictures"})
	connection.connect()
	connection.request('GET', '/1/classes/Dilemmes/CTIgk1D6JK?%s' % params, '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_API_KEY
     })
	result = json.loads(connection.getresponse().read())
	context = {'content': result["pictures"][0]["picture"]["url"]}

	#from template dir
	return render(request, 'dilemme/index.html', context)

def detail(request, dilemme_id):
	dilemme = {}
	result = get_dilemme(dilemme_id)

	dilemme["id"] = result["objectId"]
	dilemme["description"] = result["description"]

	pictures = []
	pictures_from_result = result["pictures"]

	isSingleDilemme = True if len(pictures_from_result) == 1 else False
	dilemme["isSingleDilemme"] = isSingleDilemme

	urls = []
	for picture_from_result in pictures_from_result:
		picture = {}
		picture["id"] = picture_from_result["objectId"]
		picture["likes"] = picture_from_result["like"]
		picture["dislikes"] = picture_from_result["dislike"]
		picture["url"] = picture_from_result["picture"]["url"]
		pictures.append(picture)

		urls.append(picture_from_result["picture"]["url"])
	
	dilemme["pictures"] = pictures
	
	context = {
		'description': result["description"],
		'dilemme_pictures': urls
	}
	#token = request.GET.get('access_token')
	#user = request.backend.do_auth(request.GET.get('access_token'))

	#user = UserSocialAuth.objects.filter(user=request.user)
	user_sender = result["user_id_fk"]["objectId"]
	user_from_result = get_user(user_sender)

	user = {}
	user["id"] = user_from_result["objectId"]
	user["fbID"] = user_from_result["fbID"]
	user["first_name"] = user_from_result["first_name"]
	user["location_name"] = user_from_result["location_name"]
	user["picture_url"] = user_from_result["profile_picture"]["url"]

	dilemme["sender"] = user

	#user = request.user
	#if not user.is_anonymous():
		#social = user.social_auth.get(provider='facebook')
		#userid = social.uid

		#print "extra data: "
		#print social.extra_data
		#print "userid: " 
		#print userid

	#from template dir
	return render(request, 'dilemme/index.html', dilemme)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)





