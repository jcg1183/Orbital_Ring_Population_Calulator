import math
import os
import sys
import time

from geographiclib.geodesic import Geodesic

import settings
from objs import Point, Ring


#set geodesic reference system
geod = Geodesic.WGS84


# ***************************************************************
# Function:         ring_check
# Variables/input:  object type ring
# Output:           writes points to ring object
# Usage/Purpose:    Function checks parameters of the ring object
#					to detect if a point and azimuth was given
#					or two pointers were given.  Prepares ring 
#					for use.
# ***************************************************************
def ring_check(ring):
	start_lat = ring.start_point.lat
	start_lon = ring.start_point.lon
	azim = ring.azim

	# start point and end point given, calculate azimuth
	if azim == -99:
		end_lat = ring.end_point.lat
		end_lon = ring.end_point.lon

		temp = geod.InverseLine(start_lat, start_lon, end_lat, end_lon)
		g = temp.Position(0, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
		ring.azim = g['azi1']
	
	# start point and azimuth given, calculate end point
	else:
		length = ring.resolution * 10
		
		# setup for line, not ring
		if settings.line == 1:
			length = settings.earth_circ
		
		# calculate second lat/lon for map
		gc = geod.Direct(start_lat, start_lon, azim, length)

		ring.end_point = Point(gc['lat2'], gc['lon2'])

	# calculate length for line between two lat/lons
	if settings.line == 2:
		g = geod.Inverse(start_lat, start_lon, end_lat, end_lon)
		settings.earth_circ = int(g['s12']) 


# ***************************************************************
# Function:         generate_gc
# Variables/input:  object type ring
# Output:           none
# Usage/Purpose:    Function iteratively generates points along
#					the great circle specified then calls
#					generate_perpendicular for each point.
# ***************************************************************
def generate_gc(ring):	
	start_time = time.time()

	start_lat = ring.start_point.lat
	start_lon = ring.start_point.lon
	azim = ring.azim

	print("Lat %.4f Lon %.4f Azim %.4f - Generating Path" % 
		 (ring.start_point.lat, ring.start_point.lon, ring.azim))

	# iterate along great circle path by length ring.resolution
	for i in range(0, settings.earth_circ + 1, ring.resolution):
		gc = geod.Direct(start_lat, start_lon, azim, i)
		
		checked_lon = check_lon(gc['lon2'])

		generate_perpendicular(ring, [gc['lat2'], checked_lon], gc['azi2'], i)

	end_time = time.time()

	ring.path_calculation_time = end_time - start_time


# ***************************************************************
# Function:         generate_perpendicular
# Variables/input:  object type ring
# Output:           writes points to ring object
# Usage/Purpose:    Function takes a point along the great circle
#					and generates a list of perpendicular points
#					which are saved.
# ***************************************************************
def generate_perpendicular(ring, point, azim1, count):
	lat = point[0]
	lon = point[1]

	# adjust azimuth to meet library usage requirements
	azim_left = azim1 - 90
	if azim_left < 0:
		azim_left = 360 + azim_left

	azim_right = azim1 + 90
	if azim_right > 360:
		azim_right = azim_right - 360
	
	# determine number of points to calculate
	n = int(math.ceil(ring.width / ring.resolution))
	
	left_point = ''
	right_point = ''

	perp_points = []

	# Calculate left branch of the perpendicular
	for i in range(n, 0, -1):
		left_path = geod.Direct(lat, lon, azim_left, min(ring.resolution * i, ring.width))

		checked_lon = check_lon(left_path['lon2'])

		if i == n:
			left_point = Point(left_path['lat2'], checked_lon)

		# Add calculated point to list of points
		perp_points.append(Point(left_path['lat2'], checked_lon))
		ring.num_points += 1

	# Calculate right branch of the perpendicular
	for i in range(0, n+1):
		right_path = geod.Direct(lat, lon, azim_right, min(ring.resolution * i, ring.width))

		checked_lon = check_lon(right_path['lon2'])

		if i == n:
			right_point = Point(right_path['lat2'], checked_lon)

		#Add calculated point to list of points
		perp_points.append(Point(right_path['lat2'], checked_lon))
		ring.num_points += 1


	ring.points.append([point, perp_points])

	# Add perpendicular line to list of perps in ring object
	if settings.show_width == 1 and count % ring.interval == 0:
		ring.perpendiculars.append([left_point, right_point])
		ring.num_perpendiculars += 1


# ***************************************************************
# Function:         check_lon
# Variables/input:  float longitude
# Output:           float lon
# Usage/Purpose:    Function converts longitude to the convention
#					of libraries used.
# ***************************************************************
def check_lon(lon):	
	if lon > 180:
		lon = lon - 360

	if lon < -180:
		lon = lon + 360

	return lon
