from gi.repository import Gtk, Gio, Adw, Gdk

from src.state.state_manager import StateManager
from src.state.state_widget import StateWidget
from src.widgets.standard_widget import LLabel


class CopyRow(Adw.ActionRow):

    def __init__(self, title: str, text: str | None):
        super().__init__()
        self.text = text if text is not None else ""
        self.title = title
        self.initialise()

    def initialise(self):
        self.set_activatable(True)
        self.set_selectable(False)
        self.set_title(self.title)
        self.set_icon_name("edit-copy")
        self.label = LLabel(self.text)
        self.add_suffix(self.label)
        def on_copy_clicked(_):
            add_to_clipboard(self.text)
        self.connect("activated", on_copy_clicked)

class VisibleCopyRow(Adw.ActionRow, StateWidget):

    def __init__(self, title: str, text: str | None):
        super().__init__()
        self.state_manager = StateManager(default = False)
        self.state_manager.subscribe(self)
        self.text = text if text is not None else ""
        self.title = title
        self.initialise()
        self.render()

    def initialise(self):
        self.set_activatable(True)
        self.set_selectable(False)
        self.set_title(self.title)
        self.set_icon_name("edit-copy")
        self.label = LLabel(self.text) if self.state_manager.read_state() else LLabel("*" * len(self.text))
        self.add_suffix(self.label)
        self.toggle_button = Gtk.ToggleButton()
        self.toggle_button.set_active(False)
        self.toggle_button.get_style_context().add_class("no-background")
        self.toggle_button.set_icon_name("view-conceal-symbolic" if self.state_manager.read_state() else "view-reveal-symbolic")
        self.toggle_button.set_tooltip_text("Show/Hide Password")
        def visible_clicked(button):
            self.state_manager.set_state(not self.state_manager.read_state())

        self.toggle_button.connect("clicked", visible_clicked)
        self.add_suffix(self.toggle_button)

        def on_copy_clicked(_):
            add_to_clipboard(self.text)
        self.connect("activated", on_copy_clicked)



    def render(self):
        self.label.set_text(
            self.text if self.state_manager.read_state() else
            "*" * len(self.text)
        )
        self.toggle_button.set_icon_name("view-conceal-symbolic" if self.state_manager.read_state() else "view-reveal-symbolic")

def add_to_clipboard(text):
    clipboard = Gdk.Display.get_default().get_clipboard()
    clipboard.set(text)
