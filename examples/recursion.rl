
(defun factorial (n)
    (let (f (lambda (n acc)
        (if (= n 0)
                acc
            (f (- n 1) (* acc n)))))
        (f n 1)))

(define (n (factorial 20000)))

(print (+ "the factorial of 20,000 has "
    (str (- (length (str n)) 2)) " digits"))
