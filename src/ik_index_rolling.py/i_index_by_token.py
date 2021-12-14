import regex
import matplotlib.pyplot as pyplot
import seaborn
from datetime import datetime

seaborn.set()

index_meta = {
    'enumerator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze' ],
    'denominator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze', 'hij', 'zij', 'ze', 'je', 'jou[w]', 'haar', 'zijn', 'jullie' ]
}

def label_line( line ):
    if line.startswith( '{s}' ):
        return ( 'S', line[3:] )
    else:
        return ( 'N', line )

def clean_line( line ):
    line = regex.sub( r'\d+|[\'"“”‘’\-–—.,!?]', ' ', line ).lower()
    return regex.sub( r'\s+', ' ', line ).strip()

def i_index_line( label, line ):
    enumerator = 0
    for word_form in index_meta[ 'enumerator' ]:
        enumerator += len( regex.findall( r'\b{}\b'.format( word_form ), line ) )
    denominator = 1
    for word_form in index_meta[ 'denominator' ]:
        denominator += len( regex.findall( r'\b{}\b'.format( word_form ), line ) )
    return ( ( enumerator / denominator ), label, line )

file_name = 'data/undisclosed/lmtd/full_txt/Abdolah_Koning 2.txt'
with open( file_name, "r" ) as txt_file:
    text = txt_file.read().lower()

lines = text.split( '\n' )
# isolate anything between single quotes as direct speech
labeled_lines = []
# for line in lines[100:200]:
for line in lines:
    labeled_lines += regex.sub( r'\'(.*?)\'', '\'{S}\\1\'', line ).split( '\'' )
# The split on lines that start with an ' causes blank lines, we'll remove them.
labeled_lines = list( filter( lambda line: len( line ) > 0, labeled_lines ) )
# We're not interested in punctuation for now, and we clean up leading and trailing space.
labeled_lines = list( map( clean_line, labeled_lines ) )
# Lastly map all lines to a list of tuples [ ( label, line ) ]
labeled_lines = list( map( label_line, labeled_lines ) )

# now we need to move from lines to tokens while we retain the information
# of whether the token belongs to speech or not.
# labeled_lines = { k,v for label, tuple in labeled_lines ) )
labeled_tokens = []
for ( label, tokens ) in labeled_lines:
    for token in tokens.split( ' ' ):
        labeled_tokens.append( (label, token ) )


window = labeled_tokens[0:200]
i_index_rolling = []
for token in labeled_tokens[200:]:
    # TODO: we might do someting interesting with the label. It's now just
    # the S (speech) or N (non speech) value. We could do some averaging. Not
    # sure that would serve purpose though.
    i_index = i_index_line( window[0][0], ' '.join( [ token[1] for token in window ] ) )
    i_index_rolling.append( ( i_index[0], int( i_index[1]=='N' ) ) )
    window.append( token )
    window.pop( 0 )

print( i_index_rolling )

# with open( './results/irolling/roll_i_tokens_{}.csv'.format( datetime.now().strftime( "%Y%m%d_%H%M" ) ), 'w' ) as csv_file:
#     for i_index_tuple in labeled_lines:
#         csv_file.write( ','.join( [ '"{}"'.format( str( item ) ) for item in i_index_tuple] ) )
#

x = range( 0, len( i_index_rolling ) )
y = [ i_index[0] for i_index in i_index_rolling ]
fig = pyplot.figure( figsize=(10,3))
ax = pyplot.subplot(111)
ax.plot( x, y, linestyle='solid' )
pyplot.show()
