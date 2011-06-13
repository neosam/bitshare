import settings
import bitcoin
import simplejson
import os
import uuid
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.servers.basehttp import FileWrapper
from staticload.models import *

def getLink(request, uuid):
	try:
		destFile = StoredFile.objects.get(uuid=uuid)
	except:
		return HttpResponse(simplejson.dumps(False))
	conn = bitcoin.connect_to_local()
	result = dict()
	result['bitcoinAddress'] = conn.getnewaddress()
	result['amount'] = destFile.amount

	request = Request(storedFile=destFile,
			address=result['bitcoinAddress'])
	request.save()

	return HttpResponse(simplejson.dumps(result))

def request(request, address):
	conn = bitcoin.connect_to_local()
	result = False
        try:
		fileRequest = Request.objects.get(address=address)
	except:
		return HttpResponse(simplejson.dumps(False))
	try:
		if conn.getreceivedbyaddress(address, settings.MIN_CONFIRMATIONS) >= \
			+ fileRequest.storedFile.amount:
			result = settings.ROOT_URL + "/download/" + address
	except:
		result = False
	return HttpResponse(simplejson.dumps(result))

def handleUploadFile(f, destAddress, amount):
	savename = str(uuid.uuid4())
	savefile = open(settings.MEDIA_ROOT + "/" + savename, 'w')
	print str(dir(f))
	splitted = f.name.split('.')
	print splitted[len(splitted) - 1]

	for chunk in f.chunks():
		savefile.write(chunk)

	uploaded = StoredFile(uuid=savename, 
                              extension=splitted[len(splitted) - 1],
                              destAddress=destAddress,
                              amount=amount)
	uploaded.save()
	return savename

@csrf_exempt
def upload(request):
	filename = handleUploadFile(request.FILES['file'], 
				request.POST['destAddress'],
				request.POST['amount'])
        return HttpResponse(filename)
        
def download(request, address):
	try:
		fileRequest = Request.objects.get(address=address)
	except:
		return HttpResponse('false')
	print dir(fileRequest.storedFile)
	uuid = fileRequest.storedFile.uuid
	filename = settings.MEDIA_ROOT + '/' + uuid
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='data/unknown')
	response['Content-Length'] = os.path.getsize(filename)
	conn = bitcoin.connect_to_local()
	conn.sendtoaddress(fileRequest.storedFile.destAddress, fileRequest.storedFile.amount)
	fileRequest.delete()
	
	return response
	
