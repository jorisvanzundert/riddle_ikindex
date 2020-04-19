import regex

sn_regex = regex.compile( r'\d\.\d+e-\d+$' )
idxs = []
idxs_num = []
with open( 'results/ik-ml-1001_20200128_1304.txt', 'r' ) as ml_file:
    idxs = ml_file.read().splitlines()
for idx in idxs[1:]:
    sn = sn_regex.search( idx )
    num = float( sn.group(0) )
    idx = sn_regex.sub( '{:08.7f}'.format( num ), idx )
    idxs_num.append( ( idx, num ) )
idxs_extended = list( zip( idxs_num, sorted( idxs_num, key=lambda idx_num: idx_num[1], reverse=True ) ) )
with open( 'results/ik-ml-1001_20200128_1304_decnot_sortalpha.txt', 'w' ) as ml_file:
    ml_file.write( '{}\n'.format( idxs[0] )  )
    for idx_num in idxs_extended:
        print( 'hi' )
        ml_file.write( '{}\n'.format( idx_num[0][0] ) )
with open( 'results/ik-ml-1001_20200128_1304_decnot_sortidx.txt', 'w' ) as ml_file:
    ml_file.write( '{}\n'.format( idxs[0] )  )
    print( len(idxs_extended))
    for idx_num in idxs_extended:
        print( 'ho' )
        ml_file.write( '{}\n'.format( idx_num[1][0] ) )
with open( 'results/ik-ml-1001_20200128_1304_decnot_parallel.txt', 'w' ) as ml_file:
    ml_file.write( '{}                    {}\n'.format( idxs[0], idxs[0] )  )
    for idx_num in idxs_extended:
        ml_file.write( '{}                       {}\n'.format( idx_num[0][0], idx_num[1][0] ) )
