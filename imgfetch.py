import urllib
import os.path

def portrait_filename( char_id ):

    filename = "imgs/%s.jpg" % char_id

    if os.path.isfile( filename ):
        return filename

    try:
        img = urllib.urlopen( "http://img.eve.is/serv.asp?s=64&c=%s" % char_id ).read()
    except IOError:
        return 'imgs/error.jpg'

    fp = open( filename, 'w' )
    fp.write( img )
    fp.close()
    return filename

print portrait_filename( '797400947' )
