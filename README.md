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
