import sys
import csv
import math
from region import Region
from plot import Plot
import matplotlib.pyplot as plt


def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi


def main(results, boundaries, base, width, style, coords):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions
    Args:
        results (str): name of a csv file of election results
        boundaries (str): name of a csv file of geographic information
        output (str): name of a file to save the image
        width (int): width of the image
        style (str): 'SOLID'
    """
    def to_point(longlat_list):
        '''
        Adjusts points so that they can be mapped. The with-opens below make the actual map.
        '''
        return list(zip([float(x) for x in longlat_list[2::2]],[mercator(float(x)) for x in longlat_list[3::2]]))
    with open(results,'r') as fin:
        results_lst1=list(csv.reader(fin))
    with open(boundaries,'r') as fin1:
        boundaries_lst1= list(csv.reader(fin1))

        lstofboundaries = [to_point(x) for x in boundaries_lst1] #skip state,city first pair

        lstofregions= [Region(x,int(y[2]),int(y[3]),int(y[4])) for x,y in zip(lstofboundaries,results_lst1)]
        minlong = min([(x.min_long()) for x in lstofregions])
        maxlong = max([(x.max_long()) for x in lstofregions])
        minlat = min([(x.min_lat()) for x in lstofregions])
        maxlat = max([(x.max_lat()) for x in lstofregions])

        Make_Map = Plot(width, minlong, minlat, maxlong, maxlat)
        output="map{}.png".format(base)
        for x in lstofregions:
            Make_Map.draw(x,style)
        Make_Map.save(output)
        tweet_coords=Make_Map.pointgen(coords)
        imgs=[]
        for index, tweet in enumerate(tweet_coords):
            if index % 1 == 0:
                Make_Map.drawtweet(tweet)
                Make_Map.save("map{}{:04d}.png".format(base,index))
                imgs.append("map{}{}.png".format(base,index))

        #OBSERVE: In line 51 of map_generator.py, there is an "if" parameter that will allow you to determine the numbers of tweets you want mapped. If it is set to 1, you will get every single picture. This could easily reach the hundreds. Adjust accordingly.


if __name__ == '__main__':
    results = sys.argv[1]
    boundaries = sys.argv[2]
    base = sys.argv[3]
    width = int(sys.argv[4])
    style = sys.argv[5]
    coords = sys.argv[6]
    main(results, boundaries, base, width, style, coords)
