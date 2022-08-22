# ConcaveHull
Convolutional kernel matrix for concave hull estimation

## Description
Demonstrates an algorithm for obtaining a concave hull of a point cloud that performs similarly to alphashape in roughly $\frac{1}{10}^{th}$ of the time. 
The basic algorithm is unstable, but takes about $\frac{1}{1000}^{th}$ of as long as alphashape (shown in the paper) that you can keep trying until you 
find a rod length that works and still end up beating alphashape.