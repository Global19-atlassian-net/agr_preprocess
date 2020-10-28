import logging
import os
import time
import urllib.request
from common import ContextInfo

logger = logging.getLogger(__name__)


class S3File(object):

    def __init__(self, filename, savepath):
        self.filename = filename
        self.savepath = savepath

        self.context_info = ContextInfo()

    def download(self):
        if not os.path.exists(os.path.dirname(os.path.join(self.savepath, self.filename))):
            logger.info("Making temp file storage: %s" % (self.savepath))
            os.makedirs(os.path.dirname(os.path.join(self.savepath, self.filename)))

        url = self.download_url
        logger.info(url)
        if not os.path.exists(os.path.join(self.savepath, self.filename)):
            urllib.request.urlretrieve(url, os.path.join(self.savepath, self.filename))
        else:
            logger.info("File: %s/%s already exists, not downloading" % (self.savepath, self.filename))
        return os.path.join(self.savepath, self.filename)

    def download_new(self):
        if not os.path.exists(os.path.dirname(os.path.join(self.savepath, self.filename))):
            logger.debug("Making temp file storage: %s" % (os.path.dirname(os.path.join(self.savepath, self.filename))))

            # Our little retry loop. Implemented due to speed-related writing errors.
            # TODO Replace / update with "tenacity" module.
            attempts = 0
            while attempts < 3:
                try: 
                    os.makedirs(os.path.dirname(os.path.join(self.savepath, self.filename)))
                    break
                except FileExistsError:
                    # Occassionally, two processes can attempt to create the directory at almost the exact same time.
                    # This allows except should allow this condition to pass without issue.
                    break
                except OSError as e:
                    logger.warn('OSError encountered when creating directories.')
                    logger.warn('Sleeping for 2 seconds and trying again.')
                    logger.warn(e)
                    attempts += 1
                    time.sleep(2)
            if attempts == 3:
                raise OSError('Critical error downloading file (attempted 3 times): %s + "/" + %s' % (self.savepath, self.filename))

        url = self.download_url
        logger.info("downloading %s into savepath %s" % (url, os.path.dirname(os.path.join(self.savepath, self.filename))))
        if not os.path.exists(os.path.join(self.savepath, self.filename)):
            urllib.request.urlretrieve(url, os.path.join(self.savepath, self.filename))
            return False
        else:
            logger.debug("File: %s/%s already exists, not downloading" % (self.savepath, self.filename))
            return True

    def list_files(self):
        pass
