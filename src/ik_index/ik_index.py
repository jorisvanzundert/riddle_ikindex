import glob
import re
from tqdm import tqdm
import pandas

def parse_name( name ):
    author_title_shortened = name.split( "/" )[-1].split( "." )[0]
    perspective = author_title_shortened[:7]
    return { 'author_title_shortened': author_title_shortened, 'perspective': perspective }

def ik_index( path_to_texts, index_meta ):
    file_names = sorted( glob.glob( "{}/*.txt".format( path_to_texts ) ) )
    results = {}
    for file_name in tqdm( file_names ):
        with open( file_name, "r" ) as txt_file:
            text = txt_file.read().lower()
            # merely a rough indication of text length (number of spaces found)
            n = len( re.findall( r'[ ]+', text ) )
            enumerator = 0
            for word_form in index_meta[ 'enumerator' ]:
                enumerator += len( re.findall( r'\b{}\b'.format( word_form ), text ) )
            denominator = 1
            for word_form in index_meta[ 'denominator' ]:
                denominator += len( re.findall( r'\b{}\b'.format( word_form ), text ) )
            meta_info = parse_name( file_name )
            results[ meta_info[ 'author_title_shortened' ] ] = [ meta_info[ 'perspective' ], ( enumerator / ( 1 + denominator ) ), n ]
    data_frame = pandas.DataFrame.from_dict( results, orient="index", columns=[ 'perspective', 'ik-index', 'token_count' ] )
    data_frame = data_frame.sort_values( by=[ 'ik-index' ], ascending=False )
    enumerator_latex_index = ''
    for word_form in index_meta[ 'enumerator' ]:
        enumerator_latex_index += '{}, '.format( word_form )
    denominator_latex_index = ''
    for word_form in index_meta[ 'denominator' ]:
        denominator_latex_index += '{}, '.format( word_form )
    equation_latex = r'$\frac{{n_{{({})}}}}{{1 + n_{{({})}}}}$'.format( enumerator_latex_index[:-2], denominator_latex_index[:-2] )
    return ( data_frame, equation_latex )
