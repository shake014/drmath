import ply.yacc as yacc
import consts
import lexer
import re
from sage.all import *

tokens = consts.tokens
data = '''int diff 4x-4sin(cos(x))ab(4+2)'''
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
		incr_count(var_c, p[1][3])

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
	if hasattr(sage.all, p[1]):
		p[0] = p[1] + p[2] + p[3] + p[4]
	else:
		buf = ''
		for c in tuple(p[1]):
			buf += c + '*'
			incr_count(var_c, c)
		p[0] = buf + p[2] + p[3] + p[4]


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
for (v, count) in var_c.iteritems():
	if guessvar == None:
		guessvar = v
	if var_c[v] > var_c[guessvar]:
		cerror = False
		guessvar = v
	elif var_c[v] == var_c[guessvar]:
		cerror = True
if guessvar == None:
	guessvar = 'x'
elif cerror:
	for v in ('x', 't', 'y', 'z'):
		if v in var_c:
			guessvar = v
			break
result = re.sub('@VAR@', guessvar, result)

s_vars = {}
for _x_ in var_c.keys():
	s_vars[_x_] = sage.all.var(_x_)
print sage_eval(result, locals=s_vars)