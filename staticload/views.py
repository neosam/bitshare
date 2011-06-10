import settings
import bitcoin
import simplejson
from django.http import HttpResponse

def getLink(request):
	conn = bitcoin.connect_to_local()
	result = dict()
	result['bitcoinAddress'] = conn.getnewaddress()
	result['amount'] = settings.AMOUNT
        result['requestLink'] = settings.ROOT_URL + '/request/' \
			+ result['bitcoinAddress']
	return HttpResponse(simplejson.dumps(result))

def request(request, address):
	conn = bitcoin.connect_to_local()
	result = False
	try:
		if conn.getreceivedbyaddress(address, settings.MIN_CONFIRMATIONS) >= \
			+ settings.AMOUNT:
			result = settings.ROOT_URL + settings.STATICLINK 
	except:
		pass
	return HttpResponse(simplejson.dumps(result))
