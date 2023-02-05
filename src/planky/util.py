import numpy as np

def next_start_angle(x,y):
    """
    Starting from (x0, y0), we move to (x1,y1).
    From this new point, we want to start the sweep
    45 degrees past the direction we came from so as not
    to include the previous location unless it is the only
    option.
    """
    a = angle_to(x, y) + np.pi*(0.6)
    if a<0:
        a += 2*np.pi
    return a

def angle_to(x, y):
    if x>0:
        a = np.arctan(y/x)
    elif x<0:
        a = np.pi + np.arctan(y/x)
    elif y>0:
        a = np.pi/2
    else:
        a = -np.pi/2
    if a<0:
        a += 2*np.pi
    return a