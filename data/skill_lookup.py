# skill_lookup.py: initialize it with the typeID from the XML file, and it will fetch the information we need that we can't find in the API, from the SQLite skills database I made. --danny

import sqlite3

class db_skill():
    
    def __init__( self, type_id ):

        # open the custom skill dump from cur dir. --danny
        conn = sqlite3.connect( './invTypes.sqlite' )
        c = conn.cursor()
        
        # create a tuple out of the typeID --danny
        t = ( type_id, )
        c.execute( 'SELECT typeName, description, graphicID FROM invTypes WHERE typeID = ?', t )
        # break up the tuple returned --danny
        ( self.sk_name, self.sk_desc, self.sk_graphic_id ) = c.fetchone()
        c.close()

    # ( I don't even know if this how you should do this sort of thing, just playing around with classes.) --danny

    def get_name( self ):
        return self.sk_name

    def get_desc( self ):
        return self.sk_desc
