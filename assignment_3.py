#!user/bin/env python
# -*- coding: utf-8 -*-

import argparse
import urllib2
import csv
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    args = parser.parse_args()
    print args
    csvData = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv') # delete later
    memoryData = yieldData(csvData)
    searchImages(memoryData)


def downloadData(url):
    """fetches info from a url.
    Args:
        url (srt): url address of website
    Returns:
        fetches website info
    Example:
        downloadData(www.facebook.com)
        :rtype: object
    """
    response = urllib2.urlopen(url)

    return response

def yieldData(csvData):
    cr = csv.reader(csvData)

    for line in cr:
        yield line

def searchImages(memoryData):
    count = 0
    pattern = '(?i)(png|jpg|gif)$'
    for row in memoryData:
        image = row[0]
        if re.search(pattern, image) is not None:
            count += 1
            print image
    print count







if __name__ == '__main__':
    main()

