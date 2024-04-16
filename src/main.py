# main.py
#
# Copyright 2024 Max Wickham
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk

from src.api.controller import Controller
from src.pages.information_pannel import ItemInformationPage
from src.pages.login_page import LoginPage
from src.state.state import login_state_manager
from src.pages.item_list import ItemListPage
from src.state.state_widget import StateWidget
from src.widgets.standard_widget import VBox
from src.state.state import item_state_manager



class GwardenApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.gwarden.mwickham.github',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('logout', lambda : login_state_manager.set_state(False))

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = AppWindow(application = self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='GWarden',
                                application_icon='gwarden.mwickham.github',
                                developer_name='Max Wickham',
                                version='0.0.1',
                                developers=['Max Wickham'],
                                copyright='© 2024 Max Wickham')
        about.present()


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


class AppWindow(Adw.ApplicationWindow, StateWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        login_state_manager.subscribe(self)
        self.set_title('Gnomebitwarden')
        self.set_default_size(800, 600)
        file_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{file_path}/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.initialise()
        self.render()

    def initialise(self):
        split_view = Adw.NavigationSplitView(vexpand=True, hexpand=True)
        content_page = Adw.NavigationPage(vexpand=True, hexpand=True)
        content_page.set_child(
            ItemInformationPage()
        )
        side_page = Adw.NavigationPage(vexpand=True, hexpand=True)
        side_page.set_child(
            ItemListPage(split_view)
        )
        split_view.set_content(content_page)
        split_view.set_sidebar(side_page)
        split_view.set_min_sidebar_width(400.0)
        main_box = VBox()
        main_box.append(split_view)
        self.main_box = main_box
        self.login_page = LoginPage()
        break_point = Adw.Breakpoint.new(Adw.BreakpointCondition.new_length(
            Adw.BreakpointConditionLengthType.MAX_WIDTH, 900.0, Adw.LengthUnit.PX
        ))
        break_point.add_setter(split_view, "collapsed", True);
        self.add_breakpoint(break_point)

    def render(self):
        if login_state_manager.read_state():
            self.set_content(self.main_box)
        else:
            self.set_content(self.login_page)


def main(version):
    """The application's entry point."""
    app = GwardenApplication()
    return app.run(sys.argv)
