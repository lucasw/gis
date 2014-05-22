# some basic code from https://gist.github.com/anonymous/4385412#file-makedots-py
import ogr

def make_ogr_point(x,y):
    return ogr.Geometry(wkt="POINT(%f %f)"%(x,y))

def get_pts2(geom):
    x1=float("inf")
    y1=float("inf")
    x2=float("-inf")
    y2=float("-inf")

    pts = geom.GetPoints()
    if not pts:
        return None

    #print len(pts)
    #print pts
    # z is probably supposed to be elevation, but is -1.7976931348623157e+308
    if False: # for x,y,z in pts:
        x1 = min(x1,x)
        y1 = min(y1,y)
        x2 = max(x2,x)
        y2 = max(y2,y)

    return pts #, (x1, y1, x2, y2))

# this gets the convex hull points
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

    return (pts)

# http://www.arachnoid.com/area_irregular_polygon/index.html
def find_area(array):
    a = 0
    ox,oy = array[0]
    for x,y in array[1:]:
        a += (x*oy-y*ox)
        ox,oy = x,y
    return a/2

#################################

# TBD replace this with a proper projection approach
# TBD don't use this, use ax = fig.add_subplot(111, aspect=fr)
def conv_ll(latlong, fr):
    longitude = latlong[0]
    latitude = latlong[1]
    if (fr == None):
        fr = math.cos(latitude * math.pi / 180.0)
        print "latitude scale fraction", fr
    x = longitude * fr
    y = latitude
    
    return (x, y, fr)

# for loading street network data
def update_intersection(graph, intr_id, snd_id, latlongz):
    if not graph.has_key(intr_id):
        graph[intr_id] = {'latlong':latlongz[0:2], 'snd_id':[]}
        
    # TBD check for duplication
    graph[intr_id]['snd_id'].append(snd_id)
    
    if (snd_id < 0):
        print len(graph), "negative snd_id", intr_id, latlongz[0:2]
    # TBD check if new latlong is same as old
    #graph{intr_id}{'latlong'} = latlong

# load street network data
def load_streets(input_filename, limits):
    print "lat long limits ", limits
    xlim1 = limits[0]
    ylim1 = limits[1]
    xlim2 = limits[2]
    ylim2 = limits[3]
    
    # open the shapefile
    ds = ogr.Open( input_filename )
    if ds is None:
        print "Open failed.\n", input_filename
        return None #sys.exit( 1 )

    lyr = ds.GetLayerByIndex( 0 )

    lyr.ResetReading()

    feat_defn = lyr.GetLayerDefn()
    field_defns = [feat_defn.GetFieldDefn(i) for i in range(feat_defn.GetFieldCount())]

    # look up the index of the field we're interested in
    
    f_inter_ind = -1
    t_inter_ind = -1
    compkey_ind = -1
    snd_id_ind  = -1
    
    for i, defn in enumerate( field_defns ):
        if defn.GetName()=="F_INTR_ID":
            f_inter_ind = i
        if defn.GetName()=="T_INTR_ID":
            t_inter_ind = i
        if defn.GetName()=="SND_ID":
            snd_id_ind = i
        if defn.GetName()=="COMPKEY":
            compkey_ind = i
    
    print 'field inds', f_inter_ind, t_inter_ind, snd_id_ind, compkey_ind 
    
    n_features = len(lyr)
    print "num features", n_features    
    
    graph = {}
    # streets keyed by snd_id
    streets = {}
    # streets keyed by compkey
    streets_compkey = {}
        
    for j, feat in enumerate( lyr ):
        geom = feat.GetGeometryRef()
        if geom is None:
            print  j, " no geom"
            continue
 
        pts = geom.GetPoints()
        # TBD make sure these are in right order,
        # that the first point corresponds to inter_1
        latlong1 = pts[0]
        latlong2 = pts[-1]
        
        #exclude region outside of limits
        if (latlong1[0] > xlim2) or (latlong1[0] < xlim1) or \
            (latlong1[1] > ylim2) or (latlong1[1] < ylim1):
            continue
            
        inter_1 = feat.GetField(f_inter_ind)
        inter_2 = feat.GetField(t_inter_ind)
        snd_id  = feat.GetField(snd_id_ind)
        compkey = feat.GetField(compkey_ind) 
        
        if (not streets.has_key(snd_id)):   
            streets[snd_id] = (feat, inter_1, inter_2)
        else:
            # generate error
            #if (snd_id != 0): 
            print "dupe snd_id", snd_id, inter_1, inter_2
         
        if (compkey > 0):
            if (not streets_compkey.has_key(compkey)):
                streets_compkey[compkey] = (feat, inter_1, inter_2)
            #else:
               #print "dupe compkey", snd_id, compkey, inter_1, inter_2
               
        update_intersection(graph, inter_1, snd_id, latlong1)
        update_intersection(graph, inter_2, snd_id, latlong2)
        
        if False: #j < 10:
            #print inter_1, inter_2, compkey 
            
            #last_key = graph.keys()[-1]
            #last_node = graph[last_key]
            
            print '---'
            print graph #len(graph), last_key, last_node
            print '---'
    
    print "nodes in graph", len(graph.keys())
    
    return graph, streets, streets_compkey, ds
