from pyhive import  presto
import requests
import numpy as np

cursor = presto.connect ( 'localhost' ).cursor ( )
cursor.execute ( 'SELECT count(*) from tpch.customer' )
print ( cursor.fetchone ( ) );
