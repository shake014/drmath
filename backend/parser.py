import ply.yacc as yacc
import consts
import lexer

# TODO: We _DO_ need to worry about math op's here, remove use of PsuedoLexer

tokens = tuple(set(consts.reserved.values())) + (consts.mathexpr,)
data = '''int int diff 6(3t + 5sin[t^2]) + 2 cos(t)'''

def p_statement_expr_math_expr(p):
	'statement : expression term expression'
	p[0] = p[1] + p[2] + p[3]

def p_statement_expression(p):
	'statement : expression'
	p[0] = p[1]

def p_expression_differentiate(p):
	'expression : DIFFERENTIATE expression'
	if p[1] == 'differentiate':
		p[1] = 'd/d' + lex.var
	p[0] = 'diff(' + p[2] + ',' + p[1][3] + ')'

def p_expression_integrate(p):
	'expression : INTEGRATE expression'
	p[0] = 'integrate(' + p[2] + ',' + lex.var + ')'

def p_expression_term(p):
	'expression : term'
	p[0] = p[1]

def p_term_num(p):
	'term : MATHEXPR'
	p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
	print "Syntax error in input!"

lex = lexer.PsuedoLexer()
lex.input(data)
parser = yacc.yacc()
result = parser.parse(lexer=lex)
print result