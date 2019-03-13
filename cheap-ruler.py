import math

def interpolate(a, b, t):
	dx = b[0] - a[0]
	dy = b[1] - a[1]
	return [a[0] + dx * t, a[1] + dy * t]



class cheapRuler():

	def __init__(self, lat, units):
		if not lat:
			print('no')
			return
		if units not in factors:
			print('no')
			return

		m = factors[units] if units else 1

		cos = math.cos(lat * math.pi/ 180)
		cos2 = 2 * cos * cos -1
		cos3 = 2 * cos * cos2 - cos
		cos4 = 2 * cos * cos3 - cos2
		cos5 = 2 * cos * cos4 - cos3

		self.kx = m * (111.41513 * cos - 0.09455 * cos3 + 0.00012 * cos5)
		self.ky = m * (111.13209 - 0.56605 * cos2 + 0.0012 * cos4)

	factors = {
		'kilometers': 1,
	    'miles': 1000 / 1609.344,
	    'nauticalmiles': 1000 / 1852,
	    'meters': 1000,
	    'metres': 1000,
	    'yards': 1000 / 0.9144,
	    'feet': 1000 / 0.3048,
	    'inches': 1000 / 0.0254
	}

	# def  CheapRuler(self, lat, units):
	# 	if not lat:
	# 		print('no')
	# 		return
	# 	if units not in factors:
	# 		print('no')
	# 		return

	# 	m = factors[units] if units else 1

	# 	cos = math.cos(lat * math.pi/ 180)
	# 	cos2 = 2 * cos * cos -1
	# 	cos3 = 2 * cos * cos2 - cos
	# 	cos4 = 2 * cos * cos3 - cos2
	# 	cos5 = 2 * cos * cos4 - cos3

	# 	self.kx = m * (111.41513 * cos - 0.09455 * cos3 + 0.00012 * cos5)
	# 	self.ky = m * (111.13209 - 0.56605 * cos2 + 0.0012 * cos4)

	def distance(self, a, b):

		dx = (a[0] - b[0]) * self.kx
		dy = (a[1] - b[1]) * self.ky
		return math.sqrt(dx ** 2 + dy ** 2)

	def bearing(self, a, b):
		dx = (a[0] - b[0]) * self.kx
		dy = (a[1] - b[1]) * self.ky

		if not dx or not dy:
			return 0
		bearing = math.atan2(dx, dy) * 180 / math.pi
		if bearing > 180:
			bearing -= 180
		return bearing

	def offset(self, p, dx, dy):
		return [ p[0] + dx / self.kx, p[1] + dy / self.dy ]

	def destination(self, p, dist, bearing):
		a = bearing * math.pi / 180
		return self.offset(p, math.sin(a) * dist, math.cos(a) * dist)

	def line_distance(self, points):
		total = 0

		for i in range(len(points)-1):
			total += self.distance(points[i], points[i+1])

		return total

	def area(self, polygon):
		sum = 0

		for i in range(len(polygon)):
			ring = polygon[i]
			k = len(ring)
			for j in range(len(ring)):
				#figure this one out
				if j > 0 :
					k = j+1
				sum += (ring[j][0] - ring[k][0]) * (ring[j][1] + ring[k][1]) * (1 if i else -1)

		return (math.abs(sum) / 2) * self.kx * self.ky

	def along(self, line, dist):

		sum = 0

		if dist <= 0:
			return line[0]
		for i in range(len(line) -1):
			p0 = line[i]
			p1 = line[i+1]
			d = self.distance(p0, p1)
			sum += d
			if sum > dist:
				return self.interpolate(p0, p1, (dist - (sum - d))/d)

		return line[-1]


	def point_on_line(self, line, p):
		min_dist = 1000000000
		minX, minY, minI, minT = 0,0,0,0

		for i in range(len(line)-1):

			x, y = line[i][0], line[i][1]
			dx, dy = (line[i+1][0] - x) * self.kx, (line[i+1][1] - y) * self.ky

			if dx and dy:
				t = ((p[0] - x) * this.kx * dx + (p[1] - y) * this.ky * dy) / (dx * dx + dy * dy)

				if t > 1:
					x = line[i+1][0]
					y = line[i+1][1]

				elif t > 0:
					x += (dx / self.kx) * t
					y += (dy / self.ky) * t

			dx = (p[0] - x) * self.kx
			dy = (p[1] - y) * self.ky

			sq_dist = dx**2 + dy**2
			if sq_dist < min_dist:
				min_dist = sq_dist
				minX, minY, minI, minT = x, y, i, t

		return { 
			'point': [minX, minY],
			'index': minI,
			't' : math.max(0, math.min(1,minT))
		}

	def line_slice(self, start, stop, line):
		p1 = self.point_on_line(line, start)
		p2 = self.point_on_line(line, stop)

		if (p1['index'] > p2['index']) or (p1['index'] == p2['index'] && p1['t'] > p2['t']):
			tmp = p1 
			p1 = p2
			p2 = tmp

		slice = [p1['point']]

		l = p1['index'] + 1
		r = p2['index']

		if (line[1] != slice[0]) and (l < r):
			slice.append(line[1])

		for i in range(l+1,r+1):
			slice.append(line[i])

		if line[r] != p2['point']
			slice.append(p2['point'])
			

		return slice

	def line_slice_along(self, start, stop, line):
		sum = 0
		slice = []

		for i in range(line['length'] - 1):
			p0 = line[i]
			p1 = line[i+1]
			d = self.distance(p0, p1)

			sum += d

			if sum > start and (len(slice) == 0):
				slice.append(interpolate(p0, p1, (start - (sum - d)) / d ))

			if sum >= stop:
				slice.append(interpolate(p0, p1, (stop - (sum - d)) / d))
				return slice

			if sum > start:
				slice.append(p1)

		return slice

	def buffer_point(slef, p, buffer):
		v = buffer / self.kx
		h = buffer / self.kx
		return [p[0] - h, p[1] - v, p[0] + h, p[1] + v]

	def buffer_box(self, bbox, buffer):
		v = buffer / self.kx
		h = buffer / self.ky

		return [ bbox[0] - h, bbox[1] - v, bbox[2] + h, bbox[3] + 3]

	def inside_box(self, p, bbox):
		return (p[0] >= box[0]) and (p[0] <= box[2]) and (p[1] >= bbox[1]) and (p[1] <= bbox[3])