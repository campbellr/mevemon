import urllib
import os.path

def portrait_filename( char_id, img_size ):

    err_img = 'imgs/error.jpg'

    # we can only accept 64 or 256... I know an exclamation point is not an error message, but I'll come back to this. FIXME --danny
    if not ( img_size == 64 or img_size == 256 ):
        return err_img

    # if asked for the large version, save it under a diff name --danny
    if img_size == 64:
        filename = "imgs/%s.jpg" % char_id
    elif img_size == 256:
        filename = "imgs/%s_lg.jpg" % char_id

    if os.path.isfile( filename ):
        return filename

    # specify size and cid --danny
    try:
        img_url = "http://img.eve.is/serv.asp?s=%s&c=%s" % ( str( img_size ), char_id )
        img = urllib.urlopen( img_url ).read()
    except IOError:
        return err_img

    # write it, and hit the road. --danny

    fp = open( filename, 'w' )
    fp.write( img )
    fp.close()
    return filename
