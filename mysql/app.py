#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse
from math import radians, cos
import MySQLdb
# http://www.mysqlperformanceblog.com/2013/10/21/using-the-new-spatial-functions-in-mysql-5-6-for-geo-enabled-applications/

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--latitude', required=True, type=float,
                        help='specify current latitude')
    parser.add_argument('-o', '--longitude', required=True, type=float,
                        help='specify current longitude')
    args = parser.parse_args()

    dist = 1
    current_latitude = args.latitude
    current_longitude = args.longitude
    rlon1 = current_longitude - dist / abs(cos(radians(current_latitude))*69)
    rlon2 = current_longitude + dist / abs(cos(radians(current_latitude))*69)
    rlat1 = current_latitude - (dist / 69)
    rlat2 = current_latitude + (dist / 69)

    con = MySQLdb.connect(
        db='geoloc', user='geoloc', passwd='geoloc',
        charset='utf8', host='192.168.33.59')

    cursor = con.cursor()
    sql = '''
    SELECT
        astext(geo)
        ,name
    FROM geo
    WHERE ST_WITHIN(geo, ENVELOPE(LINESTRING(POINT(%s, %s), POINT(%s, %s))))
    ORDER BY ST_DISTANCE(POINT(%s, %s), geo) LIMIT  10;
    '''
    cursor.execute(sql, [rlon1, rlat1, rlon2, rlat2, current_longitude, current_latitude])
    result = cursor.fetchall()
    for row in result:
        print row[0], row[1].encode('utf-8')
