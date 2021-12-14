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

# let's compute i index for each line
labeled_lines = [ i_index_line( *tuple ) for tuple in labeled_lines ]

for i_index_tuple in labeled_lines:
    # csv_file.write( ','.join( *i_index_tuple ) )
    print(  )

with open( './results/irolling/roll_i_lines_{}.csv'.format( datetime.now().strftime( "%Y%m%d_%H%M" ) ), 'w' ) as csv_file:
    for i_index_tuple in labeled_lines:
        csv_file.write( ','.join( [ '"{}"'.format( str( item ) ) for item in i_index_tuple] ) )
        csv_file.write( '\n' )

# i, s = list( zip( *labeled_lines ) )[0:2]
# s = list( map( lambda x: 0.2 if x=='S' else -0.2, s ) )
# x = range( 0, len(i) )
# fig = pyplot.figure( figsize=(10,3))
# ax = pyplot.subplot(111)
# ax.bar( x, i, width=0.8, color='g', alpha=0.9 )
# ax.bar( x, s, width=0.8, color='r', alpha=0.5 )
# pyplot.show()
