
(defun quicksort (a)
    (if (< (length a) 2)
            a
        (let
                (pivot (get a 0))
                (a (pop a 0))
                (<= (lambda (a b) (or (< a b) (= a b))))
            (extend
                (quicksort (filter (lambda (i) (<= i pivot)) a))
                (list pivot)
                (quicksort (filter (lambda (i) (> i pivot)) a))))))


(for i (quicksort (list 6 9 5 2 8 3 1 7 4))
    (print (str i)))
