
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
