import ply.lex as lex
import re
import consts

# FIXME: PsuedoLexer is ugly and B.I.G.
# FIXME: PsuedoLexer seems useless, we can deal with
#        things in the parser, QUIT BEING SO SMART _HERE_

def is_mult(a, b):
	if (a.type == 'NUM'    and b.type == 'LPAREN') or \
	   (a.type == 'RPAREN' and b.type == 'NUM')    or \
	   (a.type == 'NUM'    and b.type == 'ID')     or \
	   (a.type == 'RPAREN' and b.type == 'ID')     or \
	   (a.type == 'NUM'    and b.type == 'NUM'):
		return True
	return False

class MathLexer:

	def __init__(self):
		self.tokens = consts.tokens
		self.literals = consts.literals

	t_NUM = r'\d+'

	# TODO: Switch derivatives found in t_ID into d/d* form
	# This is done in the parser. This needs to be put together properly
	def t_DIFFERENTIATE(self, t):
		r'd/d([A-Za-z])'
		if len(t.value) == 4:
			return t
		else:
			# No idea what to do
			return

	def t_LPAREN(self, t):
		r'\(|\['
		t.value = '('
		return t

	def t_RPAREN(self, t):
		r'\)|\]'
		t.value = ')'
		return t

	# Almost everything comes here
	# We throw away ignore's
	# We need to separate consts/vars, which we treat as NUMBERs
	# Reserved keywords have to be identified and turned proper (eg int -> integrate)
	def t_ID(self, t):
		r'([_A-Za-z])+'
		t.value = str.lower(t.value)
		if t.value in consts.ignores:
			return
		elif t.value in consts.sage_consts or (len(t.value) == 1 and t.value != '_'):
			t.type = 'NUM'
		else:
			t.type = consts.reserved.get(t.value,'ID')
			if t.type != 'ID':
				t.value = str.lower(t.type)
		return t

	t_ignore  = ' \t'

	def t_error(self, t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	def build(self, **kwargs):
		self.lexer = lex.lex(object=self, **kwargs)

	def input(self, data):
		self.lexer.input(data)

	def toks(self):
		toks = []
		multtok = lex.LexToken()
		multtok.type = '*'
		multtok.value = '*'
		multtok.lineno = 0
		multtok.lexpos = 0
		while True:
			tok = self.lexer.token()
			if not tok: break
			toks.append(tok)

		# Make implied *'s explicit
		i = 1
		while True:
			if not i < len(toks):
				break
			if is_mult(toks[i-1], toks[i]):
				toks.insert(i, multtok)
				i += 1
			i += 1

		return toks

class PsuedoLexer:

	def __init__(self):
		self.tokens = tuple(set(consts.reserved.values())) + (consts.mathexpr,)
		self.index = 0
		self.toks = None
		self.var = None
		self.var_c = {}

	def input(self, data):
		mathlex = MathLexer()
		mathlex.build()
		mathlex.input(data)
		mathtoks = mathlex.toks()
		self.toks = []
		buf = lex.LexToken()
		buf.type = consts.mathexpr
		buf.value = ''
		buf.lineno = 0
		buf.lexpos = 0
		for mathtok in mathtoks:
			if mathtok.type in self.tokens:
				if buf.value != '':
					self.toks.append(buf)
					buf = lex.LexToken()
					buf.type = consts.mathexpr
					buf.value = ''
					buf.lineno = 0
					buf.lexpos = 0
				self.toks.append(mathtok)
			else:
				if (len(mathtok.value) == 1) and \
				   (re.match('[A-Za-z]', mathtok.value) != None):
					if mathtok.value in self.var_c.keys():
						self.var_c[mathtok.value] += 1
					else:
						self.var_c[mathtok.value] = 1
				buf.value += mathtok.value
		if buf.value != '':
			self.toks.append(buf)
		for (var, count) in self.var_c.iteritems():
			if self.var == None:
				self.var = var
			if self.var_c[var] > self.var_c[self.var]:
				self.var = var
		if self.var == None:
			self.var = 'x'

	def token(self):
		if self.index < len(self.toks):
			self.index += 1
			return self.toks[self.index-1]
