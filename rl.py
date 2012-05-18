# Reduced Lisp Interpreter
#    Copyright (C) 2012  Stefano Palazzo <stefano-palazzo@ubuntu.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



begin, end = object(), object()
whitespace, comment = object(), object()
alphabet = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789!#$%&'*+,-./<=>?@[]^_|~")


def get_token(t):
    if t in " \r\n\t\v":
        return whitespace
    if t == "(":
        return begin
    if t == ")":
        return end
    if t.startswith("\"") and t.endswith("\""):
        if t != "\"" and "\"" not in t[1:-1].replace("\\\"", ""):
            return t
    if t.startswith(";") and t.endswith("\n"):
        return comment
    if t.startswith("{") and t.endswith("}"):
        return comment
    if t == "::":
        return t
    if t == ":":
        return t
    if all(i in alphabet for i in t):
        return t


def tokenize(code):
    token, code, line, char = "", code + "\0", 1, 0
    while code:
        line, char = line + (code[0] == "\n"), char + 1
        token, code = token + code[0], code[1:]
        t0 = get_token(token)
        if t0 and not any([get_token(token + code[:i]) for i in range(1, 4)]):
            yield t0, line, char
            token = ""


class Token (str):

    def __new__(cls, line, char, *args, **kwargs):
        self = str.__new__(cls, *args, **kwargs)
        self.line, self.char = line, char
        return self

    def __repr__(self):
        return str(self)


class Expression (list):

    def __init__(self, line, char, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self.line, self.char = line, char

    def __repr__(self):
        return "(" + " ".join(repr(i) for i in self) + ")"


def parse(tokens):
    s, o = Expression(1, 0), Expression(1, 0)
    for i, line, char in tokens:
        if i is begin:
            s.append(Expression(line, char))
            o.append(s)
            s = s[-1]
        elif i is end:
            s = o.pop(-1)
        elif i is not whitespace and i is not comment:
            s.append(Token(line, char, i))
    return s


def error(t, hint, token):
    print("# {}: {} in line {}".format(t, hint, token.line))
    print("#", repr(token)[:54] + ("..." if len(repr(token)) > 54 else ""))
    exit(1)


def validate(expr):
    if isinstance(expr, str):
        return
    if not expr:
        error("syntax error", "empty expression", expr)
    if expr[0] == "fun":
        if len(expr) not in (3, 4):
            error("syntax error", "malformed function", expr)
        return
    for i in expr:
        validate(i)


def reduced(fn):
    def wrapped(*args):
        i = args[0]
        for j in args[1:]:
            i = fn(i, j)
        return i
    return wrapped


def reduce(fn, i):
    j = i[0]
    for k in i[1:]:
        j = fn(j, k)
    return j


def f_repr(i):
    if isinstance(i, type(lambda: None)):
        return "(lambda ...)"
    return repr(i)


def f_help(n=0):
    if n == 0:
        print("Welcome to reduced lisp. Let's quickly go over the basics:")
        print(" - to define the function f(x)=x*x, type")
        print("       \33[0;32m(defun f (x) (* x x))\33[m")
        print(" - to call it, type \33[0;32m(f 12)\33[m")
        print(" - define variables with \33[0;33m(define name value)\33[m")
        print(" - anonymous functions look like this:")
        print("       \33[0;32m(lambda (x) (* x x))\33[m")
        print(" - try calling the built-in functions \33[0;33m(list)\33[m and"
            " \33[0;33m(set)\33[m with")
        print("   some arguments. ")
        print("Type \33[0;32m(help 1)\33[m for more.")
    elif n == 1:
        print("The built-in types are \33[0;34minteger\33[m, \33[0;34mreal"
            "\33[m, \33[0;34mcomplex\33[m, \33[0;34mlist\33[m,\n  \33[0;34mset"
            "\33[m, \33[0;34mlambda\33[m, and \33[0;34mstring""\33[m.")
        print("The built-in objects are \33[0;36mnull\33[m, "
            "\33[0;36mtrue\33[m, and \33[0;36mfalse\33[m.")
        print("Type \33[0;32m(help \"functions\")\33[m for a list of all"
            " built-in functions.")
    elif n == "functions":
        print(', '.join(sorted(default_var.keys())))
    else:
        print("nothing here...")
    return NullObj()


default_var = {
    "list": lambda *a: ListObj(list(i for i in a)),
    "set": lambda *a: SetObj(i for i in a),
    "to-list": lambda a: ListObj(list(i for i in a)),
    "to-set": lambda a: SetObj(i for i in a),
    "integer": lambda x: IntegerObj(int(x, 0) if isinstance(x, str) else x),
    "hex": lambda x: hex(x),
    "oct": lambda x: oct(x),
    "bin": lambda x: bin(x),
    "boolean": lambda x: TrueObj() if x else FalseObj(),
    "real": lambda x: (RealObj(x.real) if isinstance(x, ComplexObj)
        else RealObj(x)),
    "complex": lambda x: ComplexObj(x),
    "str": lambda x: str(x),
    "print": lambda *a: [print(*[repr(i) if isinstance(i, Object)
        else f_repr(i) for i in a]), NullObj()][1],
    "+": reduced(lambda a, b: type(a)(a + b)),
    "-": reduced(lambda a, b: type(a)(a - b)),
    "*": reduced(lambda a, b: type(a)(a * b)),
    "^": reduced(lambda a, b: type(a)(a ** b)),
    "/": reduced(lambda a, b: type(a)(a / b)),
    "mod": reduced(lambda a, b: type(a)(a % b)),
    "<": lambda a, b: TrueObj() if (a < b) else FalseObj(),
    "=": lambda a, b: TrueObj() if (a == b) else FalseObj(),
    ">": lambda a, b: TrueObj() if (a > b) else FalseObj(),
    "and": reduced(lambda a, b: TrueObj() if (a and b) else FalseObj()),
    "or": reduced(lambda a, b: TrueObj() if (a or b) else FalseObj()),
    "not": lambda a: TrueObj() if (not a) else FalseObj(),
    "head": lambda a: a[0],
    "tail": lambda a: ListObj(i for i in a[1:]),
    "get": lambda a, n: a[n],
    "pop": lambda a, n: ListObj([i for n_, i in enumerate(a) if n_ != n]),
    "push": lambda a, x, n=-1: ListObj(list(a[:n]) + [x] + list(a[n:])),
    "append": lambda a, x: ListObj(list(a) + [x]),
    "extend": reduced(lambda a, b: ListObj(a + b)),
    "length": lambda a: IntegerObj(len(a)),
    "map": lambda fn, a: ListObj([fn(i) for i in a]),
    "reduce": reduce,
    "filter": lambda fn, a: ListObj([i for i in a if fn(i)]),
    "exit": lambda n=0: exit(n),
    "union": reduced(lambda a, b: SetObj(a | b)),
    "symmetric-difference": reduced(lambda a, b: SetObj(a ^ b)),
    "difference": reduced(lambda a, b: SetObj(a - b)),
    "intersection": reduced(lambda a, b: SetObj(a & b)),
    "cross-product": reduced(lambda a, b: SetObj(ListObj([i, j])
        for i in a for j in b)),
    "range": lambda *args: ListObj(range(*args)),
    "sqrt": lambda x: RealObj(x ** 0.5) if x >= 0 else ComplexObj(x ** 0.5),
    "imag": lambda x: RealObj(x.imag),
    "zip": lambda *a: list(zip(*a)),
    "help": f_help,
}

class Object (object):

    def __repr__(self):
        return "..."


class FunctionObj (Object):

    def __init__(self, fn, var, args):
        self.fn, self.var, self.args = fn, var, args

    def __call__(self, *args):
        self.var.update(dict(zip(self.args, args)))
        return evaluate(self.fn, self.var)

    def __repr__(self):
        return "(lambda {} ...)".format(self.args)


class MethodObj (Object):

    def __init__(self, f_self, fo):
        self.fn, self.var, self.args = fo.fn, fo.var, fo.args
        self.f_self = f_self

    def __call__(self, *args):
        self.var.update(dict(zip(self.args, [self.f_self] + list(args))))
        return evaluate(self.fn, self.var)

    def __repr__(self):
        return "(lambda {} ...)".format(self.args)


class IntegerObj (Object, int):

    def __repr__(self):
        return "(integer {})".format(str(self))


class RealObj (Object, float):

    def __repr__(self):
        return "(real {})".format(str(self))


class ComplexObj (Object, complex):

    def __repr__(self):
        return "(complex {})".format(
            complex.__repr__(self).lstrip("(").rstrip(")"))

    def __str__(self):
        return complex.__repr__(self).lstrip("(").rstrip(")")


class ListObj (Object, tuple):

    def __repr__(self):
        return ("(list " + " ".join(repr(i) for i in self)).strip() + ")"


class SetObj (Object, frozenset):

    def __repr__(self):
        return ("(set " + " ".join(repr(i) for i in self)).strip() + ")"


class TrueObj (Object):

    def __repr__(self):
        return "true"

    def __bool__(self):
        return True


class FalseObj (Object):

    def __repr__(self):
        return "false"

    def __bool__(self):
        return False


class NullObj (Object):

    def __repr__(self):
        return "null"

    def __bool__(self):
        return False


def literal_eval(i):
    if i.startswith("\""):
        return str(i[1:-1].replace("\\\"", "\""))
    try:
        return IntegerObj(int(i, 0))
    except:
        pass
    for t in (RealObj, ComplexObj):
        try:
            return t(i)
        except:
            pass
    if i in ("true", "false", "null"):
        return {"true": TrueObj(), "false": FalseObj(), "null": NullObj()}[i]
    error("name error", "invalid name", i)


def object_eval(i):
    if isinstance(i, type(lambda x: x)):
        return i
    if isinstance(i, int):
        return IntegerObj(i)
    if isinstance(i, float):
        return RealObj(i)
    if isinstance(i, complex):
        return ComplexObj(i)
    if isinstance(i, list):
        return ListObj(i)
    if i is True:
        return TrueObj()
    if i is False:
        return FalseObj()
    if i is None:
        return NullObj()


def do_import(f, v):
    try:
        fn = str(f) + ".rl"
        code = open(fn).read()
        var = {k: v for k, v in default_var.items()}
        if code.strip():
            code = tokenize(code.strip())
            code = parse(code)
            if code:
                validate(code)
                for i in code:
                    evaluate(i, var)
        v.update({str(f) + "." + k: o for k, o in var.items() if k not in v})
        return
    except IOError:
        pass
    try:
        globs, locs = {}, {}
        mod = exec(open(str(f) + ".py").read(), globs, locs)
        for k, o in list(locs.items()) + list(globs.items()):
            o_ = object_eval(o)
            if o_ is not None:
                v[f + "." + k] = o_
            else:
                v[f + "." + k] = o
        return
    except IOError:
        pass
    raise IOError()


class InstanceObj (Object):

    def __init__(self, name, var):
        self.name, self.var = name, var

    def __repr__(self):
        return "({} ...)".format(self.name)


class ClassObj (Object):

    def __init__(self, name, var):
        self.name, self.var = name, var
        self.attr = {}
        for i in var:
            self.attr[i] = var[i]

    def __repr__(self):
        return "(class {} ...)".format(self.name)

    def __call__(self, *args):
        s = InstanceObj(self.name, self.var)
        for i in self.attr:
            setattr(s, i, MethodObj(s, self.attr[i]))
        if hasattr(s, "new"):
            s.new(*args)
        return s


def evaluate(expr, var=default_var, new={}):
    v = dict(list(var.items()) + list(dict(new).items()))
    while True:
        if isinstance(expr, Token):
            # expr is either a literal or a name that has been assigned a value
            return v[expr] if expr in v else literal_eval(expr)
        elif isinstance(expr, Expression):
            if expr[0] == "defun":
                # (def f (x) (* x x))
                var[expr[1]] = FunctionObj(expr[3], var, expr[2])
                return NullObj()
            elif expr[0] == "let":
                # (let (greeting "hello") (print greeting))
                for k, o in expr[1:-1]:
                    v[k] = evaluate(o, v)
                expr = expr[-1]
            elif expr[0] == "define":
                # (export (greeting "hello")) (print greeting)
                for k, o in expr[1:]:
                    var[k] = v[k] = evaluate(o, v)
                return NullObj()
            elif expr[0] == "lambda":
                # (lambda (x) (* x x))
                return FunctionObj(expr[2], v, expr[1])
            elif expr[0] == "class":
                vx = {k: o for k, o in v.items()}
                for i in expr[2:]:
                    evaluate(i, vx)
                vx = {k: o for k, o in vx.items() if k not in v}
                var[expr[1]] = ClassObj(expr[1], vx)
                return
            elif expr[0] == "begin":
                # (begin (print "hello") (print "world"))
                for i in expr[1:-1]:
                    evaluate(i, v)
                expr = expr[-1]
            elif expr[0] == ":":
                o = evaluate(expr[1], v)
                if not expr[2].startswith("__") and hasattr(o, expr[2]):
                    return getattr(o, expr[2])
                error("attribute error", "invalid attribute", expr)
            elif expr[0] == "::":
                o = evaluate(expr[1], v)
                setattr(o, expr[2], evaluate(expr[3], v))
                return
            elif expr[0] == "if":
                # (if (< n 0) (- 0 n) n)
                if evaluate(expr[1], v):
                    expr = expr[2]
                else:
                    if not expr[3:]:
                        return NullObj()
                    expr = expr[3]
            elif expr[0] == "while":
                # (while true (print "hello"))
                r = None
                while evaluate(expr[1], var):
                    r = evaluate(expr[2], var)
                return r
            elif expr[0] == "assert":
                # (assert true)
                if not evaluate(expr[1], v):
                    error("assertion-error", "assertion failed", expr)
                return NullObj()
            elif expr[0] == "include":
                try:
                    do_import(expr[1], var)
                except IOError:
                    error("include-error", "file not found", expr)
                return NullObj()
            elif expr[0] == "for":
                # (for i (range 10) (print i))
                # (for (i j) (zip (range 10) (range 0 20 2)) (print i j))
                for i in evaluate(expr[2], v):
                    if isinstance(expr[1], Token):
                        v[expr[1]] = i
                    else:
                        for j, x in zip(expr[1], i):
                            v[j] = x
                    r = evaluate(expr[3], v)
                var.update(v)
                return r
            else:
                # (print 1 2 3)
                exps = [evaluate(i, v) for i in expr]
                if isinstance(exps[0], FunctionObj):
                    expr = exps[0].fn
                    if isinstance(exps[0].args, Token):
                        v.update({exps[0].args: ListObj(exps[1:])})
                    else:
                        v.update(dict(zip(exps[0].args, exps[1:])))
                else:
                    return exps[0](*exps[1:])
        else:
            raise ValueError(expr)


def repl():
    try:
        import readline
    except ImportError:
        pass
    print("\33[1mReduced Lisp 0.1\33[m")
    print("\33[0;36mtype (help), (exit) to quit\33[m")
    var = {k: v for k, v in default_var.items()}
    while True:
        try:
            code = input("\33[1;32m>\33[m ")
            if not code.strip():
                continue
            tokens = list(tokenize(code))
            n = 0
            for i, *_ in tokens:
                n += 1 if i is begin else -1 if i is end else 0
            while n != 0:
                code = input("  ")
                if not code.strip():
                    continue
                tokens += list(tokenize(code))
                n = 0
                for i, *_ in tokens:
                    n += 1 if i is begin else -1 if i is end else 0
            code = parse(tokens)
            validate(code)
            for i in code:
                try:
                    result = evaluate(i, var)
                except KeyboardInterrupt:
                    print()
                    continue
                if not isinstance(result, NullObj):
                    print(f_repr(result))
        except KeyboardInterrupt:
            print()
            exit(1)


def run(f):
    if f.strip():
        code = tokenize(f.strip())
        code = parse(code)
        if code:
            validate(code)
            var = {k: v for k, v in default_var.items()}
            for i in code:
                evaluate(i, var)


if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        exit(run(open(sys.argv[1]).read()))
    exit(repl())
