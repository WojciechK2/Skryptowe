def RASA_messageAPICall(message,user):
	import requests
	import json
	
	headers = {
	'Content-Type':'application/json',
	'Accept':'application/json'
	}
	
	data = '{ "sender":"' + user + '","message": "' + message +'","metadata":{}}'
	response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers = headers, data = data)
	
	messages = json.loads(response.content)
	answer = list(map(lambda msg: msg['image'] if 'image' in msg else msg['text'], messages))
	return answer


