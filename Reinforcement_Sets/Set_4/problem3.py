

'''
            SHAPE INTERFACE DESCRIPTION:

            
        def __init__(self, centroid: tuple[float,float]):
            Initializes the shape and intakes the centrid location of
            the shape and saves it as an attribute to self, the function
            can have more parameters but the first one should always be the centroid
            as a tuple of two floats.

        def move_shape(self, new_location: tuple(float, float))-> None:
            This function intakes a tuple of two floats which are the new location of the shape.
            Move the shape and update its centroid to be the new location, return None.

        def calculate_area()-> float:
            This function should use values from the attributes of the object
            to handle the calculations of the size of the specific shape, then
            return the area of the shape as a positive float.

        def calculate_perimeter()-> float:
            This function should use the object's attributes to the determine
            the perimeter of the shape within it's respective scale, and return
            that value as a positive float.

        def within_bounds(point: tuple[float, float])-> bool:
            This function takes in a tuple of two floats that represent
            the location of a point. The function should return whether the point is
            inside the area encovered by the shape, e.g. a circle centerd at
            (0,0) with radius of 5 units is asked if (0,1) is within bounds, it should return true
            if the point is (0,5) it should also be true, which means that the boarders of
            the shape count.

'''

import math
from collections import namedtuple

Point = namedtuple('Point', ['x','y'])

class Circle:

    def __init__(self, centroid: tuple[float,float], radius: float):
        self._centroid = Point(centroid[0], centroid[1])
        self._radius = radius


    def move_shape(self, new_location: tuple[float, float])-> None:
        self._centroid = Point(new_location[0], new_location[1])


    def calculate_area(self)-> float:
        return math.pi * self._radius**2
    

    def calculate_perimeter(self)-> float:
        return 2 * math.pi * self._radius
    

    def within_bounds(self, point: tuple[float, float])-> bool:
        point_distance = self._vector_distance(self._centroid, Point(point[0], point[1]))

        if self._radius >= point_distance:
             return True

        return False


    def _vector_distance(self, origin: Point, target: Point)-> float:

        new_vector = Point(target.x - origin.x, target.y - origin.y)

        magnitute = math.sqrt(new_vector.x**2 + new_vector.y**2)

        return magnitute
    
Vertices = namedtuple("Vertices", ['top_right', 'top_left', 'bottom_right','bottom_left'])

class Rectangle:

    def __init__(self, centroid: tuple[float,float], height: float, width: float):
        self._centroid = Point(centroid[0], centroid[1])
        self._height = height
        self._width = width
        
        top_right = Point(self._centroid.x + height/2, self._centroid.y + height/2)
        top_left = Point(self._centroid.x - height/2, self._centroid.y + height/2)
        bottom_right = Point(self._centroid.x + height/2, self._centroid.y - height/2)
        bottom_left = Point(self._centroid.x - height/2, self._centroid.y - height/2)

        self._vertices = Vertices(top_right, top_left, bottom_right, bottom_left)


    def move_shape(self, new_location: tuple[float, float])-> None:
        target = Point(new_location[0],new_location[1])

        x_shift = target.x - self._centroid.x
        y_shift = target.y - self._centroid.y

        self._centroid = target

        new_top_right = Point(self._vertices.top_right.x + x_shift, self._vertices.top_right.y + y_shift)
        new_top_left = Point(self._vertices.top_left.x + x_shift, self._vertices.top_left.y + y_shift)
        new_bottom_right = Point(self._vertices.bottom_right.x + x_shift, self._vertices.bottom_right.y + y_shift)
        new_bottom_left = Point(self._vertices.bottom_left.x + x_shift, self._vertices.bottom_left.y + y_shift)

        self._vertices = Vertices(new_top_right, new_top_left, new_bottom_right, new_bottom_left)
            

    def calculate_area(self)-> float:
        return self._height * self._width
    

    def calculate_perimeter(self)-> float:
        return (self._height * 2) + (self._width * 2)
    

    def within_bounds(self, point: tuple[float, float])-> bool:
        point = Point(point[0], point[1])

        point_distance = self._vector_difference(self._centroid, point)

        if self._height/2 >= abs(point_distance.x) and self._width/2 >= abs(point_distance.y):
             return True

        return False


    def _vector_difference(self, origin: Point, target: Point)-> Point:

        new_vector = Point(target.x - origin.x, target.y - origin.y)

        return new_vector


def sum_areas(shapes: list['Shapes'])-> float:

    sum_areas = 0

    for shape in shapes:
        sum_areas += shape.calculate_area()

    return sum_areas


def _testing_shapes()-> None:

    circle_one = Circle((0,0), 5)
    circle_one.move_shape((5,5))
    assert round(circle_one.calculate_area(), 4) == 78.5398
    assert round(circle_one.calculate_perimeter(), 4) == 31.4159
    assert circle_one.within_bounds((6,6)) == True
    assert circle_one.within_bounds((20,50)) == False
    
    circle_two = Circle((-4,3), 8)
    assert round(circle_two.calculate_area(), 4) == 201.0619
    assert round(circle_two.calculate_perimeter(), 4) == 50.2655
    assert circle_two.within_bounds((6,6)) == False
    assert circle_two.within_bounds((-2,-1)) == True

    circle_two.move_shape((-100,-250))
    assert circle_two.within_bounds((6,6)) == False
    assert circle_two.within_bounds((-2,-1)) == False

    rectangle_one = Rectangle((0,0), 10, 7)
    assert round(rectangle_one.calculate_area(), 4) == 70
    assert round(rectangle_one.calculate_perimeter(), 4) == 34
    assert rectangle_one.within_bounds((3,3.5)) == True
    assert rectangle_one.within_bounds((-2,-1)) == True

    rectangle_one.move_shape((-8,5))
    assert rectangle_one.within_bounds((3,3.5)) == False
    assert rectangle_one.within_bounds((-2,-1)) == False

    rectangle_two = Rectangle((-1,0), 50, 2)
    assert round(rectangle_two.calculate_area(), 4) == 100
    assert round(rectangle_two.calculate_perimeter(), 4) == 104
    assert rectangle_two.within_bounds((6,6)) == False
    assert rectangle_two.within_bounds((-2,-1)) == True

    rectangle_two.move_shape((-100,-250))
    assert rectangle_two.within_bounds((6,6)) == False
    assert rectangle_two.within_bounds((-2,-1)) == False

    list_shapes = [circle_one, circle_two, rectangle_one, rectangle_two]

    assert round(sum_areas(list_shapes), 4) == 78.5398 + 201.0619 + 70 + 100


if __name__ == "__main__":

    _testing_shapes()

    








        
