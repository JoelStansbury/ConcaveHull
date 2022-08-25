# ConcaveHull
Convolutional kernel matrix for concave hull estimation

## Description
Demonstrates an algorithm for obtaining a concave hull of a point cloud that performs similarly to alphashape in roughly $\frac{1}{10}^{th}$ of the time. 
The basic algorithm is unstable, but takes about $\frac{1}{1000}^{th}$ of the time compared to alphashape (shown in the paper), so you can just keep trying until you 
find a rod length that works and still end up beating the currently accepted solution.

In the paper, I argue that the time-complexity of the fundamental algorithm is linear, but could scale more like $\sqrt{N}$ with a few tweaks. Future work is to play with pytorch to see how fast it can go on a GPU.

The accompanying notebook has made a few advancements from the strategy discussed in the paper, but not really worth digging into. The big difference is that the `planky` function defined in the notebook actually works like you would hope, i.e. it just gives a single shape that seems like a good guess.
