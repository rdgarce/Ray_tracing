import numpy as np

class Sphere:
    def __init__(self, center, radius, k_ambient, k_diffusion, k_specular, shininess, reflection):
        self.center = center
        self.radius = radius
        self.k_ambient = np.array(k_ambient)
        self.k_diffusion = np.array(k_diffusion)
        self.k_specular = np.array(k_specular)
        self.shininess = shininess
        self.reflection = reflection
    
    """
    Returns the t value of the intersection between the sphere and the Ray [ray].
    Returns None if no intersection exists
    """
    def intersect(self, ray_origin, ray_direction):
        b = 2 * np.dot(ray_direction, ray_origin - self.center)
        c = np.linalg.norm(ray_origin - self.center) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None

class Light:
    def __init__(self, position, k_ambient, k_diffusion, k_specular):
        self.position = np.array(position)
        self.k_ambient = np.array(k_ambient)
        self.k_diffusion = np.array(k_diffusion)
        self.k_specular = np.array(k_specular)