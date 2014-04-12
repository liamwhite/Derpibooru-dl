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




class settings_handler:
    def __init__(self):
        set_defaults()
        return

    def set_defaults(self):
        self.downloads_folder = ""# Folder to process
        self.output_folder = "combined_downloads"# Folder to output to
        self.use_tag_list = True# Use tag list instead of processing everything
        self.move = False# Move files instead of copying them
        self.reverse = False
        self.input_list_path = "config\\tags_to_deduplicate.txt"
        self.done_list_path = "config\\derpibooru_deduplicate_done_list.txt"
        self.combined_download_folder_name = "combined_downloads"# Name of subfolder to use when saving to only one folder
        self.filename_prefix = "derpi_"
        return

def copy_submission_pair(settings,submission_data_pair):






def process_submission_data_pair(settings,submission_data_pair):
    # Build expected paths
    input_dir, match_filename = os.path.split(glob_match)
    expected_json_input_filename = submission_id+".json"
    expected_json_input_location = submission_data_pair[1]
    json_output_folder = os.path.join(output_folder, "json")
    json_output_path = os.path.join(json_output_folder, json_output_filename)
    submission_output_path = os.path.join(settings.output_folder,match_filename)
    # Ensure output path exists
    if not os.path.exists(json_output_folder):
        os.makedirs(json_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
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
            shutil.copy2(glob_match, submission_output_path)
            # Copy JSON
            shutil.copy2(expected_json_input_location, json_output_path)
            return True
        except IOError, err:
            logging.error("Error copying files!")
            logging.exception(err)
            return False

def join_submission_data_lists(settings,image_files_list,json_files_list)

def generate_submission_data_pairs(settings,input_folder_path)
    # generate glob string for images
    image_glob_string = input_folder_path+settings.filename_prefix+"*"
    # list image files in folder
    image_glob_matches = glob.glob(glob_string)
    # Generate JSON glob string
    json_glob_string = input_folder_path+settings.filename_prefix+"*"
    # list json files
    json_glob_matches = glob.glob(glob_string)
    # join lists into pairs of filepaths for each submission and its associated JSON



def process_folder(settings,folder_name):
    input_folder_path = os.path.join(settings.downloads_folder,folder_name)
    if not os.path.exists(input_folder_path):
        logging.error("specified folder does not exist, cannot process it."+input_folder_path)
        return
    # Buld pairs of submission + metadata files to process
    submission_data_pairs = generate_submission_data_pairs(settings,input_folder_path)
    # Process each pair
    for submission_data_pair in submission_data_pairs:
        process_submission_data_pair(settings, submission_data_pair)



def process_folders(settings,folder_names):
    logging.info("Starting to deduplicate folders")
    for folder_name in folder_names:
        process_folder(settings,folder_name)



def main():
    settings = settings_handler()
    tag_list = derpibooru_dl.import_list(settings.input_list_path)
    process_folders(settings,folder_names)

if __name__ == '__main__':
    # Setup logging
    derpibooru_dl.setup_logging("debug\\derpibooru_deduplicate_log.txt")
    try:
        main()
    except Exception, err:
        # Log exceptions
        logger.critical("Unhandled exception!")
        logger.critical(str( type(err) ) )
        logging.exception(err)
    logging.info( "Program finished.")
    #raw_input("Press return to close")
