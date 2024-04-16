from gi.repository import Gtk, Gio, Adw

from src.state.state import login_state_manager, item_state_manager
from src.api.controller import Controller
from src.widgets.standard_widget import BoxedList, VBox, set_margin_all

class LoginPage(Adw.NavigationPage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initiliase()

    def initiliase(self):
        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box1.append(Adw.HeaderBar())
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box1.append(box2)
        clamp = Adw.Clamp()
        clamp.set_child(box2)
        clamp.set_maximum_size(350)
        center_box = Gtk.CenterBox(orientation=Gtk.Orientation.VERTICAL)
        center_box.set_center_widget(clamp)
        box1.append(center_box)
        self.set_child(box1)
        box = box2
        set_margin_all(box,5)
        box.set_margin_top(300)

        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Username")
        box.append(self.username_entry)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)
        box.append(self.password_entry)

        def login(_):
            try:
                controller = Controller(self.username_entry.get_text(),self.password_entry.get_text())
                if controller.logged_in():
                    item_state_manager.set_state(controller.get_items())
                    login_state_manager.set_state(controller.logged_in())
            except:
                return
        self.login_button = Gtk.Button(label="Login")
        self.login_button.connect("clicked", login)
        box.append(self.login_button)
