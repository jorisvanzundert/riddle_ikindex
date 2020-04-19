import regex

index_meta = {
    'enumerator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze' ],
    'denominator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze', 'hij', 'zij', 'ze', 'je', 'jou[w]', 'haar', 'zijn', 'jullie' ]
}

def label_line( line ):
    if line.startswith( '{S}' ):
        return ( 'S', line[3:] )
    else:
        return ( 'N', line )

def i_index_line( label, line ):
    enumerator = 0
    for word_form in index_meta[ 'enumerator' ]:
        enumerator += len( regex.findall( r'\b{}\b'.format( word_form ), line ) )
    denominator = 1
    for word_form in index_meta[ 'denominator' ]:
        denominator += len( regex.findall( r'\b{}\b'.format( word_form ), line ) )
    return ( ( enumerator / denominator ), label, line )

file_name = 'data/undisclosed/txts/Abdolah_Koning.txt'
with open( file_name, "r" ) as txt_file:
    text = txt_file.read().lower()
    lines = text.split( '\n' )
    # isolate anything between single quotes as direct speech
    labeled_lines = []
    for line in lines[100:200]:
        labeled_lines += regex.sub( r'\'(.*?)\'', '\'{S}\\1\'', line ).split( '\'' )
    # The split on lines that start with an ' causes blank lines, we'll remove them.
    labeled_lines = list( filter( lambda line: len( line ) > 0, labeled_lines ) )
    # We're not interested in punctuation for now, and we clean up leading and trailing space.
    labeled_lines = list( map( lambda line: regex.sub( r'[.,?!;:\'"“”‘’]', '', line ).strip(), labeled_lines ) )
    # Lastly map all lines to a list of tuples [ ( label, line ) ]
    labeled_lines = list( map( label_line, labeled_lines ) )

    # let's compute i index for each line
    labeled_lines = [ i_index_line( *tuple ) for tuple in labeled_lines ]

    for line in labeled_lines:
        print( line )
