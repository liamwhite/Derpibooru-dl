#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      new
#
# Created:     08/02/2014
# Copyright:   (c) new 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import time
import os
import sys
import re
import mechanize
import cookielib
import logging
import urllib2
import httplib
import random
import glob
import ConfigParser
import HTMLParser
import json
import shutil
import pickle
import socket




# getwithinfo()
GET_REQUEST_DELAY = 0
GET_RETRY_DELAY = 30
GET_MAX_ATTEMPTS = 20




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


def add_http(url):
    """Ensure a url starts with http://..."""
    if "http://" in url:
        return url
    elif "https://" in url:
        return url
    else:
        #case //derpicdn.net/img/view/...
        first_two_chars = url[0:2]
        if first_two_chars == "//":
            output_url = "http:"+url
            return output_url
        else:
            logging.error(str(locals()))
            raise ValueError


def deescape(html):
    # de-escape html
    # http://stackoverflow.com/questions/2360598/how-do-i-unescape-html-entities-in-a-string-in-python-3-1
    deescaped_string = HTMLParser.HTMLParser().unescape(html)
    return deescaped_string


def get(url):
    #try to retreive a url. If unable to return None object
    #Example useage:
    #html = get("")
    #if html:
    assert_is_string(url)
    deescaped_url = deescape(url)
    url_with_protocol = add_http(deescaped_url)
    gettuple = getwithinfo(url_with_protocol)
    if gettuple:
        reply, info = gettuple
        return reply


def getwithinfo(url):
    """Try to retreive a url. If unable to return None objects
    Example useage:
    html = get("")
        if html:
    """
    attemptcount = 0
    while attemptcount < GET_MAX_ATTEMPTS:
        attemptcount = attemptcount + 1
        if attemptcount > 1:
            logging.debug( "Attempt " + str(attemptcount) + " for URL: " + url )
        try:
            save_file("debug\\get_last_url.txt", url, True)
            r = br.open(url, timeout=100)
            info = r.info()
            reply = r.read()
            delay(GET_REQUEST_DELAY)
            # Save html responses for debugging
            #print info
            #print info["content-type"]
            if "html" in info["content-type"]:
                #print "saving debug html"
                save_file("debug\\get_last_html.htm", reply, True)
            else:
                save_file("debug\\get_last_not_html.txt", reply, True)
            # Retry if empty response and not last attempt
            if (len(reply) < 1) and (attemptcount < GET_MAX_ATTEMPTS):
                logging.error("reply too short :"+str(reply))
                continue
            return reply,info
        except urllib2.HTTPError, err:
            logging.debug(str(err))
            if err.code == 404:
                logging.debug("404 error! " + str(url))
                return
            elif err.code == 403:
                logging.debug("403 error, ACCESS DENIED! url: "+str(url))
                return
            elif err.code == 410:
                logging.debug("410 error, GONE")
                return
            else:
                save_file("debug\\HTTPError.htm", err.fp.read(), True)
                continue
        except urllib2.URLError, err:
            logging.debug(str(err))
            if "unknown url type:" in err.reason:
                return
            else:
                continue
        except httplib.BadStatusLine, err:
            logging.debug(str(err))
            continue
        except httplib.IncompleteRead, err:
            logging.debug(str(err))
            continue
        except mechanize.BrowserStateError, err:
            logging.debug(str(err))
            continue
        except socket.timeout, err:
            logging.debug(str( type(err) ) )
            logging.debug(str(err))
            continue
        delay(GET_RETRY_DELAY)
    return


def save_file(filenamein,data,force_save=False):
    if not force_save:
        if os.path.exists(filenamein):
            logging.debug("file already exists! "+str(filenamein))
            return
    sanitizedpath = filenamein# sanitizepath(filenamein)
    foldername = os.path.dirname(sanitizedpath)
    if len(foldername) >= 1:
        if not os.path.isdir(foldername):
            os.makedirs(foldername)
    file = open(sanitizedpath, "wb")
    file.write(data)
    file.close()
    return


def delay(basetime,upperrandom=0):
    #replacement for using time.sleep, this adds a random delay to be sneaky
    sleeptime = basetime + random.randint(0,upperrandom)
    #logging.debug("pausing for "+str(sleeptime)+" ...")
    time.sleep(sleeptime)


def sanitizepath(pathin):
    #from pathsanitizer
    #sanitize a filepath for use on windows
    #http://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx
    assert(type(pathin)==type(""))
    segments = []
    workingpath = pathin# make a copy for easier debugging
    #print "sanitizepathdebug! workingpath", workingpath
    #split the path into segments
    while True:
        workingpath, segment = os.path.split(workingpath)
        segments.append(segment)
        #print "sanitizepathdebug! segments, segment", segments, segment
        if len(workingpath) <= 1:
            break
    segments.reverse()
    #sanitize segments
    precessedsegments = []
    for segment in segments:
        s0 = re.sub('[^A-Za-z0-9\ \.\_]+', '-', segment)#remove all non-alphanumeric
        s1 = s0.strip()#strip whitespace so it doesn't get turned into hyphens
        s2 = re.sub('[<>:"/\|?*]+', '-',s1)#remove forbidden characters
        s3 = s2.strip()#strip whitespace
        s4 = s3.strip(".-")#strip characters that shouldn't be at ends of filenames
        s5 = re.sub(r"\ +", " ", s4)#remove repeated spaces
        s6 = re.sub(r"\-+", "-", s5)#remove repeated hyphens
        s7 = re.sub(r"\_+", "_", s6)#remove repeated underscores
        s8 = s7.strip()# Strip whitespace
        precessedsegments.append(s8)
    #join segments
    pathout = os.path.join(*precessedsegments)
    assert(type(pathout)==type(""))
    return pathout


def import_list(listfilename="ERROR.txt"):
    nameslist = []
    if os.path.exists(listfilename):#check if there is a list
        nameslist = []#make an empty list
        listfile = open(listfilename, 'rU')
        for line in listfile:
            if line[0] != '#' and line[0] != '\n':#skip likes starting with '#' and the newline character
                if line[-1] == '\n':#remove trailing newline if it exists
                    stripped_line = line[:-1]
                else:
                    stripped_line = line#if no trailing newline exists, we dont need to strip it
                replaced_line = re.sub(" ", '+', stripped_line)# Replace spaces with plusses
                nameslist.append(replaced_line)#add the username to the list
        listfile.close()
        return nameslist
    else:#if there is no list, make one
        listfile = open(listfilename, 'w')
        listfile.write('#add one tag per line, comments start with a #, nothing but tag on a lise that isnt a comment\n')
        listfile.close()
        return []


def append_list(lines,list_file_path="weasyl_done_list.txt",initial_text="# List of completed items.\n",overwrite=False):
    # Append a string or list of strings to a file; If no file exists, create it and append to the new file.
    # Strings will be seperated by newlines.
    # Make sure we're saving a list of strings.
    if ((type(lines) is type(""))or (type(lines) is type(u""))):
        lines = [lines]
    # Ensure file exists and erase if needed
    if (not os.path.exists(list_file_path)) or (overwrite is True):
        list_file_segments = os.path.split(list_file_path)
        list_dir = list_file_segments[0]
        if list_dir:
            if not os.path.exists(list_dir):
                os.makedirs(list_dir)
        nf = open(list_file_path, "w")
        nf.write(initial_text)
        nf.close()
    # Write data to file.
    f = open(list_file_path, "a")
    for line in lines:
        outputline = line+"\n"
        f.write(outputline)
    f.close()
    return


class config_handler():
    def __init__(self,settings_path="derpibooru_dl_config.cfg"):
        self.set_defaults()
        self.load_file(settings_path)
        self.save_settings(settings_path)
        return

    def set_defaults(self):
        # Login
        self.api_key = ""

        # Download Settings
        self.reverse = False
        self.output_folder = "download"# Root path to download to
        self.download_submission_ids_list = True
        self.download_query_list = True
        self.output_long_filenames = False # Should we use the derpibooru supplied filename with the tags? !UNSUPPORTED!
        self.input_list_path = "config\\derpibooru_dl_tag_list.txt"
        self.done_list_path = "config\\derpibooru_done_list.txt"
        self.failed_list_path = "config\\derpibooru_failed_list.txt"
        self.save_to_query_folder = True # Should we save to multiple folders?
        self.skip_downloads = False # Don't retrieve remote submission files after searching
        self.sequentially_download_everything = False # download submission 1,2,3...
        self.go_backwards_when_using_sequentially_download_everything = False # when downloading everything in range mode should we go 10,9,8,7...?
        self.download_last_week = False # Download (approximately) the last weeks submissions

        # Internal variables, these are set through this code only
        self.resume_file_path = "config\\resume.pkl"
        self.pointer_file_path = "config\\dl_everything_pointer.pkl"
        self.filename_prefix = "derpi_"
        self.sft_max_attempts = 10 # Maximum retries in search_for_tag()
        self.max_search_page_retries = 10 # maximum retries for a search page
        self.combined_download_folder_name = "combined_downloads"# Name of subfolder to use when saving to only one folder
        self.max_download_attempts = 10 # Number of times to retry a download before skipping
        return

    def load_file(self,settings_path):
        config = ConfigParser.RawConfigParser()
        if not os.path.exists(settings_path):
            return
        config.read(settings_path)
        # Login
        try:
            self.api_key = config.get('Login', 'api_key')
        except ConfigParser.NoOptionError:
            pass
        # Download Settings
        try:
            self.reverse = config.getboolean('Settings', 'reverse')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.output_folder = config.get('Settings', 'output_folder')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.download_submission_ids_list = config.getboolean('Settings', 'download_submission_ids_list')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.download_query_list = config.getboolean('Settings', 'download_query_list')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.output_long_filenames = config.getboolean('Settings', 'output_long_filenames')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.input_list_path = config.get('Settings', 'input_list_path')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.done_list_path = config.get('Settings', 'done_list_path')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.failed_list_path = config.get('Settings', 'failed_list_path')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.save_to_query_folder = config.getboolean('Settings', 'save_to_query_folder')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.skip_downloads = config.getboolean('Settings', 'skip_downloads')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.sequentially_download_everything = config.getboolean('Settings', 'sequentially_download_everything')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.go_backwards_when_using_sequentially_download_everything = config.getboolean('Settings', 'go_backwards_when_using_sequentially_download_everything')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.download_last_week = config.getboolean('Settings', 'download_last_week')
        except ConfigParser.NoOptionError:
            pass
        return

    def save_settings(self,settings_path):
        config = ConfigParser.RawConfigParser()
        config.add_section('Login')
        config.set('Login', 'api_key', self.api_key )
        config.add_section('Settings')
        config.set('Settings', 'reverse', str(self.reverse) )
        config.set('Settings', 'output_folder', self.output_folder )
        config.set('Settings', 'download_submission_ids_list', str(self.download_submission_ids_list) )
        config.set('Settings', 'download_query_list', str(self.download_query_list) )
        config.set('Settings', 'output_long_filenames', str(self.output_long_filenames) )
        config.set('Settings', 'input_list_path', self.input_list_path )
        config.set('Settings', 'done_list_path', self.done_list_path )
        config.set('Settings', 'failed_list_path', self.failed_list_path )
        config.set('Settings', 'save_to_query_folder', str(self.save_to_query_folder) )
        config.set('Settings', 'skip_downloads', str(self.skip_downloads) )
        config.set('Settings', 'sequentially_download_everything', str(self.sequentially_download_everything) )
        config.set('Settings', 'go_backwards_when_using_sequentially_download_everything', str(self.go_backwards_when_using_sequentially_download_everything) )
        config.set('Settings', 'download_last_week', str(self.download_last_week) )
        with open(settings_path, 'wb') as configfile:
            config.write(configfile)
        return



def assert_is_string(object_to_test):
    """Make sure input is either a string or a unicode string"""
    if( (type(object_to_test) == type("")) or (type(object_to_test) == type(u"")) ):
        return
    logging.critical(str(locals()))
    raise(ValueError)


def decode_json(json_string):
    """Wrapper for JSON decoding
    Return None object if known problem case occurs
    Return decoded data if successful
    Reraise unknown cases for caught exceptions"""
    assert_is_string(json_string)
    try:
        json_data = json.loads(json_string)
        return json_data
    except ValueError, err:
        # Retry if bad json recieved
        if "Unterminated string starting at:" in str(err):
            logging.debug("JSON data invalid, failed to decode.")
            logging.debug(json_string)
            return
        elif "No JSON object could be decoded" in str(err):
            if len(json_string) < 20:
                logging.debug("JSON string was too short!")
                logging.debug(json_string)
                return
            else:
                logging.critical(locals())
                raise(err)
        # Log locals and crash if unknown issue
        else:
            logging.critical(locals())
            raise(err)


def read_file(path):
    """grab the contents of a file"""
    f = open(path, "r")
    data = f.read()
    f.close()
    return data


def setup_browser():
    #Initialize browser object to global variable "br" using cokie jar "cj"
    # Browser
    global br
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    # User-Agent (this is cheating, ok?)
    #br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.addheaders = [('User-agent', 'Trixie is worst pony')]#[13:57] <%barbeque> as long as it's not something like "trixie is worst pony"
    #print "trixie is worst pony"
    return


def load_search_page(settings,search_url):
    global search_page_dict
    attempt_counter = 0
    while attempt_counter <= settings.max_search_page_retries:
        attempt_counter += 1
        # Load page
        search_page = get(search_url)
        if search_page is None:
            break
        #print search_page
        if len(search_page) < 5:
            logging.debug("Search page is very small!")
            logging.debug( locals() )
        # Extract submission_ids from page
        # Convert JSON to dict
        assert_is_string(search_page)
        try:
            search_page_dict = json.loads(search_page)
        except ValueError, err:
            logging.error("Failed to read JSON on attempt "+str(attempt_counter)+"for url"+search_url)
            logging.error( locals() )
            continue
        page_keys = search_page_dict.keys()
        logging.debug(page_keys)
        first_key = page_keys[0]
        search_page_list = search_page_dict[first_key]
        #print search_page_list
        assert( type( search_page_list ) == type( [] ) )# This should be a list
        try:
            # Extract item ids
            this_page_item_ids = []
            for item_dict in search_page_list:
                if item_dict is None:
                    continue
                item_id = item_dict["id_number"]
                this_page_item_ids.append(str(item_id))
        except TypeError, err:
            logging.error( str( type(err ) ) )
            logging.error( locals() )
            logging.debug("saving local variables to pickle")
            save_pickle("debug\\locals.pickle",locals())
            logging.exception(err)
        print this_page_item_ids
        return this_page_item_ids
    logging.error("Too many failed retries loading search page, failing.")
    return


def search_for_query(settings,search_query):
    """Perform search for a query on derpibooru.
    Return a lost of found submission IDs"""
    assert_is_string(search_query)
    logging.debug("Starting search for tag: "+search_query)
    page_counter = 0 # Init counter
    max_pages = 5000 # Saftey limit
    found_submissions = []
    last_page_items = []
    while page_counter <= max_pages:
        # Incriment page counter
        page_counter += 1
        logging.debug("Scanning page "+str(page_counter)+" for query: "+search_query)
        # Generate page URL
        search_url = "https://derpibooru.org/search.json?q="+search_query+"&page="+str(page_counter)+"&key="+settings.api_key+"&nocomments=1&nofave=1"
        # Load and process page
        this_page_item_ids = load_search_page(settings,search_url)
        # Test if submissions seen are duplicates
        if this_page_item_ids == last_page_items:
            logging.debug("This pages items match the last pages, stopping search.")
            break
        last_page_items = this_page_item_ids
        # Append this pages item ids to main list
        found_submissions += this_page_item_ids
    # Return found items
    return found_submissions


def detect_redirect_page(html):
    """Detect tag redirect notice.
    If tag is a redirect return the aliased tag. Else return False"""
    if """) has been aliased to the tag""" in html:
        # find aliased tag
        # flash notice">This tag (&#39;yawning&#39;) has been aliased to the tag &#39;yawn&#39;</div><div id="content"
        redirect_tag_search_regex = """\)\s+?has\s+?been\s+?aliased\s+?to\s+?the\s+?tag\s+?&\#39;([^&]+)&\#39;</div>"""
        redirect_tag_search = re.search(redirect_tag_search_regex, html)
        if redirect_tag_search:
            raw_tag = redirect_tag_search.group(1)
            # fix for colon not being derpiboorus preferred -colon- e.g. tags/artist:kabutoro
            if ":" in raw_tag:
                tag = raw_tag.replace(":", "-colon-")
                return tag
            else:
                return raw_tag
    else:
        return False


def check_if_deleted_submission(json_dict):
    """Check whether the JSON Dict for a submission shows it as being deleted"""
    keys = json_dict.keys()
    if "deletion_reason" in keys:
        logging.error("Deleted submission! Reason: "+str(json_dict["deletion_reason"]))
        return True
    elif "duplicate_of" in keys:
        logging.error("Deleted duplicate submission! Reason: "+str(json_dict["duplicate_of"]))
        return True
    else:
        return False


def copy_over_if_duplicate(settings,submission_id,output_folder):
    """Check if there is already a copy of the submission downloaded in the download path.
    If there is, copy the existing version to the suppplied output location then return True
    If no copy can be found, return False"""
    assert_is_string(submission_id)
    # Generate expected filename pattern
    expected_submission_filename = "*"+submission_id+".*"
    # Generate search pattern
    glob_string = os.path.join(settings.output_folder, "*", expected_submission_filename)
    # Use glob to check for existing files matching the expected pattern
    glob_matches = glob.glob(glob_string)
    # Check if any matches, if no matches then return False
    if len(glob_matches) == 0:
        return False
    else:
        # If there is an existing version:
        for glob_match in glob_matches:
            # If there is an existing version in the output path, nothing needs to be copied
            if output_folder in glob_match:
                return False
            else:
                # Copy over submission file and metadata JSON
                logging.info("Trying to copy from previous download: "+glob_match)
                # Check output folders exist
                # Build expected paths
                match_dir, match_filename = os.path.split(glob_match)
                expected_json_input_filename = submission_id+".json"
                expected_json_input_folder = os.path.join(match_dir, "json")
                expected_json_input_location = os.path.join(expected_json_input_folder, expected_json_input_filename)
                json_output_folder = os.path.join(output_folder, "json")
                json_output_filename = submission_id+".json"
                json_output_path = os.path.join(json_output_folder, json_output_filename)
                submission_output_path = os.path.join(output_folder,match_filename)
                # Redownload if a file is missing
                if not os.path.exists(glob_match):
                    logging.debug("Submission file to copy is missing.")
                    return False
                if not os.path.exists(expected_json_input_location):
                    logging.debug("JSON file to copy is missing.")
                    return False
                # Ensure output path exists
                if not os.path.exists(json_output_folder):
                    os.makedirs(json_output_folder)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                logging.info("Copying files for submission: "+submission_id+" from "+match_dir+" to "+output_folder)
                # Copy over files
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


def download_submission(settings,search_query,submission_id):
    """Download a submission from Derpibooru"""
    assert_is_string(search_query)
    submission_id = str(submission_id)
    setup_browser()
    query_for_filename = convert_query_for_path(settings,search_query)
    #logging.debug("Downloading submission:"+submission_id)
    # Build JSON paths
    json_output_filename = submission_id+".json"
    if settings.save_to_query_folder is True:
        json_output_path = os.path.join(settings.output_folder,query_for_filename,"json",json_output_filename)
    else:
        # Option to save to a single combined folder
        json_output_path = os.path.join(settings.output_folder,settings.combined_download_folder_name,"json",json_output_filename)
    # Check if download can be skipped
    # Check if JSON exists
    if os.path.exists(json_output_path):
        logging.debug("JSON for this submission already exists, skipping.")
        return
    # Build output folder path
    if settings.save_to_query_folder is True:
        output_folder = os.path.join(settings.output_folder,query_for_filename)
    else:
        # Option to save to a single combined folder
        output_folder = os.path.join(settings.output_folder,settings.combined_download_folder_name)
    # Check for dupliactes in download folder
    if copy_over_if_duplicate(settings, submission_id, output_folder):
        return
    # Option to skip loading remote submission files
    if settings.skip_downloads is True:
        return
    # Build JSON URL
    json_url = "https://derpibooru.org/"+submission_id+".json?key="+settings.api_key
    # Retry if needed
    download_attempt_counter = 0
    while download_attempt_counter <= settings.max_download_attempts:
        download_attempt_counter += 1
        # Load JSON URL
        json_page = get(json_url)
        if not json_page:
            continue
        # Convert JSON to dict
        json_dict = decode_json(json_page)
        if json_dict is None:
            continue
        # Check if submission is deleted
        if check_if_deleted_submission(json_dict):
            logging.debug("Submission was deleted.")
            logging.debug(json_page)
            return
        # Extract needed info from JSON
        image_url = json_dict["image"]
        image_filename = json_dict["file_name"]
        image_file_ext = json_dict["original_format"]
        image_height = json_dict["height"]
        image_width = json_dict["width"]
        # Build image output filenames
        if settings.output_long_filenames:
            image_output_filename = settings.filename_prefix+image_filename+"."+image_file_ext
        else:
            image_output_filename = settings.filename_prefix+submission_id+"."+image_file_ext
        image_output_path = os.path.join(output_folder,image_output_filename)
        # Load image data
        authenticated_image_url = image_url+"?key="+settings.api_key
        logging.debug("Loading submission image. Height:"+str(image_height)+", Width:"+str(image_width)+", URL: "+authenticated_image_url)
        image_data = get(authenticated_image_url)
        if not image_data:
            return
        # Image should always be bigger than this, if it isn't we got a bad file
        if len(image_data) < 100:
            logging.error("Image data was too small! "+str(image_data))
            continue
        # Save image
        save_file(image_output_path, image_data, True)
        # Save JSON
        save_file(json_output_path, json_page, True)
        logging.debug("Download successful")
        return
    return


def read_pickle(file_path):
    file_data = read_file(file_path)
    pickle_data = pickle.loads(file_data)
    return pickle_data


def save_pickle(path,data):
    # Save data to pickle file
    # Ensure folder exists.
    if not os.path.exists(path):
        pickle_path_segments = os.path.split(path)
        pickle_dir = pickle_path_segments[0]
        if pickle_dir:# Make sure we aren't at the script root
            if not os.path.exists(pickle_dir):
                os.makedirs(pickle_dir)
    pf = open(path, "wb")
    pickle.dump(data, pf)
    pf.close()
    return


def save_resume_file(settings,search_tag,submission_ids):
    # Save submissionIDs and search_tag to pickle
    logging.debug("Saving resume data pickle")
    # {"search_tag":"FOO", "submission_ids":["1","2"]}
    # Build dict
    resume_dict = {
    "search_tag":search_tag,
    "submission_ids":submission_ids
    }
    save_pickle(settings.resume_file_path, resume_dict)
    return


def clear_resume_file(settings):
    # Erase pickle
    logging.debug("Erasing resume data pickle")
    if os.path.exists(settings.resume_file_path):
        os.remove(settings.resume_file_path)
    return


def resume_downloads(settings):
    # Look for pickle of submissions to iterate over
    if os.path.exists(settings.resume_file_path):
        logging.debug("Resuming from pickle")
        # Read pickle:
        resume_dict = read_pickle(settings.resume_file_path)
        search_tag = resume_dict["search_tag"]
        submission_ids = resume_dict["submission_ids"]
        # Iterate over submissions
        download_submission_id_list(settings,submission_ids,search_tag)
        # Clear temp file
        clear_resume_file(settings)
        append_list(search_tag, settings.done_list_path)
        return search_tag
    else:
        return False


def download_submission_id_list(settings,submission_ids,query):
    # Iterate over submissions
    submission_counter = 0
    # If no submissions to save record failure
    if len(submission_ids) == 0:
        logging.warning("No submissions to save! Query:"+str(query))
        append_list(query, settings.failed_list_path, initial_text="# List of failed items.\n")
    if settings.reverse:
        logging.info("Reverse mode is active, reversing download order.")
        submission_ids.reverse()
    for submission_id in submission_ids:
        submission_counter += 1
        # Only save pickle every 1000 items to help avoid pickle corruption
        if (submission_counter % 1000) == 0:
            cropped_submission_ids = submission_ids[( submission_counter -1 ):]
            save_resume_file(settings,query,cropped_submission_ids)
        logging.debug("Now working on submission "+str(submission_counter)+" of "+str(len(submission_ids) )+" : "+submission_id+" for: "+query )
        # Try downloading each submission
        download_submission(settings, query, submission_id)
        print "\n\n"
    return


def save_pointer_file(settings,start_number,finish_number):
    """Save start and finish numbers to pickle"""
    logging.debug("Saving resume data pickle")
    # {"start_number":0, "finish_number":100}
    # Build dict
    resume_dict = {
    "start_number":start_number,
    "finish_number":finish_number
    }
    save_pickle(settings.pointer_file_path, resume_dict)
    return


def clear_pointer_file(settings):
    """Erase range download pickle"""
    logging.debug("Erasing resume data pickle")
    if os.path.exists(settings.pointer_file_path):
        os.remove(settings.pointer_file_path)
    return


def get_latest_submission_id(settings):
    """Find the most recent submissions ID"""
    search_url = "https://derpibooru.org/images.json?key="+settings.api_key+"&nocomments=1&nofave=1"
    latest_submissions = load_search_page(settings,search_url)
    ordered_latest_submissions = sorted(latest_submissions)
    latest_submission_id = int(ordered_latest_submissions[0])
    return latest_submission_id


def download_this_weeks_submissions(settings):
    """Download (about) one weeks worth of the most recent submissions"""
    # Get starting number
    latest_submission_id = get_latest_submission_id(settings)
    # Calculate ending number
    one_weeks_submissions_number = 1000 * 7 # less than 1000 per day
    finish_number = latest_submission_id - one_weeks_submissions_number  # Add a thousand to account for new submissions added during run
    logging.info("Downloading the last "+str(one_weeks_submissions_number)+" submissions. Starting at "+str(latest_submission_id)+" and stopping at "+str(finish_number))
    download_range(settings,latest_submission_id,finish_number)
    return


def download_everything(settings):
    """Start downloading everything or resume downloading everything"""
    logging.info("Downloading everything by range")
    # Start downloading everything
    latest_submission_id = get_latest_submission_id(settings)
    start_number = 0
    finish_number = latest_submission + 1000 # Add a thousand to account for new submissions added during run
    if settings.go_backwards_when_using_sequentially_download_everything:
        # Swap start and finish numbers for backwards mode
        start_number, finish_number =  finish_number, start_number
    download_range(settings,start_number,finish_number)
    return


def resume_range_download(settings):
    # Look for pickle of range to iterate over
    if os.path.exists(settings.pointer_file_path):
        logging.info("Resuming range from pickle")
        # Read pickle:
        resume_dict = read_pickle(settings.pointer_file_path)
        start_number = resume_dict["start_number"]
        finish_number = resume_dict["finish_number"]
        # Iterate over range
        download_range(settings,start_number,finish_number)
    return


def download_range(settings,start_number,finish_number):
    """Try to download every submission within a given range
    If finish number is less than start number, run over the range backwards"""
    # If starting point is after end point, we're going backwards
    if(start_number > finish_number):
        backwards = True
    else:
        backwards = False
    assert(finish_number <= 1000000)# less than 1 million, 634,101 submissions as of 23-5-2014
    assert(start_number >= 0)# First submission is ID 0
    assert(type(finish_number) is type(1))# Must be integer
    assert(type(start_number) is type(1))# Must be integer
    total_submissions_to_attempt = abs(finish_number - start_number)
    logging.info("Downloading range: "+str(start_number)+" to "+str(finish_number))
    # Iterate over range of id numbers
    submission_pointer = start_number
    loop_counter = 0
    while (loop_counter <= total_submissions_to_attempt ):
        loop_counter += 1
        assert(submission_pointer >= 0)# First submission is ID 0
        assert(submission_pointer <= 1000000)# less than 1 million, 634,101 submissions as of 23-5-2014
        assert(type(submission_pointer) is type(1))# Must be integer
        # Only save pickle every 1000 items to help avoid pickle corruption
        if (submission_pointer % 1000) == 0:
            save_pointer_file(settings, submission_pointer, finish_number)
        logging.debug("Now working on submission "+str(loop_counter)+" of "+str(total_submissions_to_attempt)+", ID: "+str(submission_pointer)+" for range download mode" )
        # Try downloading each submission
        download_submission(settings, "RANGE_MODE", submission_pointer)
        print "\n\n"
        # Add/subtract from counter depending on mode
        if backwards:
            submission_pointer -= 1
        else:
            submission_pointer += 1
    # Clean up once everything is done
    clear_pointer_file(settings)
    return


def download_ids(settings,query_list,folder):
    # API for this is depricated!
    submission_ids = []
    for query in query_list:
        # remove invalid items
        if re.search("[^\d]",query):
            logging.debug("Not a submissionID! skipping.")
            continue
        else:
            submission_ids.append(query)
    download_submission_id_list(settings,submission_ids,folder)
    return


def process_query(settings,search_query):
    """Download submissions for a tag on derpibooru"""
    assert_is_string(search_query)
    #logging.info("Processing tag: "+search_query)
    # Run search for query
    submission_ids = search_for_query(settings, search_query)
    # Save data for resuming
    if len(submission_ids) > 0:
        save_resume_file(settings,search_query,submission_ids)
    # Download all found items
    download_submission_id_list(settings,submission_ids,search_query)
    # Clear temp data
    clear_resume_file(settings)
    return


def download_query_list(settings,query_list):
    counter = 0
    for search_query in query_list:
        counter += 1
        logging.info("Now proccessing query "+str(counter)+" of "+str(len(query_list))+": "+search_query)
        process_query(settings,search_query)
        append_list(search_query, settings.done_list_path)
    return


def convert_tag_string_to_search_string(settings,query):
    """Fix a tag string for use as a search query string"""
    colons_fixed = query.replace("-colon-",":")
    dashes_fixed = colons_fixed.replace("-dash-","-")
    dots_fixed = dashes_fixed.replace("-dot-",".")
    return dots_fixed

def convert_tag_list_to_search_string_list(settings,query_list):
    """Convert a whole list of queries to the new search format"""
    processed_queries = []
    for raw_query in query_list:
        processed_query = convert_tag_string_to_search_string(settings,raw_query)
        processed_queries.append(processed_query)
    return processed_queries


def convert_query_for_path(settings,query):
    """Convert a query to the old style -colon- format for filenames"""
    colons_fixed = query.replace(":", "-colon-")
    dashes_fixed = colons_fixed.replace("-", "-dash-")
    dots_fixed = dashes_fixed.replace(".", "-dot-")
    return dots_fixed


def main():
    # Load settings
    settings = config_handler("config\\derpibooru_dl_config.cfg")
    if len(settings.api_key) < 5:
        logging.warning("No API key set, weird things may happen.")
    # Load tag list
    raw_input_list = import_list(settings.input_list_path)
    # Fix input list
    input_list = convert_tag_list_to_search_string_list(settings,raw_input_list)
    #submission_list = import_list("config\\derpibooru_dl_submission_id_list.txt")
    # DEBUG
    #download_submission(settings,"DEBUG","263139")
    #print search_for_tag(settings,"test")
    #process_tag(settings,"test")
    #copy_over_if_duplicate(settings,"134533","download\\flitterpony")
    #a = read_pickle("debug\\locals.pickle")
    #print ""
    #return
    # /DEBUG
    # Handle resuming query download operations
    resumed_query = resume_downloads(settings)
    if resumed_query is not False:
        # Skip everything before and including resumed tag
        logging.info("Skipping all items before the resumed tag: "+resumed_query)
        #logging.debug(str(tag_list))
        input_list = input_list[( input_list.index(resumed_query) + 1 ):]
        #logging.debug(str(input_list))
    # Resume range operations
    resume_range_download(settings)
    # Begin new download operations
    # Ordered based on expected time to complete operations.
    # Download individual submissions
    if settings.download_submission_ids_list:
        download_ids(settings,input_list,"from_list")
    # Download last week mode (~7,000 items)
    if settings.download_last_week:
        download_this_weeks_submissions(settings)
    # Process each search query
    if settings.download_query_list:
        download_query_list(settings,input_list)
    # Download evrything mode
    if settings.sequentially_download_everything:
        download_everything(settings)
    return


if __name__ == '__main__':
    # Setup logging
    setup_logging("debug\\derpibooru_dl_log.txt")
    try:
        cj = cookielib.LWPCookieJar()
        setup_browser()
        main()
    except Exception, err:
        # Log exceptions
        logger.critical("Unhandled exception!")
        logger.critical(str( type(err) ) )
        logging.exception(err)
    logging.info( "Program finished.")
    #raw_input("Press return to close")
