Reduced Lisp
============

A dynamic, functional, object oriented programming language. I can't believe it's not Scheme!

## What is it?

Reduced Lisp is a functional programming language. The syntax is based on the lisp family of languages:

 - `12` is an integer
 - `3-1j` is a complex number
 - `(^ 3-1j 12)` is a function call - it calls the "^" function, exponentiation, with two arguments.

Here's a small program:

    (defun f (x)
        (* x x))

    (print (f 12))

If you run it, it will print `(integer 144)`.

## Syntax

### Defining functions

To define functions, the `defun` macro is called with three arguments: a name,
a list of arguments and an expression - the function body.

    (defun <= (a b)
        (or (< a b) (= a b)))

The function, `<=`, will be available in the scope of the function itself
and in the scope in which it was run (but it is not a global variable).

### Defining variables

The `defun` macro is really just syntactic sugar for binding a variable,
in this case a function, to a name. You can use `define` to bind anything
to a name in this way:

    (define (greeting "hello"))
    (print greeting)

### Using values

If you don't want a value to be in the current namespace, you can use `let`.
The very last argument is an expression that is executed, the ones before it
are pairs of (name value).

    (let
        (name "lisp")
        (greeting "hello")
        (print greeting name))
