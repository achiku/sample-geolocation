#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse
from math import radians, cos
import MySQLdb
# http://gihyo.jp/dev/feature/01/location-based-services/0005


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--latitude', required=True, type=float,
                        help='specify current latitude')
    parser.add_argument('-o', '--longitude', required=True, type=float,
                        help='specify current longitude')
    parser.add_argument('-r', '--radius', required=True, type=float,
                        help='specify radius')
    args = parser.parse_args()

    dist = args.radius  # distance must be float measured in mile
    current_latitude = args.latitude
    current_longitude = args.longitude
    rlon1 = current_longitude - dist / abs(cos(radians(current_latitude))*69)
    rlon2 = current_longitude + dist / abs(cos(radians(current_latitude))*69)
    rlat1 = current_latitude - (dist / 69)
    rlat2 = current_latitude + (dist / 69)

    print 'radius: {}'.format(dist)
    print 'rlat1: {}'.format(rlat1)
    print 'rlon1: {}'.format(rlon1)
    print 'rlat2: {}'.format(rlat2)
    print 'rlon2: {}'.format(rlon2)

    con = MySQLdb.connect(
        db='geoloc', user='geoloc', passwd='geoloc',
        charset='utf8', host='192.168.33.58')

    cursor = con.cursor()
    sql = '''
    SELECT
        id
        ,astext(geo)
        ,name
    FROM place
    WHERE MBRContains(LINESTRING(POINT(%s, %s), POINT(%s, %s)), geo);
    '''
    cursor.execute(
        sql, [rlon1, rlat1, rlon2, rlat2])
    result = cursor.fetchall()
    for row in result:
        print row[0], row[1], row[2].encode('utf-8')
