from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Footer

from config import config
from shared.utils import check_permissions_hosts
from ui.group.group_main import GroupMainView, GroupsGrid
from ui.host.host_main import HostMainView
from textual import on

from ui.widgets.alert import Alert

class HostControlApp(App):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "app.css"

    box_main = None

    def validation_permissions(self) -> None:
        message, is_ok = check_permissions_hosts()
        if is_ok == False:
            self.app.push_screen(Alert(title="[bold red]ATTENTION![/bold red]", message=message))

    def on_mount(self) -> None:
        self.title = config.APP_NAME
        self.sub_title = config.APP_VERSION
        self.validation_permissions()

    def compose(self) -> ComposeResult:
        self.box_main = VerticalScroll()
        
        yield Header(show_clock=False, name="Header", icon="🌐", classes="app-header")
        with self.box_main:
            yield GroupMainView()
        yield Footer()

    @on(GroupsGrid.GroupSelected)
    def group_selected(self, event) -> None:
        self.box_main.remove_children()
        self.box_main.mount(HostMainView(group_id=event.group.id))

    @on(HostMainView.Exit)
    def go_to_main(self, event) -> None:
        self.box_main.remove_children()
        self.box_main.mount(GroupMainView())
           
