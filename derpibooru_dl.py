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

# getwithinfo()
GET_REQUEST_DELAY = 2
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
    # End logging setup


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
    gettuple = getwithinfo(deescaped_url)
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
            logging.debug( "Attempt" + str(attemptcount) )
        try:
            r = br.open(url)
            info = r.info()
            reply = r.read()
            delay(GET_REQUEST_DELAY)
            # Save html responses for debugging
            #print info
            #print info["content-type"]
            if "html" in info["content-type"]:
                #print "saving debug html"
                save_file("debug\\get_last_html.htm", reply, True)
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
                save_file("debug\\error.htm", err.fp.read(), True)
        except urllib2.URLError, err:
            logging.debug(str(err))
            if "unknown url type:" in err.reason:
                return
        except httplib.BadStatusLine, err:
            logging.debug(str(err))
        delay(GET_RETRY_DELAY)


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



def delay(basetime,upperrandom=5):
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
                    strippedline = line[:-1]
                else:
                    strippedline = line#if no trailing newline exists, we dont need to strip it
                nameslist.append(strippedline)#add the username to the list
        listfile.close()
        return nameslist
    else:#if there is no list, make one
        listfile = open(listfilename, 'w')
        listfile.write('#add one tag per line, comments start with a #, nothing but tag on a lise that isnt a comment')
        listfile.close()
        return []


class config_handler():
    def __init__(self,settings_path="derpibooru_dl_config.cfg"):
        self.set_defaults()
        self.load_file(settings_path)
        self.save_settings(settings_path)

    def set_defaults(self):
        # Login
        self.api_key = ""
        # Download Settings
        self.reverse = False
        self.output_folder = "download"

    def load_file(self,settings_path):
        config = ConfigParser.RawConfigParser()
        if not os.path.exists(settings_path):
            return
        config.read(settings_path)
        # Login
        try:
            self.username = config.get('Login', 'api_key')
        except ConfigParser.NoOptionError:
            pass
        # Download Settings
        try:
            self.reverse = config.getboolean('Settings', 'Reverse')
        except ConfigParser.NoOptionError:
            pass
        try:
            self.username = config.get('Settings', 'output_folder')
        except ConfigParser.NoOptionError:
            pass

    def save_settings(self,settings_path):
        config = ConfigParser.RawConfigParser()
        config.add_section('Login')
        config.set('Login', 'api_key', self.api_key )
        config.add_section('Settings')
        config.set('Settings', 'Reverse', str(self.reverse) )
        config.set('Settings', 'output_folder', self.output_folder )
        with open(settings_path, 'wb') as configfile:
            config.write(configfile)


def assert_is_string(object_to_test):
    """Make sure input is either a string or a unicode string"""
    if( (type(object_to_test) == type("")) or (type(object_to_test) == type(u"")) ):
        return
    logging.critical(str(locals()))
    raise(ValueError)


def decode_json(json_string):
    """Wrapper for JSON decoding"""
    assert_is_string(json_string)
    return json.loads(json_string)


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
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def search_for_tag(settings,search_tag):
    """Perform search for a tag on derpibooru.
    Return a lost of found submission IDs"""
    assert_is_string(search_tag)
    logging.debug("Starting search for: "+search_tag)
    # Init counter
    page_counter = 1
    # Generate page URL
    # Load page
    # Extract submission_ids from page
    # Incriment page counter
    # Return found items


def download_submission(settings,search_tag,submission_id):
    """Download a submission from Derpibooru"""
    assert_is_string(search_tag)
    assert_is_string(submission_id)
    logging.debug("Downloading submission:"+submission_id)
    # Build JSON paths
    json_output_filename = submission_id+".json"
    json_output_path = os.path.join(settings.output_folder,search_tag,"json",json_output_filename)
    # Check if JSON exists
    if os.path.exists(json_output_path):
        logging.debug("JSON for this submission already exists, skipping.")
        return
    # Build JSON URL
    json_url = "https://derpibooru.org/"+submission_id+".json?"+settings.api_key
    # Load JSON URL
    json_page = get(json_url)
    if json_page is None:
        return
    # Convert JSON to dict
    json_dict = decode_json(json_page)
    # Extract needed info from JSON
    image_url = json_dict["image"]
    image_filename = json_dict["file_name"]
    image_file_ext = json_dict["original_format"]
    # Build image output filenames
    image_output_filename = image_filename+"."+image_file_ext
    image_output_path = os.path.join(settings.output_folder,search_tag,image_output_filename)
    # Load image data
    authenticated_image_url = image_url+"?"+settings.api_key
    image_data = get(authenticated_image_url)
    if image_data is None:
        return
    # Save image
    save_file(image_output_path, image_data, True)
    # Save JSON
    save_file(json_output_path, json_page, True)
    return


def process_tag(settings,search_tag):
    """Download submissions for a tag on derpibooru"""
    assert_is_string(search_tag)
    # Run search for tag
    submission_ids = search_for_tag(settings, search_tag)
    # Download all found items
    for submission_id in submission_ids:
        download_submission(settings, search_tag, submission_id)


def main():
    # Load settings
    settings = config_handler("config\\derpibooru_dl_config.cfg")
    # Load tag list
    tag_list = import_list("config\\derpibooru_dl_tag_list.txt")
    # DEBUG
    download_submission(settings,"DEBUG","44819")
    return
    # /DEBUG
    # Process each submission_id on tag list
    for search_tag in tag_list:
        logging.info("Now starting tag:"+search_tag)
        process_tag(settings, search_tag)

if __name__ == '__main__':
    # Setup logging
    setup_logging("debug\\derpibooru_dl_log.txt")
    try:

        cj = cookielib.LWPCookieJar()
        setup_browser()
        main()
    except Exception, e:
        # Log exceptions
        logger.critical("Unhandled exception!")
        logging.exception(e)
    logging.info( "Program finished.")
    #raw_input("Press return to close")
