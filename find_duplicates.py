#-------------------------------------------------------------------------------
# Name:        move duplicates
# Purpose:
#
# Author:      new
#
# Created:     27/06/2014
# Copyright:   (c) new 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import hashlib
import logging
import os
import derpibooru_dl

def setup_logging(log_file_path):
    # Setup logging (Before running any other code)
    # http://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
    assert( len(log_file_path) > 1 )
    assert( type(log_file_path) == type("") )
    global logger
    log_file_folder =  os.path.split(log_file_path)[0]
    if not os.path.exists(log_file_folder):
        os.makedirs(log_file_folder)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logging.debug('Logging started.')
    return



def uniquify(seq, idfun=None):
    # List uniquifier from
    # http://www.peterbe.com/plog/uniqifiers-benchmark
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


def walk_for_file_paths(start_path):
    """Use os.walk to collect a list of paths to files mathcing input parameters.
    Takes in a starting path and a list of patterns to check against filenames
    Patterns follow fnmatch conventions."""
    logging.debug("Starting walk. start_path:" + start_path)
    assert(type(start_path) == type(""))
    matches = []
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in ['json']]# Scanning /json/ is far too slow for large folders, skip it.
        c = 1
        logging.debug("root: "+root)
        for filename in files:
            c += 1
            if (c % 1000) == 0:
                logging.debug("File # "+str(c)+": "+filename)
            match = os.path.join(root,filename)
            matches.append(match)
        logging.debug("end folder")
    logging.debug("Finished walk.")
    return matches


def hash_file(file_path):
    """Generate a SHA512 hash for a file"""
    # http://www.pythoncentral.io/hashing-files-with-python/
    BLOCKSIZE = 65536
    hasher = hashlib.sha512()
    with open(file_path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    file_hash = u"" + hasher.hexdigest()# convert to unicode
    return file_hash


def find_duplicates(input_folder):
    """Find duplicates in a folder"""
    logging.info("Looking for duplicates in "+input_folder)
    file_paths = walk_for_file_paths(input_folder)
    hash_dict = {} # {hash : file_path}
    hash_matches = []
    logging.info("Generating and compating hashes")
    c = 0
    for file_path in file_paths:
        c += 1
        if (c % 1000) == 0:
            logging.debug("Hashing file #"+str(c)+": "+file_path)
        file_hash = hash_file(file_path)
        # Check if hash has been seen
        try:
            previously_seen = hash_dict[file_hash]
            logging.info("Match! "+hash_dict[file_hash]+" has the same hash as "+file_path)
            # Add both to move list
            hash_matches.append(hash_dict[file_hash])# From hash dict
            hash_matches.append(file_path)# Current
        except KeyError, ke:
            # If no match in dict
            hash_dict[file_hash] = file_path
    # Uniquify move list
    files_to_move = uniquify(hash_matches)
    return files_to_move


def move_duplicates(input_folder,output_folder,no_move=False):
    """Find and move all duplicate files in a folder"""
    duplicates_to_move = find_duplicates(input_folder)
    logging.info("Duplicates found: "+str(duplicates_to_move))
    derpibooru_dl.save_pickle("debug\\found_duplicates.pickle", duplicates_to_move)
    for file_path in duplicates_to_move:
        move_file(from_path, output_folder, no_move)
    logging.info("Done moving duplicates")
    return


def move_file(from_path,output_folder,no_move=False):
    """Move a file to a specified folder or copy it if no_move is True"""
    # Figure out the filename
    filename = os.path.basename(from_path)
    # Make the output path
    output_path = os.path.join(output_folder, filename)
    try:
        # Ensure folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if no_move:
            logging.info("Copying "+from_path+" to "+output_path)
            # Copy file
            shutil.copy2(from_path, output_path)
            return
        else:
            logging.info("Moving "+from_path+" to "+output_path)
            # Move file
            shutil.move(from_path, output_path)
            return
    except IOError, err:
        logging.error("Error copying/moving files!")
        logging.exception(err)
        return


def main():
    input_folder = "h:\\derpibooru_dl\\download\\combined_downloads"
    output_folder = "duplicates"
    move_duplicates(input_folder,output_folder,no_move = True)

if __name__ == '__main__':
    # Setup logging
    setup_logging("debug\\derpibooru_move_duplicate_files_log.txt")
    try:
        #cj = cookielib.LWPCookieJar()
        #setup_browser()
        main()
    except Exception, err:
        # Log exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(err) ) )
        logging.exception(err)
    logging.info( "Program finished.")
    #raw_input("Press return to close")

