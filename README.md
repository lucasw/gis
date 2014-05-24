gis
===

GIS stuff, play with openstreetmap, U.S. census, data.seattle.gov data.

Source Census Data
==================

http://bmander.com/dotmap/methods.html

    for i in `seq -w 1 56`; do wget ftp://ftp2.census.gov/geo/tiger/TIGER2010BLKPOPHU/tabblock2010_${i}_pophu.zip; done

TBD - host all the same data in a google drive and link to it here

The FIPS code link on the dotmap page is dead, so look to wikipedia:

http://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(S%E2%80%93U)#US:_United_States

US53 is Washington State.


https://gist.github.com/anonymous/4385412

    sudo apt-get install python-gdal 
    
~~python-shapely~~



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

ipython notebook --pylab inline

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


King County Voting Districts/Precincts
======================================

https://data.kingcounty.gov/Places-Boundaries/Voting-Districts-of-King-County/4eex-7357

These have shape_areas, presumably these are square meters?

Problems with ipython crashing when trying to get points- Ipython dies with no error, but trying to duplicate in regular python leads to::

  >>> geom= feat.GetGeometryRef()
  >>> geom
  <osgeo.ogr.Geometry; proxy of <Swig Object of type 'OGRGeometryShadow *' at 0x7fc5103c2e10> >
  >>> pts = geom.GetPoints()
  ERROR 6: Incompatible geometry for operation

So far I've discovered some geoms like in the street network can directly provide points with GetPoints(), while others in the census and voting district shape files require::
 
  >>> ch = geom.ConvexHull()
  >>> bd = ch.GetBoundary()
  >>> pts = bd.GetPoints()
  >>> pts
  [(1347198.0200866014, 257822.7410414368), (1347169.633004278, 257894.8399786055), (1347151.2829753608, 257941.446840778),...

Unfortunately this is just the points of the convex hull, which worked okay for rectangular census blocks but not complex voting districts.  So skip the convex hull part, and do bd = geom.GetBoundary- this works.

What are units of precinct boundaries?  They aren't lat/long- it's feet with reference to 'harn 1983' etc.

Precinct Graph
--------------

Find shared edges between precincts and make a graph connecting them all.  Find permutations of precincts that would result in >50% approval, but don't break the graph.  Designate one downtown precinct to be the center and make sure remaining precincts connect to it.
