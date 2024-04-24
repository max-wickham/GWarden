from gi.repository import Gtk, Gio, Adw

from src.state.state_widget import StateWidget
from src.widgets.standard_widget import VBox
from src.api.passer import Item, ItemType
from src.api.types import APILoginItem
from src.state.state_manager import StateManager
from src.widgets.standard_widget import LLabel
from src.state.state import item_state_manager,selected_item_state_manager

class ListItem(VBox):
    '''Individual item in the list of items. It contains the name of the item and the username of the item.'''

    def __init__(self, name: str | None, username: str | None, item: Item):
        super().__init__()
        self.item = item
        self.set_spacing(12)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)
        if name is None:
            name = ""
        if username is None:
            username = ""
        name_label = LLabel("")
        name_label.set_markup(f"<b>{name}</b>")
        username_label = LLabel(username)
        self.append(name_label)
        self.append(username_label)

class ItemListPage(VBox,StateWidget):

    def __init__(self, split_view, **kwargs):
        super().__init__(**kwargs)
        self.search_bar_state = StateManager(default = "")
        self.search_bar_state.subscribe(self)
        self.split_view = split_view
        header_bar = Adw.HeaderBar()
        self.append(header_bar)
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name('open-menu-symbolic')
        menu = Gio.Menu.new()
        menu.append("About","app.about")
        menu.append("Logout","app.logout")
        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)
        menu_button.set_popover(self.popover)

        header_bar.pack_end(menu_button)
        self.orientation = Gtk.Orientation.VERTICAL
        item_state_manager.subscribe(self)
        self.initialise()
        self.render()

    def initialise(self):
        self.list_box = Gtk.ListBox(vexpand=True, hexpand=True)
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.get_style_context().add_class("no-corner-radius")
        def on_search_changed(_):
            self.search_bar_state.set_state(self.search_entry.get_text())
        self.search_entry.connect("changed", on_search_changed)
        self.scrolled_window = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.scrolled_window.set_child(self.list_box)
        self.append(self.search_entry)
        self.append(self.scrolled_window)

    def render(self):
        items = item_state_manager.read_state()
        if items is None:
            items = []
        list_box = Gtk.ListBox(vexpand=True, hexpand=True)
        for item in [item for item in items if self.search_bar_state.read_state().lower() in item.name.lower()]:
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("dark-border")
            row.set_child(ListItem(item.name, item.value.username, item)
                            if item.item_type == ItemType.Login else
                            list_box.append(ListItem(item.name, "", item)))
            list_box.append(row)
        self.scrolled_window.set_child(list_box)
        def list_box_clicked(_, row):
            selected_item = row.get_child().item
            selected_item_state_manager.set_state(selected_item)
            self.split_view.set_show_content(True)

        list_box.connect('row-selected',list_box_clicked)
