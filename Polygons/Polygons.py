import sys
import matplotlib
matplotlib.use('Agg')
import random
import math
import string
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

hatches = ('-', '+', 'x', '\\', '*', 'o', 'O', '.', '/', '|')

# Any polygon with more number of points will be considered a circle
CIRCLE_LIMIT_POINT = 100
CANVAS_SIZE = 10
IRREGULAR_ANGLE = math.pi / 6

def rnd(zeroToOne=0):
    # if zeroToOne is 1, returns a number between 0 and 1 (inclusive)
    # else returns a number between -1 and 1 (inclusive)
    if zeroToOne == 1:
        return random.random()
    else:
        if round(random.random()) == round(0):
            # if generated number between 0 and 0.5
            return random.random()
        else:
            return random.random() * -1

def rndangle():
    # return a random angle [in radians] between 0 and 360 deg
    return rnd(1) * 2 * math.pi

def getpoints(R, theta, Xcenter, Ycenter):
    # finds the new points on circle, with radius R, center (Xcenter,Ycenter), at an angle theta
    return ((Xcenter + (R * math.cos(theta))), (Ycenter + (R * math.sin(theta))))

# Circumcircle - has a radius and a x,y coordinates for the center
class Circumcircle:
    def __init__(self, size, centerx, centery):
        self.radius = size
        self.x = centerx
        self.y = centery

    def __repr__(self):
        return "Circumcircle: radius %s, Center: (%s,%s)" % (self.radius, self.x, self.y)

# Represents a shape
class Polygon:

    @staticmethod
    def getHatches():
        return ['-', '+', 'x', '\\', '*', 'o', 'O', '.', '/', '|']

    def __init__(self, no_of_sides=4, size=30, isRegular=True, hatch=None, circumcircle=None):
        self.size = size
        self.N = no_of_sides
        if isRegular == 'any':
            self.isRegular = random.choice([True, False])
        else:
            self.isRegular = isRegular
        self.points = []

        self.circumcircle = circumcircle

        if hatch == 'random':
            self.hatch = hatches[int(random.random() * len(hatches))]
        else:
            self.hatch = hatch

        # for alphabet
        # in deg
        self.alphabet_rotation = 0
        self.alphabet = None

        # The angles at which each point was drawn
        # This will be helpful in case of rotating and other things (I can't think of right now.)
        self.point_angles = []

    '''
    This shape is drawn randomly
    considering this as the first shape to be drawn

    makeRandomCircumcircle: makes a Circumcircle with random Center
    '''

    def makeRandomCircumcircle(self):
        # The shape is randomly drawn
        # Step1 : Make the circumcircle randomly

        # generate center points between 0 and 100
        self.circumcircle = Circumcircle(self.size, round(rnd(zeroToOne=1) * CANVAS_SIZE), round(rnd(zeroToOne=1) * CANVAS_SIZE))
        # print "Random Circumcircle",self.circumcircle

        # Step2 :  Then call makeShape()
        self.makeShape()

    """
    Given a Circumcircle and No_of_points generate points for the
    polygon
    """

    def makeShape(self):
        # Uses the information - circumcircle(radius,x,y) + no_of_sides + isRegular to generate vertices
        # for the polygon

        # Start with empty lists of points
        self.points = []
        self.point_angles = []

        # Pick a random angle
        start_angle = rndangle()
        if self.N == 0:
            # A circle
            # No need to generate points
            pass
        elif self.N == 1:
            # The center of the circumcircle is the point
            # No need to generate points
            # pass
            if self.alphabet is None:
                self.type = 'alpha'
                self.alphabet = random.choice(
                    list(string.ascii_letters) + [u'\u2605', u'\u25DF', u'\u2020', u'\u002B'])
            pass
        elif self.N == 2:
            # An arrow
            # Two points that are opposite to each other
            self.point_angles = [start_angle, start_angle + math.pi]
            self.gen_points()
        elif self.isRegular:
            # Then theta is incremented uniformly by 360/N
            angle_increment = 2 * math.pi / self.N

            # Add points
            for i in range(self.N):
                cur_angle = start_angle + i * angle_increment
                self.point_angles.append(cur_angle)
                self.points.append(getpoints(
                    self.circumcircle.radius, cur_angle, self.circumcircle.x, self.circumcircle.y))

        else:
            # Then theta is incremented by randangle
            # NOTE: A minimum value should be defined for increment,
            # otherwise the generated points would be too close to
            # each other
            # NOTE: We need to be sure that all points are unique!!

            # Currently increment with one of the values in angle_increment
            # angle_increment = [math.pi / 8, 2*math.pi / 6 ]

            self.points = []
            self.point_angles = []

            angle_increment = 2 * math.pi / self.N
            # Add points
            for i in range(self.N):
                cur_angle = start_angle + i * angle_increment
                # Now modify the generated angles a little bit
                # We increment/decrement angle by any number between 0 and 30 degrees
                cur_angle += random.random() * IRREGULAR_ANGLE * \
                    (-1 if random.random() < 0.5 else 1)
                self.point_angles.append(cur_angle)

            self.gen_points()

        # point_angles can be any possible angles between [start_angle , start_angle + 2*pi].
        # it's better to convert them between 0 and 2*math.pi
        # To standardize the point angles generated, subtract 2*pi from any angle that was generated
        # if it is greater than 2*pi and then sort (sorting is not required but we just want to keep it in a way that
        # all angles are in increasing order between 0 and 2*pi)
        for i in range(len(self.point_angles)):
            if self.point_angles[i] > 2 * math.pi:
                self.point_angles[i] -= 2 * math.pi

    def setSize(self, size=10):
        self.circumcircle.radius = size

    def setHatch(self, hatch=''):
        self.hatch = hatch

    def isCircle(self):
        return self.N == 0 or self.N > CIRCLE_LIMIT_POINT

    def drawPolygon(self):
        points = self.points

        if self.N == 0:
            self.drawCircle()
        elif self.N == 1:
            plt.gca().text(self.circumcircle.x, self.circumcircle.y, self.alphabet,
                           # rotation value should in degrees
                           rotation=self.alphabet_rotation * (180 / math.pi),
                           fontsize=self.size, color='black',
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center',
                           )

        elif self.N == 2:
            self.drawArrow()
        else:
            # FOR POLYGONS
            fill = False
            if not self.hatch:
                # don't do anything
                hatch = None
            elif self.hatch == 'random':
                # pick a random hatch
                hatch = hatches[int(random.random() * len(hatches))]
                self.hatch = hatch
            else:
                hatch = self.hatch

            polygon = plt.Polygon(points, fill=fill, hatch=hatch)
            plt.gca().add_patch(polygon)

    def drawCircle(self):
        if not self.hatch:
            # don't do anything
            hatch = None
        elif self.hatch == 'random':
            # pick a random hatch
            hatch = hatches[int(random.random() * len(hatches))]
            self.hatch = hatch
        else:
            hatch = self.hatch

        circle = plt.Circle((self.circumcircle.x, self.circumcircle.y),
                             self.circumcircle.radius, fill=False, hatch=hatch)
        plt.gca().add_patch(circle)

    def drawArrow(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        dx, dy = x2 - x1, y2 - y1

        # FIX make head_width and head_length relative to something so that it scales.
        plt.arrow(x1, y1, dx, dy, head_width=abs(min(dx, dy) * 0.1),
                  head_length=abs(min(dx, dy) * 0.1), fc='k', ec='k')

    '''
    Generate this object outside the poly
    '''

    def gen_outside(self, otherpoly):
        # otherpoly should be a polygon
        if not type(otherpoly) == type(self):
            # raise error
            print("Something is wrong: Wrong type" + type(self))
        else:
            total_distance = otherpoly.circumcircle.radius + \
                self.size  # +some_random_distance
            # Get a random angle to draw the new image
            draw_angle = rndangle()
            self.gen_point_angles()
            self_center = getpoints(
                total_distance, draw_angle, otherpoly.circumcircle.x, otherpoly.circumcircle.y)
            self.circumcircle = Circumcircle(
                self.size, self_center[0], self_center[1])
            self.gen_points()

    def move_outside(self, otherpoly):
        pass

    '''
    Generate this object outside the poly
    '''

    def gen_outside_all(self, *otherpolys):
        for i in otherpolys:
            assert (type(i) == type(self))

        common_center_x = sum(
            [poly.circumcircle.x for poly in otherpolys]) / len(otherpolys)
        common_center_y = sum(
            [poly.circumcircle.y for poly in otherpolys]) / len(otherpolys)
        distance = self.size + sum([poly.size for poly in otherpolys])

        # Get a random angle to draw the new image
        draw_angle = rndangle()

        self_center = getpoints(distance, draw_angle,
                                common_center_x, common_center_y)
        self.circumcircle = Circumcircle(
            self.size, self_center[0], self_center[1])

        # Generate points for otherpoly
        self.makeShape()

    '''
    Generate this object inside the otherpoly
    '''

    def gen_inside(self, otherpoly):
        self.circumcircle = Circumcircle(
            otherpoly.circumcircle.radius / 2, otherpoly.circumcircle.x, otherpoly.circumcircle.y)
        self.makeShape()

    def move_inside(self, otherpoly):
        pass

    def rotate(self, theta=math.pi / 2):
        if self.N == 1:
            # Alphabet rotation should be in degrees
            # theta here is in rads as for everything else
            self.alphabet_rotation += theta

        elif not self.isCircle():
            # rotate the current polygon clockwise by theta
            self.points = []
            # Find new points drawn at new angles.
            for cur_angle in self.point_angles:
                self.points.append(getpoints(self.circumcircle.radius, cur_angle + theta,
                                             self.circumcircle.x, self.circumcircle.y))

            # Update the angles at which vertices are drawn
            self.point_angles = [cur_angle +
                                 theta for cur_angle in self.point_angles]

    def add_vertex(self):
        if not self.isCircle():
            # Add a random vertex to the figure
            self.N += 1
            self.makeShape()

    def delete_vertex(self):
        if not self.isCircle():
            if self.N <= 3:
                # Can't do nothing
                raise Exception("Error: Polygon can't exist with less than 3 vertices")
            else:
                self.N -= 1
                self.makeShape()

    """
    Change the circumcircle for the Polygon
    """

    def clone_circumcircle(self, otherpoly):
        self.circumcircle = Circumcircle(
            otherpoly.circumcircle.radius, otherpoly.circumcircle.x, otherpoly.circumcircle.y)
        self.makeShape()

    """
    Flip the image
    how : vert - about vertical axis
          hori - about horizontal axis
    """

    def flip(self, how='vert'):
        if self.N == 1:
            # Alphabet
            if how == 'vert':
                self.alphabet_rotation = 'vertical'
            else:
                self.alphabet_rotation = 'horizontal'

        elif not self.isCircle():
            pts = []
            if how == 'vert':
                for pt in self.points:
                    x, y = pt
                    xdist = self.circumcircle.x - x

                    x, y = 2 * self.circumcircle.x - x, y
                    pts.append((x, y))
            elif how == 'hori':
                for pt in self.points:
                    x, y = pt
                    x, y = x, 2 * self.circumcircle.y - y
                    pts.append((x, y))

            # Update the points
            self.points = pts

            # Points updated so update the angles as well
            self.gen_point_angles()

    def gen_point_angles(self):
        # Given the points are generated, find the angles in which they were
        # generated.
        if not self.isCircle():
            point_angles = []
            for pt in self.points:
                x, y = pt
                angle = math.atan2(y - self.circumcircle.y,
                                    x - self.circumcircle.x)
                if angle < 0:
                    angle = (2 * math.pi) + angle
                point_angles.append(angle)

            self.point_angles = point_angles

    def get_point_angles(self):
        self.gen_point_angles()
        return self.point_angles

    def gen_points(self):
        if not self.isCircle():
            # Given point angles and the circumcircle, draw
            self.points = []
            for angle in self.point_angles:
                self.points.append(getpoints(self.circumcircle.radius, angle,
                                             self.circumcircle.x, self.circumcircle.y))

    def swap_polygons(self, otherpoly):
        # swap the circumcircles of the two polygons and then replicate points
        # at the same angles and then draw it.

        # Making sure that the point angles are properly calculated and preserved
        self.gen_point_angles()
        otherpoly.gen_point_angles()

        # Swap the circumcircles
        self.circumcircle, otherpoly.circumcircle = otherpoly.circumcircle, self.circumcircle

        # Once the circumcircles are swapped, re-make the points.
        self.gen_points()
        otherpoly.gen_points()

    def __repr__(self):
        return "Polygon: %s sides, circumcircle: %s" % (self.N, self.circumcircle)

if __name__ == '__main__':
    plt.figure()
    A = Polygon(no_of_sides=4, isRegular=False, size=10, hatch='random')
    A.makeRandomCircumcircle()
    A.makeShape()
    A.rotate(math.pi / 2)

    B = Polygon(no_of_sides=4, isRegular=True, size=5, hatch='*')
    B.makeRandomCircumcircle()
    B.makeShape()
    A.gen_inside(B)
    B.drawPolygon()
    A.drawPolygon()
    A.rotate()
    B.rotate()
    B.drawPolygon()
    A.drawPolygon()

    plt.axis('off')
    plt.axis('image')
    plt.savefig('./test1.png')
    plt.close()
