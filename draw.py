from display import *
from matrix import *
from math import *

def add_box(points, x, y, z, width, height, depth, step):
	p = new_matrix()
	print_matrix(p)
	generate_box(p, x, y, z, width, height, depth, step)
	for i in range(4, len(p)):
		add_edge(points, p[i][0], p[i][1], p[i][2], p[i][0], p[i][1], p[i][2])
	#print_matrix(points)

def generate_box( points, x, y, z, width, height, depth, step ):
	i = 0
	#width
	stop = width
	while i < stop:
		add_point(points, x + i, y, z)
		add_point(points, x + i, y - height, z)
		add_point(points, x + i, y, z - depth)
		add_point(points, x + i, y - height, z - depth)
		i+=step
	#height
	i = 0
	stop = height
	while i < stop:
		add_point(points, x, y-i, z)
		add_point(points, x + width, y-i, z)
		add_point(points, x + width, y-i, z - depth)
		add_point(points, x, y-i, z - depth)
		i+= step
	#depth
	i = 0
	stop = depth
	while i < stop:
		add_point(points, x, y, z - i)
		add_point(points, x+width, y, z - i)
		add_point(points, x, y-height, z - i)
		add_point(points, x+width, y-height, z - i)
		i+= step

def add_sphere( points, cx, cy, cz, r, step ):
	p = new_matrix()
	#print_matrix(p)
	generate_sphere(p, cx, cy, cz, r, step)
	for i in range(4, len(p)):
		add_edge(points, p[i][0], p[i][1], p[i][2], p[i][0], p[i][1], p[i][2])
	#print_matrix(points)

def generate_sphere( points, cx, cy, cz, r, step ):
	rotation = 0
	circle = 0
	mpi = math.pi
	while rotation < 1:
		rpi = mpi * rotation * 2
		circle = 0
		while circle < 1:
			cpi = mpi * circle
			x = r * math.cos(cpi) + cx
			y = r * math.sin(cpi) * math.cos(rpi) + cy
			z = r * math.sin(cpi) * math.sin(rpi) + cz
			add_point(points, x, y, z)
			if (x == 1):
				print circle
			circle += step
		rotation += step

def add_torus( points, cx, cy, cz, r0, r1, step ):
	p = new_matrix()
	generate_torus(p, cx, cy, cz, r0, r1, step)
	for i in range(4, len(p)):
		add_edge(points, p[i][0], p[i][1], p[i][2], p[i][0], p[i][1], p[i][2])

def generate_torus( points, cx, cy, cz, r0, r1, step ):
	#FAQ:
	#Q: Why does this look like a copy/paste of generate_sphere?
	#A: Don't you have things to be doing?
	rotation = 0
	circle = 0
	mpi = math.pi
	while rotation < 2 * mpi:
		rpi = mpi * rotation * 2
		circle = 0
		while circle < 2 * mpi:
			cpi = mpi * circle
			x = (math.cos(rotation) * (r0 * math.cos(circle) + r1)) + cx
			y = r0 * math.sin(circle) + cy
			z = -1 * (math.sin(rotation) * (r0 * math.cos(circle) + r1)) + cz
			add_point(points, x, y, z)
			circle += step
		rotation += step

def draw_points(matrix, screen, color):
	for i in range(len(matrix)):
		plot(screen, color, int(matrix[i][0]), int(matrix[i][1]))

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    t = step

    while t <= 1.00001:
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    t = step
    while t <= 1.00001:
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )




def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
