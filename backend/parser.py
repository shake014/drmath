import ply.yacc as yacc
import consts
import lexer
import re

# TODO: We _DO_ need to worry about math op's here, remove use of PsuedoLexer

tokens = consts.tokens
literals = consts.literals
data = '''int diff 4x-4sin(cos(x))ab'''
var_c = {}

precedence = ( ('left', '+', '-'),
	           ('left', '*', '/') )

def incr_count(dic, key):
	if key in dic.keys():
		dic[key] += 1
	else:
		dic[key] = 1

def p_statement_expression(p):
	'statement : expression'
	p[0] = p[1]

def p_expression_differentiate(p):
	'expression : DIFFERENTIATE expression'
	if p[1] == 'differentiate':
		p[0] = 'diff(' + p[2] + ',' + '@VAR@' + ')'
	else:
		p[0] = 'diff(' + p[2] + ',' + p[1][3] + ')'

def p_expression_integrate(p):
	'expression : INTEGRATE expression'
	p[0] = 'integrate(' + p[2] + ',' + '@VAR@' + ')'

def p_expression_mathexpr(p):
	'expression : mathexpr'
	p[0] = p[1]


def p_mathexpr_wrong_func(p):
	'mathexpr : FUNC'
	buf = ''
	for c in tuple(p[1]):
		buf += '*' + c
		incr_count(var_c, c)
	p[0] = buf[1:]

def p_mathexpr_func(p):
	'mathexpr : FUNC LPAREN mathexpr RPAREN'
	p[0] = p[1] + p[2] + p[3] + p[4]


def p_mathexpr_imult(p):
	'mathexpr : mathexpr mathexpr'
	p[0] = p[1] + '*' + p[2]

def p_mathexpr_arith(p):
	'''mathexpr : LPAREN mathexpr RPAREN
	   mathexpr : mathexpr "*" mathexpr
	   mathexpr : mathexpr "/" mathexpr
	   mathexpr : mathexpr "+" mathexpr
	   mathexpr : mathexpr "-" mathexpr'''
	p[0] = p[1] + p[2] + p[3]

def p_mathexpr_num(p):
	'mathexpr : NUM'
	p[0] = p[1]

def p_mathexpr_var(p):
	'mathexpr : VAR'
	incr_count(var_c, p[1])
	p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
	print p
	print "Syntax error in input!"

lex = lexer.MathLexer()
lex.build()
lex.input(data)
parser = yacc.yacc()
result = parser.parse(lexer=lex.lexer)

# Find out guess variable
guessvar = None
cerror = False
for (var, count) in var_c.iteritems():
	if guessvar == None:
		guessvar = var
	if var_c[var] > var_c[guessvar]:
		cerror = False
		guessvar = var
	elif var_c[var] == var_c[guessvar]:
		cerror = True
if guessvar == None:
	guessvar = 'x'
elif cerror:
	for var in ('x', 't', 'y', 'z'):
		if var in var_c:
			guessvar = var
			break
result = re.sub('@VAR@', guessvar, result)

print result