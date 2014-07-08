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


import os
import logging

import derpibooru_dl




def add_tags_to_dict(settings,tags_db_dict,json_id,json_path,tags):
    """Add the specified tags to the dict and return the new one
    Format is: tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...} tags:{tag1:{ID1:JSON_path1,ID2:JSON_Path2}, tag2:{....},...}"""
    for tag in tags:
        tags_db_dict["tags"][tag][id_number] = json_path
    return tags_db_dict



def read_tags_from_json_file(json_path):
    """Open a derpibooru .JSON file and return the tags from it"""
    # Read JSON
    json_string = read_file(json_path)
    decoded_json = derpibooru_dl.decode_json(json_string)
    # Grab tags
    tags_from_json = decoded_json["tags"]
    logging.debug(tags_from_json)#remove
    return tags_from_json




def build_tag_db(settings,tag_db_dict={}):
    """Build a db of ids and tags.
    If given, add to existing DB dict, otherwise build one from scratch.
    Format is: tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...} tags:{tag1:{ID1:JSON_path1,ID2:JSON_Path2}, tag2:{....},...}"""
    building_new_db = (len(tag_db_dict) is len({}))
    logging.debug("Building tag DB")
    # Scan target folder for .JSON files
    target_folder = settings.output_folder
    #if settings.tag_splitter_speedhack:
    # Speedhack, don't use unless you understand the code
    # Generate paths for every submission rather than look for paths from disk
    generated_submission_paths = []
    for number in xrange(0,1000000):
        generated_submission_path = os.path.join(target_folder, "json", str(number)+".JSON")
    #found_submission_paths = derpibooru_dl.walk_for_file_paths(target_folder)
    # For each JSON file, get ID from filename
        logging.debug("Processing JSON for DB")
    #for found_submission_path in found_submission_paths:
        found_submission_path = generated_submission_path
        # Generate path to the json file
        submission_id = derpibooru_dl.find_id_from_filename(settings, found_submission_path)
        json_filename = submission_id+".json"
        json_path = os.path.join(target_folder, "json", json_filename)
        if os.path.exists(json_path):
            # Check if id is in processed dict
            try:
                #tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...},...}
                dummy_path = tag_db["processed"][submission_id]
                # True; ID has been processed.
                pass
            except KeyError:
                # False; ID has not been processed.
                logging.debug("New JSON found, reading. "+json_path)
                # If ID is not yet processed, read tags from json
                tags = read_tags_from_json_file(json_path)
                # add to dict
                tag_db_dict = add_tags_to_dict(settings,tag_db_dict,submission_id,json_path,tags)

        else:
            logging.error("JSON not found for submission! "+found_submission_path)
    #Once all paths are processed, return finished dict
    return tag_db_dict


def load_tag_db_pickle(settings):
    """Either load a valid tag DB from pickle or return an empty dict"""
    # Check for existing DB in pickle path
    if os.path.exists(settings.tag_splitter_tag_db_file_path):
        data_from_file = read_pickle(settings.tag_splitter_tag_db_file_path)
        if type(data_from_file == type({})):
            return data_from_file
    logging.error("Error loading tag db from file! Using an empty one instead.")
    # If any test fails, return empty dict
    return {}


def get_tag_db(settings):
    """Get a dictionary containing the tag info through whatever means needed.
    Format is: tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...} tags:{tag1:{ID1:JSON_path1,ID2:JSON_Path2}, tag2:{....},...}"""
    # tag_db = { tag1:{ID1:path1,ID2:Path2},tag2:{....},...}
    # Try loading from saved pickle
    tag_db_dict_from_file = load_tag_db_pickle(settings)
    new_tag_db_dict = build_tag_db(settings,tag_db_dict_from_file)
    return new_tag_db_dict


def copy_tag(settings,tag_db_dict,tag):
    """Copy all files matching the given tag to a folder /<tag>/ in the output folder.
    Format is: tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...} tags:{tag1:{ID1:JSON_path1,ID2:JSON_Path2}, tag2:{....},...}"""
    tag_ids_dict = tag_db_dict["tags"][tag]


def copy_tag_list(settings):
    # Read tag list from config folder
    user_input_list = derpibooru_dl.import_list(listfilename=settings.tag_splitter_tag_list_path)
    # Get database of tags
    tag_db_dict = get_tag_db(settings)
    # Iterate through user input list
    for tag in user_input_list:
        tag_db_dict = copy_tag(settings,tag_db_dict,tag)
    pass



def main():
    derpibooru_dl.setup_logging("debug\\tag_splitter_log.txt")
    # Load settings
    settings = derpibooru_dl.config_handler(os.path.join("config","derpibooru_dl_config.cfg"))
    # Settings to impliment in main settings TODO
    settings.tag_splitter_tag_db_file_path = "config\\tag_db.pkl"
    settings.tag_splitter_tag_list_path = "config\\tags_to_split.txt"
    settings.tag_splitter_speedhack = True # Speedhacks for tag splitter, for dev's computer only
    copy_tag_list(settings)

if __name__ == '__main__':
    main()
