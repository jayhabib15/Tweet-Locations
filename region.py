class Region:
    """
    A region (represented by a list of long/lat coordinates).
    """

    def __init__(self, coords, r_votes, d_votes, o_votes):
        self.coords = coords

    def lats(self):
        "Return a list of the latitudes of all the coordinates in the region"
        return [y for x,y in self.coords]

    def longs(self):
        "Return a list of the longitudes of all the coordinates in the region"
        return [x for x,y in self.coords]

    def min_lat(self):
        "Return the minimum latitude of the region"
        return min(self.lats())

    def min_long(self):
        "Return the minimum longitude of the region"
        return min(self.longs())

    def max_lat(self):
        "Return the maximum latitude of the region"
        return max(self.lats())

    def max_long(self):
        "Return the maximum longitude of the region"
        return max(self.longs())
