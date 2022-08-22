# ConcaveHull
Convolutional kernel matrix for concave hull estimation

## Description
Demonstrates an algorithm for obtaining a concave hull of a point cloud that performs similarly to alphashape in roughly $\frac{1}{10}^{th}$ of the time. 
The basic algorithm is unstable, but takes about $\frac{1}{1000}^{th}$ of the time compared to alphashape (shown in the paper), so you can just keep trying until you 
find a rod length that works and still end up beating the currently accepted solution.

In the paper, I argue that the time-complexity of the fundamental algorithm is linear, but scales more like $\sqrt{N}$. Future work is to play with pytorch to see how fast it can go on a GPU.
