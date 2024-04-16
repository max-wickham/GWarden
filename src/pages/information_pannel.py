from gi.repository import Gtk, Gio, Adw, Gdk


from src.api.passer import Item, ItemType
from src.api.types import APICardItem, APIIdentityItem, APILoginItem, APISecureNoteItem
from src.state.state_widget import StateWidget
from src.widgets.standard_widget import BoxedList, VBox, set_margin_all
from src.state.state import selected_item_state_manager
from src.widgets.specialised_widgets import CopyRow, VisibleCopyRow


class ItemInformationPage(VBox, StateWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        header_bar = Adw.HeaderBar()
        self.append(header_bar)
        selected_item_state_manager.subscribe(self)
        self.initialise()
        self.ui = None

    def initialise(self):
        ...


    def render(self):
        selected_item: Item | None = selected_item_state_manager.read_state()
        if self.ui is not None:
            self.remove(self.ui)
        if not isinstance(selected_item, Item):
            return
        match selected_item.item_type:
            case ItemType.Login:
                if not isinstance(selected_item.value, APILoginItem):
                    return
                self.render_login(selected_item.value, selected_item)
            case ItemType.SecureNote:
                if not isinstance(selected_item.value, APISecureNoteItem):
                    return
                self.render_note(selected_item.value, selected_item)
            case ItemType.Card:
                if not isinstance(selected_item.value, APICardItem):
                    return
                self.render_card(selected_item.value,selected_item)
            case ItemType.Identity:
                if not isinstance(selected_item.value, APIIdentityItem):
                    return
                self.render_identity(selected_item.value, selected_item)

    def render_login(self, login: APILoginItem, item: Item):
        ui = VBox()
        boxed_list = BoxedList()
        boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
        set_margin_all(boxed_list,32)
        name_row = Adw.ActionRow()
        name_row.set_selectable(False)
        name_row.set_title(item.name)
        sub_boxed_list = BoxedList()
        set_margin_all(sub_boxed_list,32)
        username_row = CopyRow("Username", login.username)
        sub_boxed_list.append(username_row)
        sub_boxed_list.append(VisibleCopyRow("Password",login.password))
        boxed_list.append(name_row)
        boxed_list.append(sub_boxed_list)
        sub_boxed_list = BoxedList()
        set_margin_all(sub_boxed_list,32)
        expander_row = Adw.ExpanderRow()
        expander_row.set_title("URIs")
        expander_row.set_activatable(False)
        expander_row.set_selectable(False)
        expander_row.set_expanded(True)
        for uri in login.uris if login.uris is not None else []:
            uri_row = Adw.ActionRow()
            uri_row.set_activatable(True)
            uri_row.set_selectable(False)
            uri_row.set_title(uri.uri if uri.uri is not None else "")
            uri_row.set_icon_name("edit-copy")
            if isinstance(uri.uri, list):
                uri.uri = uri.uri[0]
            expander_row.add_row(CopyRow(uri.uri if uri.uri is not None else "",""))
        sub_boxed_list.append(expander_row)
        boxed_list.append(sub_boxed_list)
        ui.append(boxed_list)
        self.ui = ui
        self.append(ui)

    def render_note(self, note: APISecureNoteItem, item: Item):
        ui = VBox()
        boxed_list = BoxedList()
        boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
        set_margin_all(boxed_list,32)
        name_row = Adw.ActionRow()
        name_row.set_selectable(False)
        name_row.set_title(item.name)
        sub_boxed_list = BoxedList()
        set_margin_all(sub_boxed_list,32)

        text_view = Gtk.TextView()
        set_margin_all(text_view, 5)
        buffer = Gtk.TextBuffer()
        buffer.set_text(item.note)
        text_view.set_buffer(buffer)
        note_row = Adw.ActionRow()
        note_row.set_selectable(False)
        note_row.set_child(text_view)
        sub_boxed_list.append(note_row)
        boxed_list.append(name_row)
        boxed_list.append(sub_boxed_list)
        ui.append(boxed_list)
        self.ui = ui
        self.append(ui)

    def render_card(self, card: APICardItem, item: Item):
        ui = VBox()
        boxed_list = BoxedList()
        boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
        set_margin_all(boxed_list,32)
        boxed_list.append(CopyRow("Cardholder", card.cardholder_name))
        boxed_list.append(CopyRow("Brand", card.brand))
        boxed_list.append(CopyRow("Number", card.number))
        boxed_list.append(CopyRow("Expiry", f"{card.exp_month}/{card.exp_year}"))
        boxed_list.append(VisibleCopyRow("Code", card.code))
        ui.append(boxed_list)
        self.ui = ui
        self.append(ui)

    def render_identity(self, identity: APIIdentityItem, item: Item):
        ui = VBox()
        boxed_list = BoxedList()
        boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
        set_margin_all(boxed_list,32)
        boxed_list.append(CopyRow("Title", identity.title))
        boxed_list.append(CopyRow("First Name", identity.first_name))
        boxed_list.append(CopyRow("Last Name", identity.last_name))
        boxed_list.append(CopyRow("Address 1", identity.address1))
        boxed_list.append(CopyRow("Address 2", identity.address2))
        boxed_list.append(CopyRow("City", identity.city))
        boxed_list.append(CopyRow("State", identity.state))
        boxed_list.append(CopyRow("Postal Code", identity.postal_code))
        boxed_list.append(CopyRow("Company", identity.company))
        boxed_list.append(CopyRow("Country", identity.country))
        boxed_list.append(CopyRow("Phone", identity.phone))
        boxed_list.append(CopyRow("Email", identity.email))
        boxed_list.append(CopyRow("SSN", identity.ssn))
        boxed_list.append(CopyRow("License Number", identity.license_number))
        boxed_list.append(CopyRow("Passport Number", identity.passport_number))
        boxed_list.append(CopyRow("Username", identity.username))
        boxed_list.append(VisibleCopyRow("Password", identity.password))
        ui.append(boxed_list)
        self.ui = ui
        self.append(ui)
