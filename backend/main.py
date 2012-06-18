import consts
import lexer

data = '''d/dx integral of x[3x + 4] * 20x^2 (-30) 2 sin(3PI/2)'''

lex = lexer.MathLexer()
lex.build()
lex.input(data)
fstr = ''
toks = lex.toks()
for i in range(len(toks)):
	print toks[i]
	if toks[i].type in consts.reserved.values():
		fstr += toks[i].value + ' '
	else:
		fstr += toks[i].value
print fstr
