literals = '-+*/^!'

reserved = { 'int'           : 'INTEGRATE',
             'integral'      : 'INTEGRATE',
			 'integrate'     : 'INTEGRATE',
			 'diff'          : 'DIFFERENTIATE',
			 'der'           : 'DIFFERENTIATE',
			 'differentiate' : 'DIFFERENTIATE',
			 'derivative'    : 'DIFFERENTIATE' }

tokens = ( 'NUM',
           'VAR',
           'FUNC',
		   'LPAREN',
		   'RPAREN' ) + tuple(set(reserved.values()))

sage_consts = ('pi',
               'e',
			   'NaN',
			   'golden_ratio',
			   'log2',
			   'euler_gamma',
			   'catalan',
			   'khinchin',
			   'twinprime',
			   'merten',
			   'mertens',
			   'glaisher',
			   'brun' )

ignores = ('of',)