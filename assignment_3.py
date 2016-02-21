#!user/bin/env python
# -*- coding: utf-8 -*-
"""Downloads and processes data from a website and returns hit information"""

import argparse
import urllib2
import csv
import re
import decimal
import os


def main():
    """Calls all functions"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    args = parser.parse_args()
    if os.path.exists('hitdata.csv'):
        searchImage('hitdata.csv')
        searchBrower('hitdata.csv')
    else:
        csvData = downloadData(args.url)
        downloadData(csvData)


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
    html = response.read()
    localfile = open('hitdata.csv', 'wb')
    localfile.write(html)
    localfile.close()


def searchImage(csvfile):
    """ processes data for images and browser
    Args:
        csvfile: file saved locally
    Returns:
        str message with number of image hits and percent
    Example:
        >>>searchImage(csvfile)
        6574 hits were for images. Out of a total of 10000,
        this means images account for 6.5740% of all hits.
    """
    f = open(csvfile, 'rb')
    reader = csv.reader(f)

    count = 0
    count_all = 0
    pattern = '(?i)(png|jpg|gif)$'

    for row in reader:
        image = row[0]
        count_all += 1
        if re.search(pattern, image) is not None:
            count += 1

    percent = decimal.Decimal((
                                  decimal.Decimal(count)
                                  / decimal.Decimal(count_all)
                              ) * decimal.Decimal('10'))
    message = '-------------------------------------------------------------' \
              '\n{} hits were for images. Out of a total of ' \
              '{}, this means images account for' \
              ' {}% of all' \
              ' hits.'.format(count, count_all, percent)

    print message
    f.close()

def searchBrower(csvfile):
    """Processes browser data.
    Args:
        csvfile: csv file to processed
    Returns:
        str message of broweser most used
    Examples:
        >>>searchBrower(csvfile)
        The browser with the most amount of hits is Chrome,
         with 4373 hits on the given day
    """
    f = open(csvfile, 'rb')
    reader = csv.reader(f)

    firefox_count = 0
    chrome_count = 0
    safari_count = 0
    explorer_count = 0

    for row in reader:
        browser = row[2]
        if re.search('(?i)(firefox)', browser):
            firefox_count += 1
        elif re.search('(?i)(chrome)', browser):
            chrome_count += 1
        elif re.search('(?i)(safari)', browser):
            safari_count += 1
        elif re.search('(?i)(trident)', browser): # trident seems to represent IE????
            explorer_count += 1

    get_most_hits = {'Firefox': firefox_count, 'Safari': safari_count, 'Chrome': chrome_count,
                     'Internet Explorer': explorer_count}
    max_key = max(get_most_hits, key=get_most_hits.get)
    max_value = max(get_most_hits.values())
    browser_message = '\nThe browser with the most amount of hits is {}, with ' \
                      '{} hits on the given day\n----------------------------------' \
                      '----------------------------' \
                      ''.format(max_key, max_value)
    print browser_message
    f.close()


if __name__ == '__main__':
    main()