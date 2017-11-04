from PIL import Image, ImageDraw
from PIL.ImageColor import getrgb
import math

def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def generatecoords(coords):
    '''
    Generates a list of appropriate, scaled coorindates for mapping.
    '''
    coordinates=[]
    with open(coords,'r') as fin:
        for line in fin:
            s=(line[1:-2])
            string_of_coords=s.split(',')
            coordtuple=(float(string_of_coords[0]),mercator(float(string_of_coords[1])))
            coordinates.append(coordtuple)
        return coordinates

class Plot:

    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """
    @staticmethod
    def interpolate(x_1, x_2, x_3, newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into newlength
        x_2 and x_3 define a line segment, and x2 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        return (newlength*(x_1-x_2))/(x_3-x_2)

    @staticmethod
    def proportional_height(new_width, width, height):
        """
        return a height for new_width that is
        proportional to height with respect to width
        Yields:
            int: a new height
        """
        return int((new_width*height)/width)

    @staticmethod
    def fill(region, style):
        """return the fill color for region according to the given 'style'"""
        if style == "SOLID":
            return Plot.solid(region)

    @staticmethod
    def solid(region):
        """
        a solid color passed to the program
        Args:
            region (Region): a region object
        Yields:
            (int, int, int): a triple (RGB values between 0 and 255)
        """
        return (255, 255, 204)

    def __init__(self, width, min_long, min_lat, max_long, max_lat):
        """
        Create a width x height image where height is proportional to width
        with respect to the long/lat coordinates.
        """

        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat
        self.width = width
        self.height = Plot.proportional_height(self.width, self.max_long - self.min_long, self.max_lat - self.min_lat)
        self.image = Image.new("RGBA", (self.width, self.height), (255, 255, 255))

    def pointgen(self, coords):
        final_longs = []
        final_lats = []
        coordinates2=generatecoords(coords)
        for x,y in coordinates2:
            final_longs.append(Plot.interpolate(x, self.min_long, self.max_long, self.width))
        for x,y in coordinates2:
            final_lats.append(self.height-Plot.interpolate(y, self.min_lat, self.max_lat, self.height))
        final_coords = list(zip(final_longs, final_lats))
        return final_coords

    def save(self, filename):
        """save the current image to 'filename'"""
        self.image.save(filename, "PNG")

    def draw(self, region, style):
        """
        Draws 'region' in the given 'style' at the correct position on the
        current image
        Args:
            region (Region): a Region object with a set of coordinates
            style (str): 'SOLID' to determine the polygon's fill
        """

        def trans_long():
            '''
            Translates longitudes for mapping.
            '''
            return [Plot.interpolate(x, self.min_long, self.max_long, self.width) for x in region.longs()]

        def trans_lat():
            '''
            Translates latitudes for mapping.
            '''
            return [self.height - Plot.interpolate(x, self.min_lat, self.max_lat, self.height) for x in region.lats()]

        ImageDraw.Draw(self.image).polygon([(x,y) for (x,y) in zip(trans_long(), trans_lat())], Plot.fill(region, style), outline=(0,0,0))

    def drawtweet(self, point):
        '''
        Plots a square on the map showing where the tweet came from.
        '''
        (x,y) = point
        ImageDraw.Draw(self.image).rectangle([x-10 ,y-10 ,x+10, y+10], fill = (0, 132, 180, 150), outline = (0, 0, 0))
