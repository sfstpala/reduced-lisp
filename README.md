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

## Using RL

In order to run the interpreter, simply type `python3 rl.py`.
If you want to use the gtk extension module, you'll also have to
install the `python3-gi` package (this is Gtk3 with Gobject-Introspection).

Note: at the moment modules are loaded from the current working direction.

In order to run the gtk example, you'd therefore type

    cd examples/gtk
    python3 ../../rl.py gtk-example.rl


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

The value of a `let` expression is the value of the last expression in it. In
this case, it will be the value of a call to `print`, which is `null`.


### Anonymous functions

Anonymous functions, lambdas, are objects just like integers or strings, they
can be used as arguments, returned from functions and so on.

    (lambda (x) (* x x))


### Executing multiple expressions

To do multiple things, you can use the `(begin)` construct:

    (begin
        (print "hello")
        (print "world"))

The value of this expression will be the value of the last expression in it.

### Conditional Evaluation

Conditionals works like you'd expect:

    (if (&lt; 4 8)
            (print "four is less than eight")
        (print "eight is less than four.. huh?"))

### Looping constructs

While loops works similarly:

    (while true
        (print "are we there yet?"))

For loops take three arguments: a variable, or list of variables, an iterable
objects, such as a list, set, or range, and a body:

    (for i (range 10)
        (print i))

    (for (i j) (zip (range 10) (range 0 20 2))
        (print i j))

### Including modules

Extension modules can either be written in Python or reduced-lisp.
Running `(include gtk)` will make the interpreter look for a module
named either `gkt.py` or `gtk.rl`. If it is found, all the variables
defined in it will be assigned to `gtk.variablename`. 

    (include maths)
    (print (maths.square 12))

With maths.rl being

    (defun square (n)
        (* n n))


### Assertions

Assertions merely raise an error if their condition is not true:

    (assert (= result 144))


### Classes and Attributes

Classes are lists of expressions. Their namespace will become the class
namespace, and any function inside will become a method - meaning it will
receive the instance as the first argument (called `self`).

Attributes of classes can be got using `:` and set using `::`, i.e. `(:my_point x)` will return
the member `x` of the object `my_point`, and `(::my_moint x 12)` will set
it to 12.

Every class should have a method called `new`. It is automatically run after
the object has been created, and it can be used to set object attributes.

To create an instance of the class, simply call the class with the arguments
for `new`. Here's an example:

    (class Point

        (defun new (self x y)
            (begin
                (::self x x)
                (::self y y)))

        (defun get_x (self)
            (:self x))

        (defun get_y (self)
            (:self y)))


    (define (p
        (Point 1.34 7)))

    (print ((:p get_x)))
