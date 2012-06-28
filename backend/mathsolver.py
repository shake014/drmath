import ply.yacc as yacc
import consts
import lexer
import re
from sage.all import *

def incr_count(dic, key):
	if key in dic.keys():
		dic[key] += 1
	else:
		dic[key] = 1

class MathSolver():

	def __init__(self):
		self.tokens = consts.tokens
		self.var_c = {}
		precedence = (('left', '+', '-'),
		              ('left', '*', '/'),
			      ('left', '^'))

	def p_statement_expression(self, p):
		'statement : expression'
		p[0] = p[1]

	def p_expression_differentiate(self, p):
		'mathexpr : DIFFERENTIATE mathexpr'
		if p[1] == 'differentiate':
			p[0] = 'diff(' + p[2] + ',' + '@VAR@' + ').simplify()'
		else:
			p[0] = 'diff(' + p[2] + ',' + p[1][3] + ').simplify()'
			incr_count(self.var_c, p[1][3])

	def p_expression_integrate(self, p):
		'mathexpr : INTEGRATE mathexpr'
		p[0] = 'integrate(' + p[2] + ',' + '@VAR@' + ').simplify()'

	def p_expression_mathexpr(self, p):
		'expression : mathexpr'
		p[0] = p[1]

	def p_mathexpr_wrong_func(self, p):
		'mathexpr : FUNC'
		buf = ''
		for c in tuple(p[1]):
			buf += '*' + c
			incr_count(self.var_c, c)
		p[0] = buf[1:]

	def p_mathexpr_func(self, p):
		'mathexpr : FUNC LPAREN mathexpr RPAREN'
		if hasattr(sage.all, p[1]):
			p[0] = p[1] + p[2] + p[3] + p[4]
		else:
			buf = ''
			for c in tuple(p[1]):
				buf += c + '*'
				incr_count(self.var_c, c)
			p[0] = buf + p[2] + p[3] + p[4]


	def p_mathexpr_imult(self, p):
		'mathexpr : mathexpr mathexpr'
		p[0] = p[1] + '*' + p[2]

	def p_mathexpr_arith(self, p):
		'''mathexpr : LPAREN mathexpr RPAREN
		   mathexpr : mathexpr "*" mathexpr
		   mathexpr : mathexpr "/" mathexpr
		   mathexpr : mathexpr "+" mathexpr
		   mathexpr : mathexpr "-" mathexpr
		   mathexpr : mathexpr "^" mathexpr'''
		p[0] = p[1] + p[2] + p[3]

	def p_mathexpr_num(self, p):
		'mathexpr : NUM'
		p[0] = p[1]

	def p_mathexpr_var(self, p):
		'mathexpr : VAR'
		incr_count(self.var_c, p[1])
		p[0] = p[1]

#	# Error rule for syntax errors
#	def p_error(self, p):
#		print p
#		print "Syntax error in input!"

	def solve(self, data):
		lex = lexer.MathLexer()
		lex.build()
		lex.input(data)
		parser = yacc.yacc(module=self)
		result = parser.parse(lexer=lex.lexer)

		# Find out guess variable
		guessvar = None
		cerror = False
		for (v, count) in self.var_c.iteritems():
			if guessvar == None:
				guessvar = v
			if self.var_c[v] > self.var_c[guessvar]:
				cerror = False
				guessvar = v
			elif self.var_c[v] == self.var_c[guessvar]:
				cerror = True
		if guessvar == None:
			guessvar = 'x'
			incr_count(self.var_c, 'x')
		elif cerror:
			for v in ('x', 't', 'y', 'z'):
				if v in self.var_c:
					guessvar = v
					break
		result = re.sub('@VAR@', guessvar, result)

		s_vars = {}
		for _x_ in self.var_c.keys():
			s_vars[_x_] = sage.all.var(_x_)
		solution = sage_eval(result, locals=s_vars)
		return latex(solution)