#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# pylint: disable=I0011


"""
Action file for pywx.
    Ian Nesbitt <ian.nesbitt@gmail.com>
"""

from __future__ import print_function
import os
import os.path
import imghdr
import json
import argparse
from ftplib import FTP
from datetime import datetime
from PIL import Image
from PIL import ImageFont, ImageDraw
from subprocess import call, STDOUT
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'w')

# PARSER = argparse.ArgumentParser()
# PARSER.add_argument("-v", "--verbose", action="count", default=0,
#                    help="run in verbose mode")
# ARGS = PARSER.parse_args()

VERBOSE = 0
WARMUP_TIME = 4
OUTPUT_DIR = '/tmp/wx/'
IMAGE_NAME = 'image.jpg'
OUTPATH = os.path.join(OUTPUT_DIR, IMAGE_NAME)
BASEPATH = os.path.dirname(os.path.abspath(__file__))
JSONPATH = os.path.abspath(os.path.join(BASEPATH, "..", "settings.json"))
NOW = datetime.now()
YEAR = NOW.strftime('%Y')
NOW = NOW.strftime('%Y/%m/%d %H:%M:%S %Z')

def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])


if VERBOSE > 0:
    print('--------------------------------')
    print('(processor time): ' + NOW)
    print('--------------------------------')
    print('pywx image utility v0.0.1')
    print('(c) ' + YEAR + ' Ian Nesbitt')
    print('Mozilla Public License (MPL) 2.0')
    print('--------------------------------')

class ImageError(Exception):
    """An exception raised when file is not an appropriate image type."""
    def __init__(self, path): # pylint: disable=W0231
        self.path = path
    def __str__(self):
        return repr(self.path)
class PathError(Exception):
    """An exception raised when no image file exists here."""
    def __init__(self, path): # pylint: disable=W0231
        self.path = path
    def __str__(self):
        return repr(self.path)
class CredentialError(Exception):
    """An exception raised when no user credentials have been set."""
    def __init__(self, path): # pylint: disable=W0231
        self.path = path
    def __str__(self):
        return repr(self.path)

try:
    with open(JSONPATH) as j:
        DATA = json.load(j)
    DEVICE = DATA["device"]
except IOError as io_err:
    print("Could not find or could not open JSON at " + JSONPATH)
    raise PathError("You must have a JSON named settings.json in the top level directory.")


class Actions(object):
    """The actions class, where important things go on.
    """
    @staticmethod
    def take():
        """This function looks for the output directory and creats if necessary
        then calls imagesnap which takes a photo and saves it there."""
        if VERBOSE > 0:
            print('Looking for output directory ' + OUTPUT_DIR)
        # make sure the dir exists
        if not os.path.isdir(OUTPUT_DIR):
            if VERBOSE > 0:
                print(OUTPUT_DIR + ' does not exist. Attempting to create...')
            os.makedirs(OUTPUT_DIR)
            if VERBOSE > 0:
                print('Successfully created ' + OUTPUT_DIR)
        else:
            if VERBOSE > 0:
                print('Found ' + OUTPUT_DIR)
                print('imagesnap recording frame to ' + OUTPATH + ' using ' + DEVICE)
            pass
        # take a photo and put it in the output directory
        snap = call(['/opt/local/bin/imagesnap', '-w', str(WARMUP_TIME), '-q', '-d', DEVICE, OUTPATH],
                    stdout=DEVNULL, stderr=STDOUT)
        if VERBOSE > 0:
            print('Bash call errors: ' + str(snap))
            print('...done.')

    @staticmethod
    def check_file():
        """This function does some magic to make sure it's an image."""
        if VERBOSE > 0:
            print('Checking image recorded correctly...')
        # make sure image exists
        if not os.path.exists(OUTPATH):
            print('Cannot find ' + OUTPATH)
            raise PathError(OUTPATH)
        else:
            imgtype = imghdr.what(OUTPATH)
            if imgtype != 'jpeg':
                raise ImageError(OUTPATH)
            size = str(os.path.getsize(OUTPATH)/1024)
            if VERBOSE > 0:
                print('...found ' + size + 'kb ' + imgtype + ' at ' + OUTPATH)
        if size >= 150: # Wunderground only likes images under 150kb. Eventually may move to a loop
            if VERBOSE > 0:
                print('Image too large, attempting resize.')
            img = Image.open(OUTPATH)
            img.save(OUTPATH,optimize=True,quality=85)
            size = str(os.path.getsize(OUTPATH)/1024)
            if VERBOSE > 0:
                print('New size: ' + size + 'kb')

    @staticmethod
    def check_credentials():
        """This function checks the json for username and password."""
        if DATA["user"] == "username":
            raise CredentialError("You haven't set your credentials. Do so at: " + JSONPATH)
        else:
            if VERBOSE > 0:
                print("Found username " + DATA["user"] + ", proceeding to FTP.")
            pass

    @staticmethod
    def upload():
        """Here thar be FTP lads!"""
        if VERBOSE > 0:
            print('Upload sequence initiated. Connecting to Weather Underground...')
        wu_conn = FTP('webcam.wunderground.com')
        if VERBOSE > 0:
            print('Using login credentials for user: ' + DATA["user"])
        login = wu_conn.login(DATA["user"], DATA["pswd"])
        if login[0] == '2':
            if VERBOSE > 0:
                print('Login accepted. Uploading...')
            upl = wu_conn.storbinary('STOR image.jpg', open(OUTPATH, 'rb'))
            if upl[0] == '2':
                if VERBOSE > 0:
                    print('Upload success.')
                pass
            else:
                if VERBOSE > 0:
                    print('Upload failed.')
                pass
        elif login[0] == '5':
            if VERBOSE > 0:
                print('Login rejected. Adjust username and password.')
            pass
        else:
            if VERBOSE > 0:
                print('Status:' + login)
            pass
        if VERBOSE > 0:
            print('Exiting FTP connection.')
        wu_conn.quit()

    @staticmethod
    def all():
        """This function does it all."""
        err_name = ''
        success = False
        try:
            Actions.take()
            Actions.check_file()
            Actions.check_credentials()
        except PathError as err_name:
            print('There is no file at ' + err_name.path)
        except ImageError as err_name:
            print('The image at ' + err_name.path + ' is not jpeg.')
        except CredentialError as err_name:
            print('Weather Underground login credentials not set.')

        if err_name == '':
            try:
                Actions.upload()
                success = True
            except Exception as err_name: # pylint: disable=W0703
                print(err_name)
            finally:
                now = datetime.now()
                now = now.strftime('%Y/%m/%d %H:%M:%S %Z')
                if success:
                    size = GetHumanReadable(os.path.getsize(OUTPATH))
                    print(now + " - Success. Size: " + size)
                else:
                    print(now + " - Failure. Enable verbose mode for details.")

