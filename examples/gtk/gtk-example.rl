
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
