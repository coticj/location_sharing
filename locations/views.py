from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from locations.models import Location,User
from django.template import RequestContext, loader
from ipware.ip import get_real_ip
from datetime import datetime
import GeoIP
from django.conf import settings
from django.db.models import Count
from django.shortcuts import redirect



def index(request):
	#count total unique visitors in the past 5min
	total = Location.objects.raw("SELECT id, count(distinct(user_ip)) as c from locations_location WHERE datetime(visit_date) >= Datetime('now', '-5 minutes')")[0]
	#init the vars
	cr=""
	ip = get_real_ip(request)
	now = datetime.now()
	
	#init geoip db
	gi = GeoIP.open(settings.GEO_IP_DB, GeoIP.GEOIP_STANDARD)
	gir = gi.record_by_addr(ip)
	
	#check if visitor was already here in the past 5min, otherwise save his visit
	visitor_min=Location.objects.raw("SELECT id from locations_location WHERE datetime(visit_date) >= Datetime('now', '-5 minutes') and user_ip like %s", [ip,])
	
	if not list(visitor_min):
		entry = Location(user_ip=ip,visit_date=now,lat=gir['latitude'],lon=gir['longitude'],location=gir['country_name'])
		entry.save()
		
	#check if users ip is already registered, if so, then log in	
	dbip=Location.objects.raw("SELECT id,email as e from locations_user where user_ip like %s", [ip,])
	if list(dbip):
		cr=dbip[0].e
		return redirect('/locations')
	#check if email was posted,saves it in db and logs the user in	
	if request.POST:
		email=request.POST['email']
		user = User(user_ip=ip,email=email)
		user.save()
		return redirect('/locations')
	#if nothing, then display regular welcome page
	else:
		template = loader.get_template('locations/index.html')
		context = RequestContext(request, {
			'total':total.c,
			't':cr,
		})
		return HttpResponse(template.render(context))
	


def locations(request):
	ip = get_real_ip(request)
	#get list of all distinc users
	user_list = Location.objects.raw("SELECT id, user_ip,location,lat,lon,visit_date from locations_location group by user_ip")
	
	#check if username exists and take user as logged in
	username=Location.objects.raw("SELECT id,email as username from locations_user where user_ip like %s", [ip,])
	
	if list(username):
		#get list of unique visitors in the past 5 minutes
		people = Location.objects.raw("SELECT id, count(distinct(user_ip)) as c from locations_location WHERE datetime(visit_date) >= Datetime('now', '-5 minutes')")[0]
		#get list of unique visits by the hour for the previous day 
		hours= Location.objects.raw("select id,strftime('%Y-%m-%dT%H:00:00.000', visit_date) as h,time(strftime('%Y-%m-%dT%H:00:00.000', visit_date),'localtime') as time,count(distinct(user_ip)) as c from locations_location where strftime('%Y-%m-%d', visit_date) =  strftime('%Y-%m-%d', DATE('now','-1 days')) group by strftime('%Y-%m-%dT%H:00:00.000', visit_date) ")
		
		gi = GeoIP.open(settings.GEO_IP_DB, GeoIP.GEOIP_STANDARD)
		gir = gi.record_by_addr(ip)
		
		now = datetime.now()
		visitor_min=Location.objects.raw("SELECT id from locations_location WHERE datetime(visit_date) >= Datetime('now', '-5 minutes') and user_ip like %s", [ip,])
	
		if not list(visitor_min):
			entry = Location(user_ip=ip,visit_date=now,lat=gir['latitude'],lon=gir['longitude'],location=gir['country_name'])
			entry.save()

		template = loader.get_template('locations/locations.html')
		context = RequestContext(request, {
			'user_list': user_list,
			'ip': ip,
			'lat':gir['latitude'],
			'lon':gir['longitude'],
			'p':people.c,
			'hours':hours,
			'username':username[0].username,
		})
		return HttpResponse(template.render(context))
	else:
		return redirect('/')
