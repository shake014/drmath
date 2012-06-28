
#  Copyright (c) 2012 Muhammed Uluyol
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.

import ply.lex as lex
import consts
import sage.all

class MathLexer:

	def __init__(self):
		self.tokens = consts.tokens
		self.literals = consts.literals
		self.lexer = None

	t_NUM = r'\d+'

	# TODO: Switch derivatives found in t_FUNC into d/d* form
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
	# Reserved keywords have to be identified
	def t_FUNC(self, t):
		r'([_A-Za-z])+'
		t.value = str.lower(t.value)
		if t.value in consts.ignores:
			return
		elif t.value in consts.sage_consts:
			t.type = 'NUM'
		elif len(t.value) == 1 and t.value != '_':
			t.type = 'VAR'
		else:
			t.type = consts.reserved.get(t.value,'FUNC')
			if t.type != 'FUNC':
				t.value = str.lower(t.type)
		return t

	t_ignore  = ' \t'

	def t_error(self, t):
#		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

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

		return toks