import time
import tempfile
import cPickle
import zlib
import os
from os.path import join, exists

class cache_handler( object ):
    # adapted from http://home.wanadoo.nl/ntt/eve/library/files/api/apitest.py (does this satisfy the terms of the license?), will need work, but we need basic cache functionality... I feel guilty for abusing the server. FIXME --danny
    
    def __init__( self, debug = False ):
        self.debug = debug
        self.count = 0
        self.cache = {}
        self.tempdir = join( tempfile.gettempdir(), "eveapi" )
        if not exists( self.tempdir ):
            os.makedirs( self.tempdir )
            
    # remove this later --danny
    def log( self, what ):
        if self.debug:
            print "[%d] %s" % ( self.count, what )

    def retrieve( self, host, path, params ):
        # eveapi asks if we have this request cached
        key = hash( ( host, path, frozenset( params.items() ) ) )

        # for logging
        self.count += 1
        
        # see if we have the requested page cached...
        cached = self.cache.get( key, None )
        if cached:
            cacheFile = None
        else:
            # not in memory, maybe on disk --danny
            cacheFile = join( self.tempdir, str( key ) + ".cache" )
            if exists( cacheFile ):
                self.log( "%s: retreiving from disk." % path )
                f = open( cacheFile, "rb" )
                cached = self.cache[key] = cPickle.loads( zlib.decompress( f.read() ) )
                f.close()

        if cached:
            # check if the cached object is fresh enough
            if time.time() < cached[0]:
                self.log( "%s: returning cached document." % path )
                # return the cached object
                return cached[1]

                # if it's stale, purge it --danny
                self.log( "%s: cache expired, purging!" % path )
                del self.cache[key]
                if cacheFile:
                    os.remove( cacheFile )

            self.log( "%s: not cached, fetching from server..." % path )
            # We didn't get a cache hit so return None to indicate that the data should be requested from server
            return None
    
    def store( self, host, path, params, doc, obj ):
        # eveapi is asking us to cache an item
        key = hash( ( host, path, frozenset( params.items() ) ) )
        
        cachedFor = obj.cachedUntil - obj.currentTime
        if cachedFor:
            self.log( "%s: cached (%d seconds)." % ( path, cachedFor ) )
            
            cachedUntil = time.time() + cachedFor

            # store in memory
            cached = self.cache[key] = ( cachedUntil, obj )
            
            # store in cache folder
            cacheFile = join( self.tempdir, str( key ) + ".cache" )
            f = open( cacheFile, "wb" )
            f.write( zlib.compress( cPickle.dumps( cached, -1 ) ) )
            f.close


