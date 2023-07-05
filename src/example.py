from raytracing import Scene,Camera
from objects import Sphere,Light
import matplotlib.pyplot as plt
from os import cpu_count

if __name__ == '__main__':

    scena = Scene(Camera((0,0,1),1000,1500))

    sfera1 = Sphere((0.0, 0.2, -1.5), 0.6,        (0, 0.1, 0.1),     (0, 0.6, 0),     (1, 1, 1), 100, 0.5)
    sfera2 = Sphere((-0.3, 0, 0),     0.1,        (0, 0.1, 0.1),     (0.7, 0, 0.7),   (1, 1, 1), 100, 0.5)   
    sfera3 = Sphere((0.1, -0.3, 0),   0.15,       (0.255, 0.0, 0.0), (0.7, 0, 0),     (1, 1, 1), 100, 0.5)
    sfera4 = Sphere((0, -9000, 0),    9000 - 0.7, (0.1, 0.1, 0.1),   (0.6, 0.6, 0.6), (1, 1, 1), 100, 0.1)

    luce1 = Light((5, 5, 5), (1, 1, 1), (1, 1, 1), (1, 1, 1))

    scena.addObject(sfera1)
    scena.addObject(sfera2)
    scena.addObject(sfera3)
    scena.addObject(sfera4)

    scena.addLight(luce1)

    image = scena.render(3,int(cpu_count()/2))

    plt.imshow(image)
    plt.show()