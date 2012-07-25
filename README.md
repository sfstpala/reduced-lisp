Reduced Lisp
============

A dynamic, functional, object oriented programming language. I can't believe it's not Scheme!

# Quick Example

Here's a short program that demonstrates how RL integrates with python extension modules, in this case `examples/gtk/gtk.py`.


    (include gtk)


    (class Application
        (defun new (self)
            (begin
                (::self builder ((:gtk.Builder new)))
                ((:(:self builder) add_from_file) "test.glade")
                ((:(:self builder) connect_signals) self)))
        (defun quit (self widget)
            (gtk.main_quit))
        (defun run (self)
            (gtk.main)))


    ((:(Application) run))

## What is RL?

Reduced Lisp is an interpreted, functional programming language written in Python 3.
The syntax is based on the lisp family of languages:

 - `12` is an integer
 - `3-1j` is a complex number
 - `(^ 3-1j 12)` is a function call - it calls the "^" function, exponentiation, with two arguments.

Here's a small program:

    (defun f (x)
        (* x x))

    (print (f 12))

If you run it, it will print `(integer 144)`.

RL optimizes tail recursion. If you can write a recursive function so that
the last expression is a recursive call, you don't have to worry about
stack overflows:

    ; naive factorial, not tail-recursive (will crash for large n)
    (defun factorial (n)
        (if (= n 0)
                1
            (* n (factorial (- n 1)))))


    ; this is a tail-recursive function (won't crash).
    (defun factorial' (n)
        (let (f (lambda (n acc)
            (if (= n 0)
                    acc
                (f (- n 1) (* acc n)))))
            (f n 1)))

    (print (factorial' 2000))

You can just type all of this into a terminal:

    python3 rl.py


## Using RL

In order to run the interpreter, simply type `python3 rl.py`.
If you want to use the gtk extension module, you'll also have to
install the `python3-gi` package (this is Gtk3 with Gobject-Introspection).

Note: at the moment modules are loaded from the current working directory.

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

    (if (< 4 8)
            (print "four is less than eight")
        (print "eight is less than four.. huh?"))

### Looping constructs

You can loop by simply writing a tail recursive function, but there are also
`while` and `for` loops built in:

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

        (defun distance (self other)
            (sqrt (+
                (^ (- (:other x) (:self x)) 2)
                (^ (- (:other y) (:self y)) 2))))

        (defun get_x (self)
            (:self x))

        (defun get_y (self)
            (:self y)))


    (define (p
        (Point 1.34 7)))
    (define (q
        (Point 2.34 8)))


    (print ((:p distance) q))


### Comments

Inline comments are inside of curly braces, line comments begin with a semicolon.


## Types

These are the built in types:

 - null (always `null`)
 - boolean (`true` and `false`)
 - integer (i.e. `12`, `-9`, `0b101101011`)
 - real (i.e. `0.5`, `.3`, `2e-99`)
 - complex (i.e. `1j`, `7.5-4j`)
 - list (i.e. `(list 1 2 3 4)`)
 - set (i.e. `(set)`, `(set 1 2 3 4)`)
 - functions (i.e. `(lambda (x) x)`)

### Built-in Functions

RL comes with loads of built-in functions. Type `(help "functions")` in
the interactive prompt to get a list of them. Here's just one example on
how to use them:

    (defun even-squares-up-to (n)
        ; print the even squares of all numbers up to n
        (filter (lambda (j) (= (mod j 2) 0))
            (map (lambda (i) (* i i))
                (range n))))

    (defun sum (a)
        (reduce + a))

    (defun sum-of-even-squares-up-to (n)
        (sum (even-squares-up-to n)))


Arithmetic functions, such as `+` or `mod` take any number of arguments - i.e.
`(+ 1 2 3)` is equivalent to `(+ (+ 1 2) 3)`. However, predicates such as `=`,
`and`, `or`, `not` only take two arguments.

The functions `map`, `reduce` and `filter` take a function as their first
argument and a list, or set, as their second argument.

    (defun add-one (n) (+ n 1))
    (map add-one (list 1 2 3)) ; returns (list 2 3 4)

List-related functions (head, tail, get, pop, push, append, extend, length)
never modify the actual object: lists are immutable.

    (define (a (list 1 2 3)))
    (print (pop a 0)) ; will return (list 2 3)
    (print (push a 4 0)) ; will return (list 4 1 2 3)
    (assert (= a (list 1 2 3)))

For operations on sets, there are five functions pre-defined: union, difference,
symmetric-difference, intersection, and cross-product. To convert a set
into a list, use `(to-list myset)`, and `(to-set mylist)` to convert a list
into a set.

Note: At the moment, language semantics change pretty much every time I make
a new commit. I'll will try to keep the documentation up to date.
