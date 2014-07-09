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
        # Ensure dict for tag exists
        try:
            tags_db_dict["tags"][tag]
        except KeyError:
            tags_db_dict["tags"][tag] = {}
            # Add entry to tag dict
        tags_db_dict["tags"][tag][json_id] = json_path
    return tags_db_dict



def read_tags_from_json_file(json_path):
    """Open a derpibooru .JSON file and return the tags from it"""
    # Read JSON
    json_string = derpibooru_dl.read_file(json_path)
    decoded_json = derpibooru_dl.decode_json(json_string)
    # Grab tags
    tag_string_from_json = decoded_json["tags"]
    tags_from_json = tag_string_from_json.split(",")
    #logging.debug(tags_from_json)
    return tags_from_json




def build_tag_db(settings,tag_db_dict={}):
    """Build a db of ids and tags.
    If given, add to existing DB dict, otherwise build one from scratch.
    Format is: tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...} tags:{tag1:{ID1:JSON_path1,ID2:JSON_Path2}, tag2:{....},...}"""
    building_new_db = (len(tag_db_dict) is len({}))
    if building_new_db:
        # Initialize dict
        tag_db_dict["processed"] = {}
        tag_db_dict["tags"] = {}
    logging.debug("Building tag DB")
    # Scan target folder for .JSON files
    target_folder = os.path.join(settings.output_folder, settings.combined_download_folder_name)
    number_of_ids_in_dict = len(tag_db_dict["processed"])
    logging.debug("number of keys in processed listing dict:"+str(number_of_ids_in_dict))
    # Use xrange() to generate paths because it's faster than os.walk() for large folders
    for number in xrange(number_of_ids_in_dict,1000000):
        # Generate path to the json file
        submission_id = str(number)
        json_filename = submission_id+".json"
        json_path = os.path.join(target_folder, "json", json_filename)
        if os.path.exists(json_path):
            # Check if id is in processed dict
            try:
                #tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...},...}
                dummy_path = tag_db_dict["processed"][submission_id]
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
            logging.error("JSON not found for id! "+json_path)
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
    if settings.tag_splitter_update_tag_db:
        new_tag_db_dict = build_tag_db(settings,tag_db_dict_from_file)
        return new_tag_db_dict
    else:
        return tag_db_dict_from_file


def copy_tag(settings,tag_db_dict,tag):
    """Copy all files matching the given tag to a folder /<tag>/ in the output folder.
    Format is: tag_db = {processed:{ID1:JSON_Path1,ID2:JSON_Path2,...} tags:{tag1:{ID1:JSON_path1,ID2:JSON_Path2}, tag2:{....},...}"""
    tag_ids_dict = tag_db_dict["tags"][tag]
    id_to_copy = tag_ids_dict.keys()
    logging.debug("About to copy these items to "+tag+": "+str(id_to_copy))
    output_folder = os.path.join(settings.output_folder,tag)
    for id_to_copy in ids_to_copy:
        derpibooru_dl.copy_over_if_duplicate(settings,id_to_copy,output_folder)


def copy_tag_list(settings):
    # Read tag list from config folder
    user_input_list = derpibooru_dl.import_list(listfilename=settings.tag_splitter_tag_list_path)
    # Get database of tags
    tag_db_dict = get_tag_db(settings)
    # Iterate through user input list
    counter = 0
    for tag in user_input_list:
        tag += u""# convert input to unicode
        counter += 1
        logging.debug("Now copying tag "+str(counter)+" of "+str(len(user_input_list))+":"+tag)
        tag_db_dict = copy_tag(settings,tag_db_dict,tag)
    logging.info("Done copying tags")
    pass



def main():
    derpibooru_dl.setup_logging("debug\\tag_splitter_log.txt")
    # Load settings
    settings = derpibooru_dl.config_handler(os.path.join("config","derpibooru_dl_config.cfg"))
    # Settings to impliment in main settings TODO
    settings.tag_splitter_tag_db_file_path = "config\\tag_db.pkl"
    settings.tag_splitter_tag_list_path = "config\\tags_to_split.txt"
    settings.tag_splitter_update_tag_db = False
    settings.tag_splitter_speedhack = True # Speedhacks for tag splitter, for dev's computer only
    copy_tag_list(settings)

if __name__ == '__main__':
    main()
