#!user/bin/env python
# -*- coding: utf-8 -*-

import argparse
import urllib2
import csv
import re
import decimal


def main():
    """Docstring"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    args = parser.parse_args()
    csvData = downloadData(args.url) # delete later
    memoryData = yieldData(csvData)
    searchData(memoryData)


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
    """Stores download csv data as generator object"""
    cr = csv.reader(csvData)

    for line in cr:
        yield line

def searchData(memoryData):
    """ processes data for images and browser"""
    count = 0
    count_all = 0
    pattern = '(?i)(png|jpg|gif)$'

    firefox_count = 0
    chrome_count = 0
    safari_count = 0
    explorer_count = 0

    for row in memoryData:
        image = row[0]
        count_all += 1
        if re.search(pattern, image) is not None:
            count += 1

        image2 = row[2]
        if re.search('(?i)(firefox)', image2):
            firefox_count += 1
        elif re.search('(?i)(chrome)', image2):
            chrome_count += 1
        elif re.search('(?i)(safari)', image2):
            safari_count += 1
        elif re.search('(?i)(trident)', image2): # trident seems to represent IE????
            explorer_count += 1


    percent = decimal.Decimal((
                                  decimal.Decimal(count)
                                  / decimal.Decimal(count_all)
                              ) * decimal.Decimal('10'))
    message = '{} hits were for images. Out of a total of ' \
              '{}, this means images account for' \
              ' {}% of all' \
              ' hits.'.format(count, count_all, percent)

    get_most_hits = {'Firefox': firefox_count, 'Safari': safari_count, 'Chrome': chrome_count,
                     'Internet Explorer': explorer_count}
    max_key = max(get_most_hits, key=get_most_hits.get)
    max_value = max(get_most_hits.values())
    browser_message = 'The browser with the most amount of hits is {}, with ' \
                      '{} hits on the given day'.format(max_key, max_value)
    print message
    print browser_message


if __name__ == '__main__':
    main()