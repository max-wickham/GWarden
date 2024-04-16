from gi.repository import Gtk, Gio, Adw


class VBox(Gtk.Box):

    def __init__(self, **kwargs):
        super().__init__(orientation = Gtk.Orientation.VERTICAL,vexpand=True, **kwargs)

    def clear(self):
        for child in self.get_children():
            self.remove(child)


class LLabel(Gtk.Label):

    def __init__(self, label, **kwargs):
        super().__init__(label = label, **kwargs)

        self.set_halign(Gtk.Align.START)

class BoxedList(Gtk.ListBox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(['boxed-list'])


def set_margin_all(widget, margin):
    widget.set_margin_top(10)
    widget.set_margin_bottom(10)
    widget.set_margin_start(10)
    widget.set_margin_end(10)
