![image](https://raw.githubusercontent.com/rdgarce/ray_tracing/main/renders/6spheres_1000x1500.png)
# Ray tracing for 3D scene render
A short and easy-to-use implementation of the ray tracing algorithm in python in the context of a 3D scene render.

## Why
*Ray tracing* has always been a buzzword for us, so we decided to explore computer graphics and lighting topics and create an educational, easy-to-use version of the ray tracing algorithm to render 3D scenes. This code is the result of our work.

## What is it
In a nutshell, it allows the user to do the followings:
1. Generate a 3D scene composed of objects and a light
2. Set a point of view of this scene, known as a *camera*
3. Render the scene, and so producing the image that an observer would have seen if looking at the scene from the point of view

## Features:
- Easy scene and object creation
- All screen resolutions
- Movable camera
- Multiprocessor support for the scene rendering

## Limitations:
- (Obviusly) Not feasable for real time applications
- Only one light source supported
- Only spheres are available as scene objects
- Only light reflection rays are taken into account
- Camera angles are fixed

## References:
[1] [Ray Tracing](https://it.wikipedia.org/wiki/Ray_tracing)\
[2] [Ray Tracing From Scratch in Python](https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9)\
[3] [Blinn–Phong reflection model](https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model)\
[4] [Advanced Lighting](https://learnopengl.com/Advanced-Lighting/Advanced-Lighting)
