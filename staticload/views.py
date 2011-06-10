import settings
import bitcoin
import simplejson
from django.http import HttpResponse

def getLink(request):
	conn = bitcoin.connect_to_local()
	result = dict()
	result['bitcoinAddress'] = conn.getnewaddress()
	result['amount'] = 1
        result['requestLink'] = 'http://localhost:8000/request/' \
			+ result['bitcoinAddress']
	return HttpResponse(simplejson.dumps(result))

def request(request, address):
	conn = bitcoin.connect_to_local()
	result = False
	try:
		if conn.getreceivedbyaddress(address, 0) >= 1:
			result = 'http://localhost:8000/static/test.html'
	except:
		pass
	return HttpResponse(simplejson.dumps(result))
