# lexical analysis
# https://docs.python.org/3/reference/lexical_analysis.html
# TODO:
#	https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals


#########################
# Test indentation and \
# line breaks

def test_indentation(a):
		# and line breaks
	if a \
\
			and True:
		print('te\
\'st')
	else:
	 print('else')

test_indentation(1)
# te'st
test_indentation(0)
# else

#########################
# Class private names

class A():
	@staticmethod
	def __a():
		return 1
	def __b(self):
		return self.__a()

A()._A__b()
# 1

#########################
# String literals

raw_newline = r'\n\
'
newline = '\\n\\\n\
'
raw_newline_longstring = r'''\n\
'''
newline_longstring = '''\\n\\
'''

print(RF'\nñ{raw_newline}ñ')
# \nñ\n\
# ñ
assert RF'\nñ{raw_newline}ñ' \
	== RF'\nñ{newline}ñ' \
	== RF'\nñ{raw_newline_longstring}ñ' \
	== RF'\nñ{newline_longstring}ñ'

print(F'\nñ{raw_newline}ñ')
# 
# ñ\n\
# ñ
assert F'\nñ{raw_newline}ñ' \
	== F'\nñ{newline}ñ' \
	== F'\nñ{raw_newline_longstring}ñ' \
	== F'\nñ{newline_longstring}ñ'

#########################
# Bytes literals

raw_bytestring = br'\r\
a'
bytestring = b'\\r\\\n\
a'
raw_bytestring_longbytes = br'''\r\
a'''
bytestring_longbytes = b'''\\r\\
a'''

print(raw_bytestring)
# b'\\r\\\na'
assert raw_bytestring \
	== bytestring \
	== raw_bytestring_longbytes \
	== bytestring_longbytes

print(raw_bytestring.decode())
# \r\
# a
assert raw_bytestring.decode() \
	== bytestring.decode() \
	== raw_bytestring_longbytes.decode() \
	== bytestring_longbytes.decode()

###########################
# Formatted string literals

class S:
	def __str__(self):
		return '__str__ñ'
	def __repr__(self):
		return '__repr__ñ'

string_object = S()

print(f'test {{s}} {string_object=!s}')
# test {s} string_object=__str__ñ
print(f'test {{s}} {string_object=!r}')
# test {s} string_object=__repr__ñ
print(f'test {{s}} {string_object=!a}')
# test {s} string_object=__repr__\xf1

print(f'{            False 	or True   =}')
#             False       or True   =True

## - Format Specification Mini-Language
# https://docs.python.org/3/library/string.html#format-specification-mini-language

print(f'a|{987654.3210:"^17,.8}|b')
# a|"""987,654.32""""|b

import locale
locale.setlocale(locale.LC_ALL, 'en_US')
print(f'{12345678:9^15n}')
# 9912,345,678999
locale.setlocale(locale.LC_ALL, '')

format = 'b'
print(f'{255:{format}}')
# 11111111
