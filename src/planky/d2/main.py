import numpy as np

from .kernel import SweepKernel
from .util import next_start_angle


def find_hull(points, d=10):
    points = np.array(points)
    xmin, ymin = points.min(axis=0)
    xmax, ymax = points.max(axis=0)
    
    N = len(points)
    
    points -= [xmin, ymin]
    points += d + 1
    
    grid = np.zeros(
        (
            xmax-xmin+d*2+2,
            ymax-ymin+d*2+2
        )
    )
    
    grid[tuple(points.T)] = 1

    i = points.argmin(axis=0)[1]
    y, x = tuple(points[i])
    dy, dx = 0, 1

    sk = SweepKernel(d)

    n = 0
    
    steps = {}
    while True:
    
        n += 1
        new_angle = next_start_angle(dx,dy)
        
        sk.rotate_to(new_angle)
        i, j = sk.apply(grid[y-d:y+d+1, x-d:x+d+1])
        
        dy = d-i
        dx = j-d
        
        if ((y,x) in steps) and (steps[(y,x)]==(y-dy, x+dx)):
            res = []
            _last, _next = (y,x), steps[(y,x)]
            while _next != (y,x):
                res.append(_last)
                _last, _next = _next, steps[_next]
            res.append(_next)
            return res

        steps[(y,x)]=(y-dy, x+dx)
        x+=dx
        y-=dy
        if n > N: return []
