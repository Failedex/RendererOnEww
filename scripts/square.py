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
    points = [
        np.array([100,100,100]),
        np.array([200,100,100]),
        np.array([200,200,100]),
        np.array([100,200,100]),

        np.array([100,100,200]),
        np.array([200,100,200]),
        np.array([200,200,200]),
        np.array([100,200,200]),
    ]

    connections = [
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7), 
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4)
    ]

    # get center point (avg point)
    center = np.array([0, 0, 0])

    for p in points:
        center += p

    center = center/len(points)

    while True: 

        ppoints = {"points": [], "lines": []}
        for i, p in enumerate(points):
            p = p - center 
            p = rotate(p, 0.01, 0.01, 0.01)
            p = p + center

            points[i] = p
            # ppoints["points"].append(list(map(int, p)))


        for a, b in connections: 
            midx = int((points[a][0]+points[b][0])/2)
            midy = int((points[a][1]+points[b][1])/2)
            length = (abs(points[a][0]-points[b][0])**2 + abs(points[a][1]-points[b][1])**2)**0.5

            if length == 0:
                continue

            if points[a][0]-points[b][0] == 0:
                angle = 25
            else:
                oa = (points[a][1]-points[b][1])/(points[a][0]-points[b][0])
                angle = math.atan(oa) * 50/math.pi

            ppoints["lines"].append([midx, midy, angle, length])

        print(json.dumps(ppoints), flush=True)
        time.sleep(1/30)
main()
