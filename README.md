Reduced Lisp
============

A dynamic, functional, object oriented programming language. I can't believe it's not Scheme!

## What is it?

Reduced Lisp is a functional programming language. The syntax is based on the lisp family of languages:

 - `12` is an integer
 - `3-1j` is a complex number
 - `(^ 3-1j 12)` is a function call - it calls the "^" function, exponentiation with two arguments.

Here's a small program:

    (defun f (x)
        (* x x))

    (print (f 12))

If you run it, it will print `(integer 144)`.
