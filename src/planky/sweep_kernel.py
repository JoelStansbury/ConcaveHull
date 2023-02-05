import numpy as np

from .util import angle_to

class SweepKernel:
    def __init__(self, length: int, starting_angle: float = 0):
        """
        Generates a kernel to simulate a sweeping action
        in which a plank starts at a certain angle wrt the positive
        x axis and rotates clockwise 360 degrees
        """
        d = (2*length)+1
        kernel = np.zeros((d, d))
        dist = np.zeros((d, d))
        for y in range(length, -length-1, -1):
            for x in range(-length, length+1, 1):
                i = length - y
                j = x - length - 1
                kernel[i,j] = angle_to(x,y)
                dist[i,j] = x**2+y**2
        mask = dist > length**2
        mask[length,length] = 1
        kernel -= starting_angle
        kernel[kernel>2*np.pi] -= 2*np.pi
        kernel[kernel<0] += 2*np.pi
        kernel[mask] = 0
        self.kernel = kernel
        self.mask = mask
        self.angle = starting_angle
    
    def rotate_to(self, angle):
        self.rotate(self.angle - angle)
    
    def rotate(self, angle):
        self.angle -= angle
        self.kernel -= angle
        self.kernel[self.kernel > 2*np.pi] -= 2*np.pi
        self.kernel[self.kernel < 0] += 2*np.pi
        self.kernel[self.mask] = 0
