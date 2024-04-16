import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw


from abc import ABC, abstractmethod, ABCMeta

class _ABCQObjectMeta(type(Gtk.Widget), ABCMeta):
    ...

class StateWidget(ABC, Gtk.Widget, metaclass=_ABCQObjectMeta):

    @abstractmethod
    def render(self):
        ...
