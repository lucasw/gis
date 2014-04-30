# some basic code from https://gist.github.com/anonymous/4385412#file-makedots-py

def make_ogr_point(x,y):
    return ogr.Geometry(wkt="POINT(%f %f)"%(x,y))

def get_pts(geom):
    x1=float("inf")
    y1=float("inf")
    x2=float("-inf")
    y2=float("-inf")

    ch = geom.ConvexHull()
    if not ch:
        return None
    bd = ch.GetBoundary()
    if not bd:
        return None
    pts = bd.GetPoints()
    if not pts:
        return None

    for x,y in pts:
        x1 = min(x1,x)
        y1 = min(y1,y)
        x2 = max(x2,x)
        y2 = max(y2,y)
        
    return (pts, (x1, y1, x2, y2))

# http://www.arachnoid.com/area_irregular_polygon/index.html
def find_area(array):
    a = 0
    ox,oy = array[0]
    for x,y in array[1:]:
        a += (x*oy-y*ox)
        ox,oy = x,y
    return a/2

