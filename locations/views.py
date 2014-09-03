from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from locations.models import Location
from django.template import RequestContext, loader
from ipware.ip import get_real_ip
from datetime import datetime
import GeoIP
from django.conf import settings
from django.db.models import Count
from django.shortcuts import redirect

def index(request):
	total = Location.objects.raw("SELECT id, count(distinct(user_ip)) as c from locations_location WHERE datetime(visit_date) >= Datetime('now', '-5 minutes')")[0]
	t="ni post"
	if request.POST:
		t=request.POST['email']
	
	template = loader.get_template('locations/index.html')
	context = RequestContext(request, {
		'total':total.c,
		't':t
	})
	return HttpResponse(template.render(context))
	


def locations(request):
	user_list = Location.objects.all()
	ip = get_real_ip(request)
	p = Location.objects.raw('SELECT id, count(distinct(user_ip)) as c from locations_location')[0]
	hours= Location.objects.raw("select id,strftime('%Y-%m-%dT%H:00:00.000', visit_date) as h,time(strftime('%Y-%m-%dT%H:00:00.000', visit_date),'localtime') as time,count(distinct(user_ip)) as c from locations_location where strftime('%Y-%m-%d', visit_date) =  strftime('%Y-%m-%d', DATE('now','-1 days')) group by strftime('%Y-%m-%dT%H:00:00.000', visit_date) ")
	
	gi = GeoIP.open(settings.GEO_IP_DB, GeoIP.GEOIP_STANDARD)
	gir = gi.record_by_addr(ip)
	
	now = datetime.now()
	entry = Location(user_ip=ip,visit_date=now,email="test",lat=gir['latitude'],lon=gir['longitude'],location=gir['country_name'])
	#entry.save()

	template = loader.get_template('locations/locations.html')
	context = RequestContext(request, {
		'user_list': user_list,
		'ip': ip,
		'lat':gir['latitude'],
		'lon':gir['longitude'],
		'p':p.c,
		'hours':hours,
	})
	return HttpResponse(template.render(context))
