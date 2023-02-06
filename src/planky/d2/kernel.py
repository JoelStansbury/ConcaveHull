import numpy as np
from shapely.geometry.polygon import Polygon
import torch

from .util import angle_to

class SweepKernel:
    def __init__(self, length: int, starting_angle: float = 0):
        """
        Generates a kernel to simulate a sweeping action
        in which a plank starts at a certain angle wrt the positive
        x axis and rotates clockwise 360 degrees
        """
        d = (2*length)+1
        kernel = torch.from_numpy(np.zeros((d, d)))
        dist = np.zeros((d, d))
        for y in range(length, -length-1, -1):
            for x in range(-length, length+1, 1):
                i = length - y
                j = x - length - 1
                kernel[i,j] = angle_to(x,y)
                dist[i,j] = x**2 + y**2

        mask = torch.from_numpy(dist > length**2)
        mask[length,length] = 1
        kernel -= starting_angle
        kernel[kernel>2*np.pi] -= 2*np.pi
        kernel[kernel<0] += 2*np.pi
        kernel[mask] = 0

        self.kernel = kernel

        # Used to keep the corners of the box at 0
        self.mask = mask

        # Current angle of the rod
        self.angle = starting_angle

        # Distance based multiplier to incentivise larger steps
        self.d_mult = torch.from_numpy((dist/d**2)/100)

        # Angle at which the sweeping edge trails behind the vector of motion
        # pi/2 indicates that the edge should start tangent to the last vector of motion.
        # Values larger than this will tilt the edge back towards the previous point.
        self.trail = np.pi * (0.6)

        self.L = length
    
    def rotate_to(self, angle):
        self.rotate(angle-self.angle)
        self.angle=angle
    
    def rotate(self, angle):
        self.angle -= angle
        self.kernel -= angle
        self.kernel[self.kernel > 2*np.pi] -= 2*np.pi
        self.kernel[self.kernel < 0] += 2*np.pi
        self.kernel[self.mask] = 0
    
    def apply(self, a):
        m = self.kernel * a + self.d_mult
        x,y = np.unravel_index(torch.argmax(m), m.shape)
        return x, y

    def next_start_angle(self, x, y):
        """
        Starting from (x0, y0), we move to (x1,y1).
        From this new point, we want to start the sweep
        45 degrees past the direction we came from so as not
        to include the previous location unless it is the only
        option.
        """
        a = angle_to(x, y) + self.trail
        if a<0:
            a += 2 * np.pi
        return a

    def fit(self, points):
        points = np.array(points)
        xmin, ymin = points.min(axis=0)
        xmax, ymax = points.max(axis=0)
        
        
        points -= [xmin, ymin]
        points += self.L + 1
        
        grid = torch.from_numpy(np.zeros(
            (
                xmax - xmin + self.L * 2 + 2,
                ymax - ymin + self.L * 2 + 2
            )
        ))
        
        grid[tuple(points.T)] = 1

        i = points.argmin(axis=0)[1]
        y, x = tuple(points[i])
        dy, dx = 0, 1
        s = grid.shape
        return self._mainloop(
            grid,
            np.ones(shape=(s[0], s[1], 2), dtype=np.int32) -2, 
            [y, x], 
            [dy, dx], 
            len(points)
        )

    def _mainloop(self, grid, steps, last, vec, N):
        y,x = last
        dy,dx = vec
        n=0
        L = self.L
        
        while n<N:
            n += 1
            self.rotate_to(self.next_start_angle(dx,dy))
            i, j = self.apply(grid[y-L:y+L+1, x-L:x+L+1])
            
            dy = L-i
            dx = j-L
            
            if list(steps[y, x]) == [y-dy, x+dx]:
                return self.to_poly(steps, [y,x])

            steps[y, x] = [y-dy, x+dx]
            x+=dx
            y-=dy
    
    def to_poly(self, steps, start):
        y,x = start
        res = []
        _last, _next = [y,x], list(steps[y, x])
        while not list(_next) == [y,x]:
            res.append(_last)
            _last, _next = _next, list(steps[_next[0],_next[1]])
        res.append(_next)
        return Polygon(res)