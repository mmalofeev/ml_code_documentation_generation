import ast

import astor  # read more at https://astor.readthedocs.io/en/latest/
#
# parsed = ast.parse(open('source.py').read())
#
# for node in ast.walk(parsed):
#     # let's work only on functions & classes definitions
#     if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
#         continue
#
#     if not len(node.body):
#         continue
#
#     if not isinstance(node.body[0], ast.Expr):
#         continue
#
#     if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
#         continue
#
#     # Uncomment lines below if you want print what and where we are removing
#     # print(node)
#     # print(node.body[0].value.s)
#
#     node.body = node.body[1:]
#
# print('***** Processed source code output ******\n=========================================')
#
# print(astor.to_source(parsed))

import sys, token, tokenize

def do_file(fname):
    """ Run on just one file.

    """
    source = open(fname)
    mod = open(fname + ",strip", "w")

    prev_toktype = token.INDENT
    first_line = None
    last_lineno = -1
    last_col = 0

    tokgen = tokenize.generate_tokens(source.readline)
    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
        if 0:   # Change to if 1 to see the tokens fly by.
            print("%10s %-14s %-20r %r" % (
                tokenize.tok_name.get(toktype, toktype),
                "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                ttext, ltext
                ))
        if slineno > last_lineno:
            last_col = 0
        if scol > last_col:
            mod.write(" " * (scol - last_col))
        if toktype == token.STRING and prev_toktype == token.INDENT:
            # Docstring
            mod.write("#--")
        else:
            mod.write(ttext)
        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno

do_file("source.py")