literals = '-+*/^!'

reserved = { 'int'           : 'INTEGRATE',
             'integral'      : 'INTEGRATE',
			 'integrate'     : 'INTEGRATE',
			 'diff'          : 'DIFFERENTIATE',
			 'der'           : 'DIFFERENTIATE',
			 'differentiate' : 'DIFFERENTIATE',
			 'derivative'    : 'DIFFERENTIATE' }

tokens = ( 'NUM',
           'ID',
		   'LPAREN',
		   'RPAREN' ) + tuple(set(reserved.values()))

mathexpr = 'MATHEXPR'

sage_consts = ('pi',
               'e',
			   'NaN',
			   'golden_ratio',
			   'log2',
			   'euler_gamma',
			   'twinprime',
			   'mertens',
			   'brun' )

ignores = ('of',)