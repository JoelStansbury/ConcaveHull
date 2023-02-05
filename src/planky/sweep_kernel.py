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

        # Used to keep the corners of the box at 0
        self.mask = mask

        # Current angle of the rod
        self.angle = starting_angle

        # Distance based multiplier to incentivise larger steps
        self.d_mult = (dist/d**2)/100
    
    def rotate_to(self, angle):
        self.rotate(angle-self.angle)
        self.angle=angle
    
    def rotate(self, angle):
        self.angle -= angle
        if self.angle < 0: self.angle += 2*np.pi
        if self.angle >= 2*np.pi: self.angle -= 2*np.pi
        self.kernel -= angle
        self.kernel[self.kernel > 2*np.pi] -= 2*np.pi
        self.kernel[self.kernel < 0] += 2*np.pi
        self.kernel[self.mask] = 0
    
    def apply(self, a):
        m = self.kernel * a + self.d_mult
        x = m.max(axis=1).argmax()
        y = m[x].argmax()
        return x, y
