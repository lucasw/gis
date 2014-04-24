# basic code from https://gist.github.com/anonymous/4385412#file-makedots-py


import sys
import ogr
import pygame

def make_ogr_point(x,y):
    return ogr.Geometry(wkt="POINT(%f %f)"%(x,y))

def get_bbox(geom):
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
        
    return (x1, y1, x2, y2)

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
    
    pop_min = float("inf")
    pop_max = float("-inf")
    pop_tot = 0

    census = []
    
    for j, feat in enumerate( lyr ):

        pop = feat.GetField(pop_field)
        geom = feat.GetGeometryRef()
        if geom is None:
            continue
        
        bb = get_bbox(geom)

        x1 = min(x1, bb[0])
        y1 = min(y1, bb[1])
        x2 = max(x2, bb[2])
        y2 = max(y2, bb[3])

        census.append((bb, geom, pop))

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
    
    print len(census)
    print census[0]
    print census[0][0]
    #for block in census:
    #    print census[2]

if __name__=='__main__':
    if len(sys.argv) < 3:
        print("not enough arguments  'input shp file' 'output file'")
        sys.exit( 1 ) 
    print "test ", sys.argv[1], sys.argv[2]
    process(sys.argv[1], sys.argv[2]) 
    #for state in ['44','45','46','47','48','49','50','51','53','54','55','56']:
    #    print "state:%s"%state
    #    main( "../tabblock2010_"+state+"_pophu/tabblock2010_"+state+"_pophu.shp", "people.db" )
