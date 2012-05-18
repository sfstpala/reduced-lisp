
(defun problem_1 (null)
    (reduce + (filter (lambda (i)
            (or (= (mod i 3) 0) (= (mod i 5) 0)))
        (range 1 1000))))

(defun problem_2 (null)
        (begin
            (define (sum 0))
            (define (a 1))
            (define (b 2))
            (define (sum 0))
            (while (or (< a 4000000) (= a 4000000)) (begin
                (define
                    (t (+ a b))
                    (a b)
                    (b t))
                (if (= (mod a 2) 0)
                    { the language needs a better way 
                        of assigning to the outer scope... }
                    (define (sum (+ sum a))))
                sum))))

(defun problem_20 (null)
    (let (factorial (lambda (n)
        (let (f (lambda (n acc)
            (if (= n 0)
                    acc
                (f (- n 1) (* acc n)))))
            (f n 1))))
        (reduce + (to-list (map
            (lambda (i) (integer i)) (str (factorial 100)))))))


(assert (= (problem_1) 233168))
(assert (= (problem_2) 4613732))
(assert (= (problem_20) 648))
