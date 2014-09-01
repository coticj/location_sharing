from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from locations.models import Location
from django.template import RequestContext, loader
from ipware.ip import get_real_ip
from datetime import datetime
import GeoIP
from django.conf import settings

def index(request):
	user_list = Location.objects.all()
	ip = get_real_ip(request)
	
	gi = GeoIP.open(settings.GEO_IP_DB, GeoIP.GEOIP_STANDARD)
	gir = gi.record_by_addr(ip)
	
	now = datetime.now()
	entry = Location(user_ip=ip,visit_date=now,email="test",lat=gir['latitude'],lon=gir['longitude'],location=gir['country_name'])
	#entry.save()
	
	template = loader.get_template('locations/index.html')
	context = RequestContext(request, {
		'user_list': user_list,
		'ip': ip,
		'lat':gir['latitude'],
		'lon':gir['longitude'],
	})
	return HttpResponse(template.render(context))