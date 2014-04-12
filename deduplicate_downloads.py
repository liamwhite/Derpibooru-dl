#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      new
#
# Created:     28/03/2014
# Copyright:   (c) new 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import derpibooru_dl
import logging
import os
import glob
import re
import shutil

class settings_handler:
    def __init__(self):
        self.set_defaults()
        return

    def set_defaults(self):
        self.downloads_folder = "G:\derpibooru_dl\download"# Folder to process
        self.output_folder = os.path.join(self.downloads_folder,"combined_downloads")# Folder to output to
        self.use_tag_list = True# Use tag list instead of processing everything
        self.move = False# Move files instead of copying them
        self.reverse = False
        self.input_list_path = "config\\tags_to_deduplicate.txt"
        self.done_list_path = "config\\derpibooru_deduplicate_done_list.txt"
        self.combined_download_folder_name = "combined_downloads"# Name of subfolder to use when saving to only one folder
        self.filename_prefix = "derpi_"
        return


def process_submission_data_tuple(settings,submission_data_tuple):
    # Build expected paths
    input_filepath, json_filepath, submission_id = submission_data_tuple
    input_dir, match_filename = os.path.split(input_filepath)
    json_output_filename = os.path.split(json_filepath)[1]
    json_output_folder = os.path.join(settings.output_folder, "json")

    json_output_path = os.path.join(json_output_folder, json_output_filename)
    submission_output_path = os.path.join(settings.output_folder,match_filename)
    # Ensure output path exists
    if not os.path.exists(json_output_folder):
        os.makedirs(json_output_folder)
    if not os.path.exists(settings.output_folder):
        os.makedirs(settings.output_folder)
    # Check that both files exist in the input location and skip if either is missing
    # Ensure output location exists
    # Depending on mode, wither copy or move files to output location
    if settings.move is True:
        # Move over files
        pass
    else:
        # Copy over files
        logging.info("Copying files for submission: "+submission_id+" from "+input_dir+" to "+settings.output_folder)
        try:
            # Copy submission file
            shutil.copy2(input_filepath, submission_output_path)
            # Copy JSON
            shutil.copy2(json_filepath, json_output_path)
            return True
        except IOError, err:
            logging.error("Error copying files!")
            logging.exception(err)
            return False

def generate_image_tuples(settings,input_folder_path):
    """Generate a list of tuples of image file paths and their id numbers.
    e.g. ("download\\derpi_12345.jpg", "12345")"""
    # generate glob string for images
    image_glob_string = os.path.join(input_folder_path, settings.filename_prefix+"*")
    # list image files in folder
    image_files_list = glob.glob(image_glob_string)
    print "image_files_list", image_files_list
    # Extract submission ids from filenames
    image_tuples = []
    for image_file_path in image_files_list:
        image_id_regex = settings.filename_prefix+"(\d+)"
        image_id_search = re.search(image_id_regex,image_file_path)
        if image_id_search:
            image_id = image_id_search.group(1)
            image_tuple = (image_file_path, image_id)
            image_tuples.append(image_tuple)
    print "image_tuples", image_tuples
    return image_tuples

def generate_json_tuples(settings,input_folder_path):
    """Generate a list of tuples of json file paths and their id numbers.
    e.g. ("download\\json\\12345.json", "12345")"""
    # Generate JSON glob string
    json_glob_string = os.path.join(input_folder_path,"json","*.json")
    # list json files
    json_files_list = glob.glob(json_glob_string)
    print "json_files_list", json_files_list
     # Extract JSON ids
    json_tuples = []
    for json_file_path in json_files_list:
        json_id_regex = "(\d+)\.json"
        json_id_search = re.search(json_id_regex,json_file_path)
        if json_id_search:
            json_id = json_id_search.group(1)
            json_tuple = (json_file_path, json_id)
            json_tuples.append(json_tuple)
    print "json_tuples", json_tuples
    return json_tuples

def join_submission_data_lists(settings,image_tuples,json_tuples):
    # Data tuple formats:
    # image_tuple = (image_file_path, image_id)
    # json_tuple = (json_file_path, json_id)
    # joined_file_tuple = (image_file_path, json_file_path, image_id)
    # Sort and join tuples
    joined_files_tuples = []
    for image_tuple in image_tuples:
        image_id = image_tuple[1]
        for json_tuple in json_tuples:
            json_id = json_tuple[1]
            if json_id == image_id:
                image_file_path = image_tuple[0]
                json_file_path = json_tuple[0]
                joined_file_tuple = (image_file_path, json_file_path, image_id)
                joined_files_tuples.append(joined_file_tuple)
    print "joined_files_tuples", joined_files_tuples
    return joined_files_tuples




def generate_submission_data_tuples(settings,input_folder_path):
    image_tuples = generate_image_tuples(settings,input_folder_path)
    json_tuples = generate_json_tuples(settings,input_folder_path)
    # join lists into pairs of filepaths for each submission and its associated JSON
    submission_data_tuples = join_submission_data_lists(settings,image_tuples,json_tuples)
    return submission_data_tuples



def process_folder(settings,folder_name):
    input_folder_path = os.path.join(settings.downloads_folder,folder_name)
    if not os.path.exists(input_folder_path):
        logging.error("specified folder does not exist, cannot process it."+input_folder_path)
        return
    # Buld pairs of submission + metadata files to process
    submission_data_tuples = generate_submission_data_tuples(settings,input_folder_path)
    # Process each pair
    for submission_data_tuple in submission_data_tuples:
        process_submission_data_tuple(settings, submission_data_tuple)



def process_folders(settings,folder_names):
    logging.info("Starting to deduplicate folders")
    for folder_name in folder_names:
        process_folder(settings,folder_name)



def main():
    settings = settings_handler()
    tag_list = derpibooru_dl.import_list(settings.input_list_path)
    process_folders(settings,tag_list)

if __name__ == '__main__':
    # Setup logging
    derpibooru_dl.setup_logging("debug\\derpibooru_deduplicate_log.txt")
    try:
        main()
    except Exception, err:
        # Log exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(err) ) )
        logging.exception(err)
    logging.info( "Program finished.")
    #raw_input("Press return to close")
