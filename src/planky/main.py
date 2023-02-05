import numpy as np

from .sweep_kernel import SweepKernel
from .util import next_start_angle


def find_hull(points, d=10):
    points = np.array(points)
    xmin, ymin = points.min(axis=0)
    xmax, ymax = points.max(axis=0)
    
    points -= [xmin, ymin]
    points += d+1
    
    grid = np.zeros(
        (
            xmax-xmin+d*2+2,
            ymax-ymin+d*2+2
        )
    )
    visited = grid.copy()
    
    grid[tuple(points.T)] = 1

    i = points.argmin(axis=0)[1]
    first = tuple(points[i])
    y, x = first
    dy, dx = 0,1

    sk = SweepKernel(d)

    polygon = []
    N = len(points)
    N_root = N**0.5
    n = 0
    h = 0
    while True:
        h += visited[y,x]
        n += 1
        polygon.append((y,x))
        visited[y,x]=1

        vision = grid[y-d:y+d+1, x-d:x+d+1]
        sk.rotate_to(next_start_angle(dx, dy))
        
        m = sk.kernel * vision
        i = m.max(axis=1).argmax()
        j = m[i].argmax()
        
        dy = d-i
        dx = j-d
        
        x+=dx 
        y-=dy
        
        if m[i,j]<=0 or h > 30 or n > N: return
        if (y, x) == first:
            if n < N_root: return
            return polygon