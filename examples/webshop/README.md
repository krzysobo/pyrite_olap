Webshop (Online shop example)
=============================

# About and news
- Example taken from ([pyrite-examples](https://github.com/krzysobo/pyrite-examples)), formerly ([cubes-examples](https://github.com/DataBrewery/cubes-examples))  
- improvements in:
    - model.json - upgrading of aggregates, fixing some errors in database model incl. references to nonexisting tables "newsletter" and "browser"    
    - upgrading to the newer Python stack (giving up 2.x completely)
    - database creation/cleanup etc
- extended with __webshop_fact_generator.py__, allowing to generate random facts for a specified cardinality and range of years. For example:
    ```python3 webshop_fact_generator.py 2 2022 2024```
    will generate a list of facts with cardinality 2 / 100 (0.02) for years 2022-2024.
    the generated csv can then be loaded into import_webshop.py:
    ```python3 import_webshop.py webshop-facts-daily-crd-2--{date-and-time-of-creation}.csv```

- The complete example "webshop" has been added back to cubes-anew-examples as well


# Example summary
Example includes:

* data sql
* SQLite database 
* model
* some sample screenshots using cubesviewer

Description
-----------

This sample includes a simple model and sample data about a fictional
online shop.

It contains a fact table "sales" with information about product sales,
customer country, product and product category, and invoice amount.

It also contains a fact table "webvisits" with information about
fictional web visits (country of visitor, page views, browser...).

Slicer Use
----------

Execute:

    $ slicer serve slicer.ini

Documentation: http://packages.python.org/cubes/server.html

CubesViewer
-----------

You can use a client tool like CubesViewer to inspect these cubes:

Live example: http://jjmontesl.github.io/cubesviewer/

Documentation: https://github.com/jjmontesl/cubesviewer/


Pyrite OLAP and Pyrite OLAP Frontend
-----------
There is an Angular-based frontend (currently under construction) 
for the forked, revived and renewed Cubes project, renamed to Pyrite OLAP:
    https://github.com/krzysobo/pyrite_olap_frontend
    https://github.com/krzysobo/pyrite_olap

