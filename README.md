gis
===

GIS stuff, play with openstreetmap, U.S. census, data.seattle.gov data.

Posts
=====

https://plus.google.com/103190342755104432973/posts/5UnDuAHcDLV
https://plus.google.com/103190342755104432973/posts/QCHe9er2KnP
https://plus.google.com/103190342755104432973/posts/JCoXRYva3zR
https://plus.google.com/103190342755104432973/posts/QHkUDUrEQyQ
https://plus.google.com/103190342755104432973/posts/jUdxLiqqb3P

Traffic Volumes:
https://plus.google.com/103190342755104432973/posts/GFAts9rkDys

https://plus.google.com/103190342755104432973/posts/7nPrnygsHif
https://plus.google.com/103190342755104432973/posts/g1grYpy74e9
https://plus.google.com/103190342755104432973/posts/A9eHVJ82fj1
https://plus.google.com/103190342755104432973/posts/7uNXwKJYkCn
https://plus.google.com/103190342755104432973/posts/2LyKmWJxavh
https://plus.google.com/103190342755104432973/posts/ZCv8tkg7aTC


Todo
====

Take traffic volumes and output a json file with all the data in it, then make a gmap viewer in javascript.

Could have complete history of each street in the json.

The current traffic_volume.ipynb creates an image using street network points from the street network shapefile.  
In order to get this into json, could output a json with features that have volume data, but the streets are all lines- will these be clickable in a browser?
If not then need to create inflated shapes from them, should be easy geometric function for that, then write those into the json.

How were the json files made for http://lucasw.github.io/gmap/census.html?
Those were a straight conversion from shp, no extra data was put into them.

Have a small json test file (Also no extra data), see if a gmap viewer can be made for it.

Tools
=====

easy_install Rtree

Source Census Data
==================

http://bmander.com/dotmap/methods.html

```
    for i in `seq -w 1 56`; do wget ftp://ftp2.census.gov/geo/tiger/TIGER2010BLKPOPHU/tabblock2010_${i}_pophu.zip; done
```

TBD - host all the same data in a google drive and link to it here

The FIPS code link on the dotmap page is dead, so look to wikipedia:

http://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(S%E2%80%93U)#US:_United_States

US53 is Washington State.


https://gist.github.com/anonymous/4385412

```
    sudo apt-get install python-gdal 
```
    
~~python-shapely~~


2013 or 2014 Census updates?
----------------------------

https://www.census.gov/geo/maps-data/data/tiger-line.html

Housing Data
------------

Per-tract info on housing units in multi-unit structures vs. single-family-housing?

http://quickfacts.census.gov/qfd/meta/long_HSG096212.htm

Economic
--------

American Community Survey?

http://www2.census.gov/acs2012_5yr/summaryfile/2008-2012_ACSSF_By_State_All_Tables/

http://www2.census.gov/acs2012_5yr/summaryfile/2008-2012_ACSSF_By_State_All_Tables/Washington_All_Geographies_Tracts_Block_Groups_Only.zip

What is difference with 'not tract' version?

Lots of warnings on opendata stack about complexity, statistical inaccuracy.

Tables are unlabeled.

http://www2.census.gov/acs2012_5yr/summaryfile/UserTools/ACS_2008-2012_SF_Tech_Doc.pdf

The e prefix is for estimate, the m is for margin of error.

Here is an example file

e20125wa0059000.txt 

This is sequence number 0059

Inside the file is a set of long lines, here is one:

```
ACSSF 201200000 wa  0 59  1 2619995 130819  23551 10544 11151 10766 10056 10422 7834  7573  5916  9527  10258 8051  3180  807 791 392 926139  44349 27841 30469 36923 37541 43490 42770 44774 40626 79924 111635  145771  95680 54006 49756 40584 1037531 58273 33877 31343 34334 35003 39795 36911 41291 37694 81315 110721  152267  117833  77681 78888 70305 525506  32948 39653 40541 39784 37736 34185 31293 28963 26569 45041 50586 50395 26015 14993 13660 13144 2186137 98755 15786 8437  8436  8199  7819  7990  5758  5663  4680  7431  8401  6290  2277  748 555 285 719456  31345 18965 20775 26448 27463 32016 32196 33830 31212 63742 90225 117884  77718 43950 39472 32215 887415  45577 27607 25014 27991 28786 33069 30470 34615 31502 68823 95753 132910  103038  68330 70544 63386 480511  26179 34797 36652 36643 35156 31949 29151 26821 24865 41857 47249 46715 23701 13920 12575 12281 88888 5320  1321  244 519 462 514 553 343 331 205 253 171 321 61  0 2 20  38623 3831  2490  2331  2952  2792  2727  2026  2593  1809  3004  3445  4307  2024  927 911 454 34907 3985  2293  1628  1669  1332  1871  1602  1819  1567  2703  3256  4511  2969  1713  1270  719 10038 1368  1126  1003  611 559 505 521 480 302 747 802 713 600 185 276 240
```

The columns range from 'A' to 'HE', which is  'H'*26 + 'E' = 7*26 + 4 = 186
False leads (insufficient resolution):

1yr vs. 3 vs 5yr?
http://www2.census.gov/acs2012_1yr/pums/

files http://www2.census.gov/acs2012_1yr/pums/csv_hwa.zip and http://www2.census.gov/acs2012_1yr/pums/unix_pwa.zip are for Washington State.

Data is in sas7bdat format, what is that?

https://pypi.python.org/pypi/sas7bdat

Don't bother with install, just export PYTHONPATH=$PYTHONPATH:. and then run the convert to csv script from the same dir:

```
:~/other/sas7bdat-0.2.2$ ./scripts/sas7bdat_to_csv ~/own/gis/acs/psam_h53.sas7bdat 
[psam_h53.csv] wrote 32149 of 32149 lines
```

The data has a few samples of income per PUMA Public Use Microdata Area "PUMAs are special non-overlapping areas that partition each state into contiguous geographic units containing no fewer than 100,000 people each"

Need to get PUMA shapefiles.  

But what about tract level data?

BG is for block group:
ftp://ftp2.census.gov/geo/tiger/TIGER_DP/2011ACS/2011_ACS_5YR_BG_53.gdb.zip

Seattle Data
============

City Council Districts
----------------------

These list census tracts:
http://clerk.seattle.gov/~public/charter/charter.htm#articleIV

http://www.seattledistrictsnow.org/files/view-only_petition.pdf

The census shape file has TRACTCE10, which is the same as the tract numbers in the charter with two decimal places- 97.02 is 009702. 

The charter also mentions block groups, which appear the same as BLOCKCE.  Perhaps some of the tracts span the border with neighboring cities, so the blocks are called out.  

It should be easy to make list of all the tracts and block numbers where provided in an ipython notebook, then plot them and have a data structure that organizes all the census data by council district.

How to do joins that will meld all the tracts together- buffer + cascaded_union in Shapely?

### Verification 

Get a shapefile of the Seattle boundary and make sure the edges of the districts are within it.
https://data.seattle.gov/dataset/Seattle-City-Limits/veex-tfda

#### Missing & Erroneous tracts

So far it looks like the amendment missed tracts in District 2: 110.02 and 111.01

Also 260.01 block 1008 is outside the Seattle boundary.

Block Group 1 of Tract 17 should be 17.01

### Export to shapefile, kml?

Use fiona, though no ubuntu package:
https://pypi.python.org/pypi/Fiona

So install python-pip and then pip-install fiona
also need descartes

Buildings
---------

2009 building outlines:

https://data.seattle.gov/dataset/2009-Building-Outlines/y7u8-vad7

Use qgis to inspect data

Ideally all the buildings would be associated with their census blocks- a data structure would have 2-way links, a census block would have a list of all buildings included, and a the buildings would link to their census block.  A rough estimate of occupants per building could be made for visualization purposes.

Parks 
-----

A good first pass would be to subtract parks out of census blocks that include them, and get the population density correct for the remaining area rather than diluting it with park land.

https://data.seattle.gov/dataset/City-Of-Seattle-Parks/kxj9-se6t

Zoning
------

Zoning- can see a map on this page, but no shp boundaries?

https://data.seattle.gov/Land-Base/DPD-ZONING/r6xd-5qab

Use this for zoning instead:
https://data.seattle.gov/dataset/City-Of-Seattle-Zoning/2hat-teay

Look at zoning breakdown of each district, total area of each zoning type in all of Seattle.

Street Network
--------------

Network of streets, no widths just 'artclass' (arterial class).

Pavement
--------

Pretty old (1999), but better than nothing.  Want to be able to figure out street widths.

https://data.seattle.gov/dataset/Pavement-Edge/zbph-53dz

Parking
-------

Haven't found this dataset yet- street parking, zone permit areas.

https://data.seattle.gov/Transportation/No-parking-data/aua5-7y43

Traffic Volume
--------------

Spreadsheet sent to me by SDOT, get an updated one regularly, try to get them to post it to data.seattle.gov?

Spreadsheet references 

Traffic Signals
---------------

https://data.seattle.gov/Transportation/Traffic-Signals/dr6d-ejex

Traffic Circles
---------------

https://data.seattle.gov/Transportation/Traffic-Circles/g6i5-ix4z

Usage
=====

ipython (1.2.1) 

```
ipython notebook --pylab inline
```

Edit parameter values, run all, should get png in current directory.  

old python only script:
    python census_shp.py ~/own/gis/census/*53_pophu.shp pop_density_wa.png output.png


Street Network
==============

How to implement a graph in python?

Each street item as an F_INTR_ID and a S_INTR_ID - the start and finish intersections

Combining network with pavement
-------------------------------

Need to create a graph of adjacent pavement sections, associate network segments inbetween them.

Want to get average width of each network segment, and approximate radius of each intersection.

King County
===========

data.kingcounty.gov

http://www5.kingcounty.gov/gisdataportal/Default.aspx

Parcels
-------

property_SHP.zip

ftp://ftp.kingcounty.gov/gis/Web/GISData/property_SHP.zip

Found via http://www5.kingcounty.gov/gisdataportal/Default.aspx

The best information is in this shapfile:

parcel_address.shp

The amount of data is very large, filter on POSTALCYTN = SEATTLE or CTYNAME = Seattle - no these don't include everything, try LEVY_JURIS=SEATTLE (more complete but still not all) or KCTP_CTYST=SEATTLE WA (also not complete).  What about zip codes?  Also not complete.  

A boolean combination may be best, in qgis Select By Expression: 
```
( "POSTALCTYN" = 'SEATTLE')  +  ("CTYNAME" = 'Seattle' ) +  "LEVY_JURIS"= 'SEATTLE' + "KCTP_CTYST"='SEATTLE'( "POSTALCTYN" = 'SEATTLE')  +  ("CTYNAME" = 'Seattle' ) +  "LEVY_JURIS"= 'SEATTLE' + "KCTP_CTYST"='SEATTLE' + ("JURIS" = 'SE') (this still isn't working in qgis)
```

Maybe just boundary clipping.

The 'PRESENTUSE' field looks very interesting.

Ought to make a geojson that has all that information plus census information and population density.  Some info in the parcels could be used to determine that chunks of census blocks are unoccupied (because the taxes are zero?  Is that a safe assumption), and that the real density is higher.  

Need to calculate area of all parcels within a census block (and are there any parcels that cross census block boundaries?), and then assume population is distributed among them.  
The densities will be higher since streets are excluded, which is fine.
It's okay for densities to include more unused areas at higher levels, because those areas ought to be factored in.

Even without integrating census data a simple colorized map of property size or property values would be useful.

Need to convert the units to lat long.

" Planar coordinates are encoded using coordinate pair
Abscissae (x-coordinates) are specified to the nearest 0.0005
Ordinates (y-coordinates) are specified to the nearest 0.0005
Planar coordinates are specified in Foot_US

The horizontal datum used is D North American 1983 HARN.
The ellipsoid used is GRS 1980.
The semi-major axis of the ellipsoid used is 6378137.0.
The flattening of the ellipsoid used is 1/298.257222101."

Convert to EPSG:4326 - WGS 84 (Seattle zoning map), or EPSG:4269 - NAD83 (Census) ?
```
From USER:100000 -  * Generated CRS (+proj=lcc +lat_1=47.5 +lat_2=48.73333333333333 +lat_0=47 +lon_0=-120.8333333333333 +x_0=500000.0000000001 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs)
```

What happens during conversion to geojson with no parameters, does it do the right thing with coordinates?  

```
  ogr2ogr -f "GeoJSON" kc_parcels.json ../parcel_address.shp parcel_address
```

No it doesn't, also it is huge.

Try out a smaller us-feet shape file, the King County parks dataset.
See how google maps or the github geojson viewer likes the us-feet coordinates.
First attempt at github viewer was too large of a file (tens of megabytes) error, google maps didn't show anything and no console errors.  

Try reprojection.

  ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 park_property.json ../park_property.shp park_property

See lat and longs in output file so looking good.  Confirmed in google maps version.  Next go forwared with with clipping down 

Seattle rough bounding lat/long
  47.735444 -122.4394
  47.478379 -122.217455

```
  ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 -clipdst -122.4394 47.478379 -122.217455 47.735444 park_property.json ../park_property.shp park_property
```

Now try it on big kc_property shapefile:
  
```
  ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 -clipdst -122.4394 47.478379 -122.217455 47.735444 seattle_parcels.json ../parcel_address.shp parcel_address
```

Still nearly 500 MB, loads very slow in qgis.  Would take a ton of work to make this interactive in google maps with level-of-detail paging algorithms.

Why is it so large compared to census data, the entire state there was only 200 MB.  Are there too many data fields?  Could screen out all features except for Shape_area or a few other.  Are the polygons too detailed?

```
  ogr2ogr -f "GeoJSON" -select Shape_area,TAX_IMPR,TAX_LNDVAL -t_srs EPSG:4326 -clipdst -122.4394 47.478379 -122.217455 47.735444 seattle_parcels2.json ../parcel_address.shp parcel_address
```

The above field selection only shrinks the 500 MB down to 200 MB, the problem is in overly precise parcels- will ogr simplify them, or python?  

Is there a way to view vertices in qgis?   
Yes, click on the pencil to enable editing, then red x's appear at vertices.

How about filtering based on area?  
Screen out parks and similar that are less useful.

```
ogr2ogr -where "Shape_area<30000"  -t_srs EPSG:4326 -select Shape_area,TAX_IMPR,TAX_LNDVAL -clipdst -122.4394 47.478379 -122.217455 47.735444 filter.shp ../parcel_address.shp parcel_address
```

Instead of processing the entire KC dataset for each of this, create a Seattle only with no filtering:

```
ogr2ogr -t_srs EPSG:4326 -clipdst -122.4394 47.478379 -122.217455 47.735444 seattle_parcel.shp ../parcel_address.shp parcel_address
```

Get some error output:

```
ERROR 1: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 1306471.7205725275 125966.72408644645 at 1306471.7205725275 125966.72408644645
^[[B^[[BERROR 1: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 1295687.0337478775 196514.39328233138 at 1295687.0337478775 196514.39328233138
ERROR 1: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 1295277.0759567122 202488.5485786706 at 1295277.0759567122 202488.5485786706
```

Simplify:

```
ogr2ogr -simplify 0.00001 simplified_seattle_parcel.shp ../seattle_parcel.shp seattle_parcel
```

That halved the shapefile size (the dbf is still the same and huge, only the other filtering of fields will get that down), try make the tolerance 10x bigger - no change?  Raise to 0.001 makes some polys really bad (mostly coastlines), but most polys are already simple so don't benefit, and size doesn't shrink much.

On closer look even 0.0001 is too much, small lots lose corners, lower to 0.00001.

TBD combine the following with the simplification:

TBD get rid of MINOR=HYDR

```
ogr2ogr -where "MINOR!='HYDR'" -select Shape_area,TAX_IMPR,TAX_LNDVAL select_seattle_parcel.shp ../simplified_seattle_parcel.shp simplified_seattle_parcel
```

Could go back to making a static ipython image.
Trying that now, took a few minutes to even load the simplified seattle only parcels.

Trying to draw the 200,000 Seattle parcels with python patches takes way too much time, once 8 gigs of ram are met it doesn't seem to ever end after hitting about 168,000 parcels.  
Need to tile the images, make sure the plots aren't autoscaling, set them directly.

Also can filter down Seattle to core area, want less than 100k parcels:

```
ogr2ogr -clipdst -122.43 47.53 -122.22 47.67 seattle_parcel_subset.shp ../select_seattle_parcel.shp select_seattle_parcel
```

Off-screen rendering
--------------------

```
/usr/lib/pymodules/python2.7/matplotlib/__init__.py:1173: UserWarning:  This call to matplotlib.use() has no effect
because the backend has already been chosen;
matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
or matplotlib.backends is imported for the first time.

  warnings.warn(_use_error_msg)
```

Start ipython notebook without pylab:

```
  ipython notebook
```

Prop 1 vs. parcel size would be interesting.


King County Voting Districts/Precincts
======================================

https://data.kingcounty.gov/Places-Boundaries/Voting-Districts-of-King-County/4eex-7357

These have shape_areas, presumably these are square meters?

Problems with ipython crashing when trying to get points- Ipython dies with no error, but trying to duplicate in regular python leads to::

```
  >>> geom= feat.GetGeometryRef()
  >>> geom
  <osgeo.ogr.Geometry; proxy of <Swig Object of type 'OGRGeometryShadow *' at 0x7fc5103c2e10> >
  >>> pts = geom.GetPoints()
  ERROR 6: Incompatible geometry for operation
```

So far I've discovered some geoms like in the street network can directly provide points with GetPoints(), while others in the census and voting district shape files require::
 
```
  >>> ch = geom.ConvexHull()
  >>> bd = ch.GetBoundary()
  >>> pts = bd.GetPoints()
  >>> pts
  [(1347198.0200866014, 257822.7410414368), (1347169.633004278, 257894.8399786055), (1347151.2829753608, 257941.446840778),...
```

Unfortunately this is just the points of the convex hull, which worked okay for rectangular census blocks but not complex voting districts.  So skip the convex hull part, and do bd = geom.GetBoundary- this works.

What are units of precinct boundaries?  They aren't lat/long- it's feet with reference to 'harn 1983' etc.

Precinct Graph
--------------

Find shared edges between precincts and make a graph connecting them all.  Find permutations of precincts that would result in >50% approval, but don't break the graph.  Designate one downtown precinct to be the center and make sure remaining precincts connect to it.
