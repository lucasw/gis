# basic code from https://gist.github.com/anonymous/4385412#file-makedots-py

# Lucas Walter April 2014 

import sys
import ogr
import pygame
import time
import math

def make_ogr_point(x,y):
    return ogr.Geometry(wkt="POINT(%f %f)"%(x,y))

# http://stackoverflow.com/questions/21335091/python-area-of-irregular-polygon-results-in-negative-value
# assume last point and first are same, apparently common in survey/gis data
def get_area(pts):
    area = 0.0

    n = len(pts)
    # if matching endpoint isn't true, maybe should make -1 optional
    for i in range(n - 1):
        i1 = (i+1)%n
        area += pts[i][0]*pts[i1][1] - pts[i1][0]*pts[i][1]       
        area *= 0.5

    return abs(area);

# http://www.arachnoid.com/area_irregular_polygon/index.html
def find_area(array):
    a = 0
    ox,oy = array[0]
    for x,y in array[1:]:
        a += (x*oy-y*ox)
        ox,oy = x,y
    return a/2

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

def process(input_filename, output_filename):

    # open the shapefile
    ds = ogr.Open( input_filename )
    if ds is None:
        print "Open failed.\n"
        sys.exit( 1 )

    lyr = ds.GetLayerByIndex( 0 )

    lyr.ResetReading()

    feat_defn = lyr.GetLayerDefn()
    field_defns = [feat_defn.GetFieldDefn(i) for i in range(feat_defn.GetFieldCount())]

    # look up the index of the field we're interested in
    for i, defn in enumerate( field_defns ):
        if defn.GetName()=="POP10":
            pop_field = i

    n_features = len(lyr)

    x1 = float("inf")
    y1 = float("inf")
    x2 = float("-inf")
    y2 = float("-inf")
    
    density_min = float("inf")
    density_max = float("-inf")
    #density_avg = 
    area_tot = 0

    pop_min = float("inf")
    pop_max = float("-inf")
    pop_tot = 0

    census = []
    
    for j, feat in enumerate( lyr ):

        pop = feat.GetField(pop_field)
        geom = feat.GetGeometryRef()
        if geom is None:
            continue
        
        dat = get_pts(geom)
        if dat is None:
            continue
        pts, bb = dat
        #if len(pts) != 4:
        #    print j, " ", pop, " ", len(pts)

        x1 = min(x1, bb[0])
        y1 = min(y1, bb[1])
        x2 = max(x2, bb[2])
        y2 = max(y2, bb[3])

        # all the pts end with with the same starting point, need to remember this
        # when computing area
        if (j == 0):
            print "points ", pts
    
        # TBD need a lat/long to meters conversion
        area = find_area(pts)
        
        if (area <= 0):
            print j, " bad area ", pts
            continue
        
        area_tot += area

        census.append((bb, pts, pop, area))
        
        density = pop/area
        
        if (area < 2e-8):
            print "small area", j, pop, area, pts
        
        if (pop > 0):
            density_min = min(density_min, density)
        density_max = max(density_max, density)
        
        pop_min = min(pop_min, pop)
        pop_max = max(pop_max, pop)
        pop_tot += pop

        #if j%1000==0:
        #    #conn.commit()
        #    print "%s/%s (%0.2f%%)"%(j+1,n_features,100*((j+1)/float(n_features)))
        #    print "population ", pop
        #    print bb
   
    print j
    print "bounding box ", x1, y1, x2, y2
    print "pop ", pop_tot, ", bounds ", pop_min, pop_max
    print "density ", density_min, density_max, ", area", area 
    dy = y2 - y1
    dx = x2 - x1
    pygame.init()
    ratio = dy / dx
    print "ratio ", ratio
    width = 2048
    height = ratio * width
    size = (int(width), int(height))
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255, 255))
    surf = pygame.Surface(size, flags=pygame.SRCALPHA)
    pix_per_deg = width / dx 
    print "pix per deg ", pix_per_deg

    print len(census)
    print census[0]
    print census[0][0]
    for block in census:
        pop = block[2]
        area = block[3]
        density = pop/area
        # TODO need to take into account area for proper coloring
        color_val = 0
        log_scale = 0.0001
        if (density > 0):
            color_val = (255.0) * math.log(density * log_scale) / \
                 math.log(density_max * log_scale)
        col = (255 - color_val * 0.5 , color_val, 128 - color_val * 0.5, 120)
        if pop == 0:
            col = (0,0,0, 40)
        # draw bounding rect
        if False:
            bb_deg = block[0]
            x1b = bb_deg[0] - x1 
            y1b = bb_deg[1] - y1
            x2b = bb_deg[2] - bb_deg[0]
            y2b = bb_deg[3] - bb_deg[1]
            rect = pygame.Rect( 
                int(x1b * pix_per_deg), height - int( (y1b + y2b) * pix_per_deg), 
                int(x2b * pix_per_deg), int(y2b * pix_per_deg) )
            pygame.draw.rect(surf, col, rect, 0)

        deg_pts = block[1]
        pts = []
        for (xd,yd) in deg_pts:
            xp = (xd - x1) * pix_per_deg 
            yp = height - (yd - y1) * pix_per_deg
            pts.append((xp, yp)) 

        pygame.draw.polygon(surf, col, pts, 0)
        #pygame.draw.polygon(surf, (0, 0, 0, 100), pts, 1)
    
    screen.blit(surf, (0,0))
    pygame.image.save(screen, sys.argv[2])
    time.sleep(1.0)

if __name__=='__main__':
    if len(sys.argv) < 3:
        print("not enough arguments  'input shp file' 'output file'")
        sys.exit( 1 ) 
    print "test ", sys.argv[1], sys.argv[2]
    process(sys.argv[1], sys.argv[2]) 
    #for state in ['44','45','46','47','48','49','50','51','53','54','55','56']:
    #    print "state:%s"%state
    #    main( "../tabblock2010_"+state+"_pophu/tabblock2010_"+state+"_pophu.shp", "people.db" )
