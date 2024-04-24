import logging
from gi.repository import Gtk, Gio, Adw

from src.state.state import login_state_manager, item_state_manager
from src.api.controller import Controller
from src.state.state_widget import StateWidget
from src.state.state import login_loading_state
from src.widgets.standard_widget import BoxedList, VBox, set_margin_all
from src.controller import controller, configs

class LoginPage(Adw.NavigationPage, StateWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        schema_source = Gio.SettingsSchemaSource.get_default()
        login_state_manager.subscribe(self)
        # schema = schema_source.lookup("com.github.mwickham.gwarden", True)
        # if schema is None:

        # self.settings = Gio.Settings("com.github.mwickham.gwarden")
        login_loading_state.subscribe(self)
        self.username = configs.username
        self.render()

    def render(self):
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
        self.username_entry.set_text(self.username)
        box.append(self.username_entry)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)
        box.append(self.password_entry)

        def login(_):
            logging.debug("login")
            try:
                # controller = Controller(self.username_entry.get_text(),self.password_entry.get_text())#
                configs.username = self.username_entry.get_text()
                configs.save()
                def login_callback(result):
                    if result is not None:
                        login_state_manager.set_state(True)
                        def callback(items):
                            print('CCCCCallback')
                            item_state_manager.set_state(items)
                        controller.get_items(callback)
                    login_loading_state.set_state(False)
                print("starting controller")
                controller.login(self.username_entry.get_text(),self.password_entry.get_text(), login_callback)
                print("finish controller")
                # if login_state_manager.read_state():
                #     controller.get_items(lambda items: item_state_manager.set_state(items))
                    # item_state_manager.set_state(controller.get_items())
                    # login_state_manager.set_state(controller.logged_in())
            except:
                return
            print("changing")
            login_loading_state.set_state(True)
        print('setting up')
        self.login_button = Gtk.Button(label="Login")
        self.login_button.connect("clicked", login)
        box.append(self.login_button)
        if login_loading_state.read_state():
            spinner = Gtk.Spinner()
            spinner.start()
            box.append(spinner)
