import ast
import sys, token, tokenize

def   delete_docstring(tmp_filepath1, tmp_filepath2):
    """ Run on just one file.

    """
    with open(tmp_filepath1, "r") as source:
        with open(tmp_filepath2, "w") as mod:

            prev_toktype = token.INDENT
            first_line = None
            last_lineno = -1
            last_col = 0

            tokgen = tokenize.generate_tokens(source.readline)
            for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
                # if 0:   # Change to if 1 to see the tokens fly by.
                #     print("%10s %-14s %-20r %r" % (
                #         tokenize.tok_name.get(toktype, toktype),
                #         "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                #         ttext, ltext
                #         ))
                if slineno > last_lineno:
                    last_col = 0
                if scol > last_col:
                    mod.write(" " * (scol - last_col))
                if not (toktype == token.STRING and prev_toktype == token.INDENT):
                    mod.write(ttext)
                prev_toktype = toktype
                last_col = ecol
                last_lineno = elineno
    result = ""
    with open(tmp_filepath2, "r") as mod:
        result = "".join(mod.readlines())
    return result

result = delete_docstring("/Users/mikhail.malofeev/programm/ml/thesis/playground/source.py", "script.txt")
print(result)