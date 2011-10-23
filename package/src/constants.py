""" Contains all the constants that mevemon uses """
import os
import tempfile

CONFIG_DIR = os.path.expanduser("~/.mevemon/")
CONFIG_NAME = "mevemon.cfg"
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_NAME)
IMG_CACHE_PATH = os.path.join(CONFIG_DIR, "imgs")
APICACHE_PATH = os.path.join(tempfile.gettempdir(), "eveapi")

# Logging constants
LOGNAME = "mevemon.log"
LOGPATH = os.path.join(CONFIG_DIR, LOGNAME)
MAXBYTES = 1 * 1000 * 1000 # 1MB
LOGCOUNT = 10

ABOUT_NAME = 'mEveMon'
ABOUT_TEXT = ('Mobile character monitor for EVE Online')
ABOUT_AUTHORS = ['Ryan Campbell <campbellr@gmail.com>',
                 'Danny Campbell <danny.campbell@gmail.com>']

ABOUT_WEBSITE = 'http://mevemon.garage.maemo.org'
APP_VERSION = '0.5-2'

# size of a valid verification code
MIN_VER_CODE_SIZE = 20
MAX_VER_CODE_SIZE = 64

# the access mask we need to perform mevemon's functions (we may want
# this to be a _minimum_ access, but I'd have to take a closer look at
# how the masks work - FIXME, danny)

REQUIRED_ACCESS_MASK = 131081
