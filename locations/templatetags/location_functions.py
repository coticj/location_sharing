from django import template
from math import sin, cos, sqrt, atan2, radians

register = template.Library()

@register.simple_tag

def get_distance(lat1,lon1,lat2,lon2):
	R = 6373.0
	
	rlat1 = radians(float(lat1))
	rlon1 = radians(float(lon1))
	rlat2 = radians(float(lat2))
	rlon2 = radians(float(lon2))
	
	dlon = rlon2 - rlon1
	dlat = rlat2 - rlat1
	a = (sin(dlat/2))**2 + cos(rlat1) * cos(rlat2) * (sin(dlon/2))**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	distance = R * c
	
	return int(distance)