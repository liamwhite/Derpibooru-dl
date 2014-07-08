#-------------------------------------------------------------------------------
# Name:        copy_to_tag_folders
# Purpose:
#
# Author:      new
#
# Created:     08/07/2014
# Copyright:   (c) new 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python





import derpibooru_dl




def build_tag_db(settings,tag_db_dict={}):
    """Build a db of ids and tags.
    If given, add to existing DB dict, otherwise build one from scratch.
    Format is: tag_db = {processed:{ID1:Path1,ID2:Path2,...} tags:{tag1:{ID1:path1,ID2:Path2}, tag2:{....},...}"""
    # Scan target folder for .JSON files
    # For each JSON file, get ID from filename
    derpibooru_dl.find_id_from_filename(settings, file_path)
    # check if id is in processed dict
    # if ID is not yet processed, read tags from json
    #Once all paths are processed, return finished dict



def get_tag_db(settings):
    """Get a dictionary containing the tag info through whatever means needed.
    Format is: tag_db = {processed:{ID1:Path1,ID2:Path2,...} tags:{tag1:{ID1:path1,ID2:Path2}, tag2:{....},...}"""
    # tag_db = { tag1:{ID1:path1,ID2:Path2},tag2:{....},...}
    # Check for existing DB in pickle path
    if os.path.exists(settings.tag_db_file):
    # If cannot get valid data from pickle, create new empty dict for DB
    # If no update or replace, return saved DB
    # If replace mode, ignore that and rebuild the whole thing, saving and returning new data
    # If update mode, add new ids to existing tag DB
    #


def copy_tag_list(settings):

    # Read tag list from config folder
    # Get database of tags
    # tag_db = { tag1:{ID1:path1,ID2:Path2},tag2:{....},...}
    # Iterate through user input list



def main():
    # Load settings
    settings = derpibooru_dl.config_handler(os.path.join("config","derpibooru_dl_config.cfg"))
    # settings to impliment in main settings
    settings.tag_db_file = "config\\tag_db.pkl"

if __name__ == '__main__':
    main()
