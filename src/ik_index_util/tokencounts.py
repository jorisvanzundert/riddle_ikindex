import os
import glob
import regex
import statistics

PATH_TO_DATA = os.path.join( 'data', 'undisclosed', 'AD_ZD' )
PATH_TO_1001 = os.path.join( PATH_TO_DATA, '1001'  )

def clean( text ):
    return regex.sub( r'\d+|[\'"“”‘’\-–—.,!?]', '', text ).lower()

def shortname( file_path ):
    return os.path.basename( file_path ).split( '.' )[0]

def get_text( file_path ):
    with open( file_path, "r" ) as text_file:
        return clean( text_file.read() )

first_person_file_paths = sorted( glob.glob( "{}/1E PERS*.txt".format( PATH_TO_1001 ) ) )
third_person_file_paths = sorted( glob.glob( "{}/3E PERS*.txt".format( PATH_TO_1001 ) ) )

all_file_paths = first_person_file_paths + third_person_file_paths

space_regex = regex.compile( r'[ ]+' )
counts = []
for idx, file_path in enumerate( all_file_paths ):
    text = clean( get_text( file_path ) )
    text_length = len( space_regex.findall( text ) )
    counts.append( text_length )
    print( text_length, file_path )
    print( clean( text ) )
    print( '-------' )
print( min( counts ) )
print( max( counts ) )
print( statistics.mean( counts ) )
print( statistics.stdev( counts ) )
