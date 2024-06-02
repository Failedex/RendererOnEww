import numpy as np 
import time
import math
import json

WIDTH, HEIGHT = (640, 360)

def rotate(point, x, y, z):
    rotx = np.array([
        [1, 0, 0],
        [0, math.cos(x), -math.sin(x)],
        [0, math.sin(x), math.cos(x)],
    ])
    point = np.matmul(rotx, point)

    roty = np.array([
        [math.cos(y), 0, math.sin(y)],
        [0, 1, 0],
        [-math.sin(y), 0, math.cos(y)],
    ])
    point = np.matmul(roty, point)

    rotz = np.array([
        [math.cos(z), -math.sin(z), 0],
        [math.sin(z), math.cos(z), 0],
        [0, 0, 1],
    ])
    point = np.matmul(rotz, point)
    return point

def main():
    points = []
    connections = []

    center = np.array([WIDTH//2, HEIGHT//2, 0])

    thickness = 30
    radius = 60
    i = 0
    poly = 8
    for theta in np.arange(0, 2*np.pi, np.pi*(2/poly)):
        point = np.array([0, thickness*np.sin(theta), thickness*np.cos(theta)])
        point -= np.array([0, radius, 0])
        points.append(point)
        connections.append((i, (i+1)%poly))
        connections.append((i, (i+poly)%(poly*poly)))
        i += 1

    for j, theta in enumerate(np.arange(np.pi*(2/poly), 2*np.pi, np.pi*(2/poly))):
        for i in range(poly): 
            p = points[i]
            p = rotate(p, 0, 0, theta)
            points.append(p)
            ii = i+(j+1)*poly
            if j % 2 == 1:
                connections.append((i+(j+1)*poly, ((i+1)%poly)+(j+1)*poly))
            connections.append((ii, (ii+poly)%(poly*poly)))

    for p in points:
        p += center

    while True: 

        ppoints = {"points": [], "lines": []}
        for i, p in enumerate(points):
            p -= center 
            p = rotate(p, 0.03, 0.03, 0.03)
            p += center

            points[i] = p
            # ppoints["points"].append(list(map(int, p)))


        for a, b in connections: 
            # I find that rotating from the center is probably the easiest way
            midx = int((points[a][0]+points[b][0])/2)
            midy = int((points[a][1]+points[b][1])/2)
            length = (abs(points[a][0]-points[b][0])**2 + abs(points[a][1]-points[b][1])**2)**0.5

            if length == 0:
                continue

            # mega scuffed trigonometry
            if points[a][0]-points[b][0] == 0:
                angle = 25
            else:
                oa = (points[a][1]-points[b][1])/(points[a][0]-points[b][0])
                angle = math.atan(oa) * 50/math.pi

            ppoints["lines"].append([midx, midy, angle, length])

        print(json.dumps(ppoints), flush=True)

        # Eww is not enjoying this lmao
        time.sleep(1/20)
main()
