import urllib
import os.path

def portrait_filename( char_id, img_size ):

    err_img = '/opt/mEveMon/imgs/error.jpg'

    # we can only accept 64 or 256... I know an exclamation point is not an error message, but I'll come back to this. FIXME --danny
    if not ( img_size == 64 or img_size == 256 ):
        return err_img

    # if asked for the large version, save it under a diff name --danny
    if img_size == 64:
        filename = "/opt/mEveMon/imgs/%s.jpg" % char_id
    elif img_size == 256:
        filename = "/opt/mEveMon/imgs/%s_lg.jpg" % char_id

    if os.path.isfile( filename ):
        return filename

    # specify size and cid --danny
    img_url = "http://img.eve.is/serv.asp?s=%s&c=%s" % ( str( img_size ), char_id )

    # fetch it, and hit the road. --danny
    try:
        urllib.urlretrieve( img_url, filename, report_handler )
    except urllib.ContentTooShortError:
        filename = err_img
    return filename

def report_handler( *a ):
    ( blocks_transferred, block_size, total_size ) = a
