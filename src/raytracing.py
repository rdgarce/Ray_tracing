import numpy as np
from multiprocessing import Pool
import time

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

class Camera:
    def __init__(self, position, screenHeight, screenWidth):
        self.position = np.array(position)
        self.width = screenWidth
        self.height = screenHeight
        self.ratio = screenWidth/screenHeight
        self.__init_screen()

    def __init_screen(self):
        self.screen = np.zeros((self.height, self.width, 3))
        self.screen[0,0] = self.position - np.array([1, -1/self.ratio, 1])
        self.screen[0, self.width-1] = self.position - np.array([-1, -1/self.ratio, 1])
        self.screen[self.height-1, 0] = self.position - np.array([1, 1/self.ratio, 1])
        
        # maybe useless
        #self.[self.height-1, self.width-1] = self.position - np.array([-1, 1/self.ratio, 1])

        colIncrement = (self.screen[0, self.width-1] - self.screen[0,0]) / self.width
        rowIncrement = (self.screen[self.height-1, 0] - self.screen[0,0]) / self.height

        self.screen[0] = np.linspace(self.screen[0,0], self.screen[0, self.width-1], self.width)

        for row in range(1,self.height):
            self.screen[row][0] = self.screen[row-1][0] + rowIncrement
            self.screen[row] = np.linspace(self.screen[row][0], self.screen[row][0] + self.width*colIncrement, self.width)

class Scene:
    def __init__(self, camera = None, light = None):
        self.objects = []
        self.light = light
        self.camera = camera
    
    def setCamera(self, sceneCamera):
        self.camera = sceneCamera

    def addObject(self, sceneObject):
        self.objects.append(sceneObject)
    
    def addLight(self, sceneLight):
        self.light = sceneLight

    def _ray_trace(self,screen_pixel_coord):
        origin = self.camera.position
        direction = normalize(screen_pixel_coord - origin)

        color = np.zeros((3))
        reflection = 1

        for k in range(self.max_ray_depth):
            # check for intersections
            nearest_object, min_distance = self._nearest_intersected_object(origin, direction)
            if nearest_object is None:
                break

            intersection = origin + min_distance * direction
            normal_to_surface = normalize(intersection - nearest_object.center)
            shifted_point = intersection + 1e-5 * normal_to_surface
            intersection_to_light = normalize(self.light.position - shifted_point)

            _, min_distance = self._nearest_intersected_object(shifted_point, intersection_to_light)
            intersection_to_light_distance = np.linalg.norm(self.light.position - intersection)
            is_shadowed = min_distance < intersection_to_light_distance

            illumination = np.zeros((3))

            if not is_shadowed:
                # ambient
                illumination += nearest_object.k_ambient * self.light.k_ambient
                # diffuse
                illumination += nearest_object.k_diffusion * self.light.k_diffusion * np.dot(intersection_to_light, normal_to_surface)
                # specular
                intersection_to_camera = normalize(self.camera.position - intersection)
                H = normalize(intersection_to_light + intersection_to_camera)
                illumination += nearest_object.k_specular * self.light.k_specular * np.dot(normal_to_surface, H) ** (nearest_object.shininess / 4)

            # reflection
            color += reflection * illumination
            reflection *= nearest_object.reflection

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)

        return np.clip(color, 0, 1)
    
    def _nearest_intersected_object(self, ray_origin, ray_direction):
        distances = [obj.intersect(ray_origin, ray_direction) for obj in self.objects]
        nearest_object = None
        min_distance = np.inf
        for index, distance in enumerate(distances):
            if distance and distance < min_distance:
                min_distance = distance
                nearest_object = self.objects[index]
        return nearest_object, min_distance
    
    def render(self, max_ray_depth, num_of_process = 1):
        
        if num_of_process <= 0:
            raise Exception("The minimum number of processes to render the scene is 1.")
        
        if self.camera == None:
            raise Exception("It's not possible to render the scene without a camera.")

        if self.light == None:
            raise Exception("It's not possible to render the scene without a light.")

        self.max_ray_depth = max_ray_depth
        print("Sarting the render with NUM_OF_PROCESS = {} and MAX_RAY_DEPTH = {} ...".format(num_of_process, self.max_ray_depth))
        image = np.zeros((self.camera.height, self.camera.width, 3))
        
        if num_of_process == 1:
            # single-process version
            start_time = time.time()
            image = np.apply_along_axis(self._ray_trace, 2, self.camera.screen)
            end_time = time.time()
            print("Render terminated. Elapsed time: {:.2f} s".format(end_time-start_time))
        else:
            # multi-process version
            start_time = time.time()
            with Pool(num_of_process) as p:
                image = np.array(
                            p.map(
                                self._ray_trace,
                                self.camera.screen.reshape((-1,3))
                                )
                            ).reshape(self.camera.screen.shape)
            end_time = time.time()
            print("Render terminated. Elapsed time: {:.2f} s".format(end_time-start_time))
        return image