#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      new
#
# Created:     25/06/2014
# Copyright:   (c) new 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from derpibooru_dl import *


def main():
    # Load settings
    settings = config_handler("config\\derpibooru_dl_config.cfg")
    verify_folder(settings, settings.output_folder)

if __name__ == '__main__':
    # Setup logging
    setup_logging("debug\\derpibooru_verify_log.txt")
    try:
        #cj = cookielib.LWPCookieJar()
        #setup_browser()
        main()
    except Exception, err:
        # Log exceptions
        logger.critical("Unhandled exception!")
        logger.critical(str( type(err) ) )
        logging.exception(err)
    logging.info( "Program finished.")
    #raw_input("Press return to close")
