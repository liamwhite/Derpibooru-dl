#-------------------------------------------------------------------------------
# Name:        For sorting download lists
# Purpose:
#
# Author:      new
#
# Created:     24/03/2014
# Copyright:   (c) new 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import derpibooru_dl


def artists_at_top(query_list):
    """Put anything with the string "artist" at the top of the list"""
    put_at_top = []
    put_at_bottom = []
    for query in query_list:
        if "artist".lower() in query.lower():
            put_at_top.append(query)
        else:
            put_at_bottom.append(query)
    output_list = put_at_top + put_at_bottom
    return output_list


def main():
    input_list_path = "config\\to_sort.txt"
    output_list_path = "config\\artists_at_top.txt"
    input_list = derpibooru_dl.import_list(input_list_path)
    artists_at_top_list = artists_at_top(input_list)
    derpibooru_dl.append_list(artists_at_top_list, output_list_path)

if __name__ == '__main__':
    main()
