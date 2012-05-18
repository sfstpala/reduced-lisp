
from gi.repository import Gtk
for i in dir(Gtk):
    try:
        exec(i + " = Gtk." + i)
    except:
        pass
del i
del Gtk
