# seb - 03.08.2013
import os
import logging

# TODO:
# Define: What is a log?
#           - Is it a file?
#           - Is it readable?
#           - does it exist?
#           - can we open it? if not, fail and let the user know.
#           - log everything we do, can be here or in the engine file.

# Class to define what a log is.
class ALog(object):

    def __init__(self, logfile):
        self.logfile_nonparsed = logfile # Path to CXS log.
        self.logfile_parsed = 'cxsparser.log' # Record every action on this file.
        # Empty list to store the files we are going to 
        # delete after the log is parsed.
        self.files2delete = []
        ### Logging config below.
        logging.basicConfig(
            filename = self.logfile_parsed,
            level = logging.DEBUG,
            format = '%(asctime)s %(message)s',
            datefmt = '%m/%d/%Y %I:%M:%S'
            )

    def filter_log(self):
        """Parse CXS log and create a new one filtering stuff we don't need """

        log2parse = open(self.logfile_nonparsed, 'r')
        
        for l in log2parse:
            lf = l.split()[5].strip('\'[]')
            if "virus" in l or "exploit" in l:
                logging.info('FOUND: %s' % lf)
                self.files2delete.append(lf)
            
            else:
                logging.info('IGNORED: %s' % lf)
        
        log2parse.close()

        return self.files2delete

    def process_list(self, files2del):
        """Delete the files on the list returned by the filter_log() function"""

        # Iterate the list of files that are going to be deleted.
        for item in files2del:
            # Delete files only if those are regular or symlinks.
            if os.path.isfile(item) or os.path.islink(item):
                logging.info('DELETED: %s' % item)
                os.unlink(item)

            # Skip directories and other non regular files.
            else:
                logging.info('SKIPPED: %s' % item)
        
