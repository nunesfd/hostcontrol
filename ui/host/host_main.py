from textual.app import ComposeResult
from textual.widgets import Static, Label, ListView, ListItem, Rule
from textual.containers import ScrollableContainer, Horizontal

from models.group import Group
from repositories.group_repository import GroupRepository
from repositories.host_repository import HostRepository
from services.host_manager import HostsManager
from shared.utils import format_group_name
from ui.host.host_form import HostFormView
from textual.events import Message
from textual.reactive import reactive
from textual.binding import Binding

from ui.widgets.box_message import BoxMessage
from ui.widgets.confirmation import Confirmation

EMPTY_HOSTS_MESSAGE = "👉 Press [bold yellow]a[/bold yellow] to add your first host"
APPLY_HOSTS_MESSAGE="⚠️  Press [bold yellow]ctrl+a[/bold yellow] to apply these changes in hosts file"
ACTIVE_HOSTS_MESSAGE="⚠️  Press [bold yellow]ctrl+a[/bold yellow] to apply and activate this group in hosts file"

class HostMainView(Static):

    class Exit(Message):
        pass

    group_id = 0
    group: Group = None
    list_view = None
    host_selected_id = None
    hosts = reactive([], init=False, recompose=True)

    def __init__(self, group_id=None, **kwargs) -> None:
        super().__init__(**kwargs)  # Chama o construtor da classe pai com os argumentos
        self.can_focus = True
        
        self.group_repo = GroupRepository()
        self.host_repo = HostRepository()
        self.host_manager = HostsManager()

        self.group_id = group_id
        self.load_group_info()
        self.load_hosts()

    BINDINGS = [
        ("a", "add_host", "add"),
        ("e", "edit_host", "edit"),
        ("r", "remove_host", "remove"),
        Binding("escape", "exit", "go back", show=False),
        Binding("ctrl+a", "apply_hosts", "apply", show=False)
    ]

    def update_selection(self):
        self.list_view.focus()
        # self.list_view.action_select_cursor()

    async def on_list_view_highlighted(self, message: ListView.Highlighted) -> None:
        self.host_selected_id = message.item.name

    def compose(self) -> ComposeResult:
        title = format_group_name(self.group.name, self.group.hosts_status)
        self.list_view = None
        
        yield Label(f"{title} - ({self.group.total_hosts})", classes="app-title")
        yield Rule(line_style="dashed")

        with ScrollableContainer():
            if len(self.hosts) == 0:
                yield BoxMessage(EMPTY_HOSTS_MESSAGE)
                self.call_after_refresh(self.focus)
            else:
                self.list_view = ListView(classes="list-hosts")
                with self.list_view:
                    for row in self.hosts:
                        yield ListItem(
                            Horizontal(
                                Label(row.ip_address, classes="ip-address"),
                                Label(row.hostname, classes="host-name"),
                            ),
                            name=row.id,
                        )
                if self.group.hosts_status == "not_applied":
                    yield Static(APPLY_HOSTS_MESSAGE, classes="apply-hosts")
                
                if self.group.hosts_status == "inactive":
                    yield Static(ACTIVE_HOSTS_MESSAGE, classes="apply-hosts")
                self.call_after_refresh(self.update_selection)  
    
    def sync_hosts(self):
        self.group_repo.update_hosts_status(self.group_id, "not_applied")
        self.load_group_info()
        self.load_hosts()

    # ACTIONS AND HANDLERS
    # add host
    def action_add_host(self) -> None:
        self.app.push_screen(HostFormView(group_id=self.group.id, group_name=self.group.name), self.handle_host_created_or_updated)

    def handle_host_created_or_updated(self, has_created: bool) -> None:
        if has_created is True:
            self.sync_hosts()

    # update host
    def action_edit_host(self) -> None:
        if self.host_selected_id is None:
            return None

        self.app.push_screen(
            HostFormView(
                group_id=self.group_id, 
                group_name=self.group.name, 
                update_id=self.host_selected_id
            ), 
        self.handle_host_created_or_updated)

    def action_apply_hosts(self):
        self.host_manager.create_or_replace_hosts(int(self.group_id), self.group.name, self.hosts)

        self.group_repo.update_hosts_status(self.group_id, "active")
        self.load_group_info()
        self.load_hosts()
        self.app.notify("Hosts applied", title="Success", severity="information")

    def action_exit(self):
        self.post_message(self.Exit())    

    def action_remove_host(self) -> None:
        if self.host_selected_id is None:
            return None
        
        mConfirm = Confirmation(question=f"Are you sure you want to remove this host?")
        self.app.push_screen(mConfirm, self.handle_removal_confirmation)

    def handle_removal_confirmation(self, info):
        if info == "yes":
            self.delete_host_db(self.host_selected_id)
            self.sync_hosts()

    # delete host db
    def delete_host_db(self, host_id):
        try:
            self.host_repo.delete_host(host_id)
            self.group_repo.update_total_hosts(self.group_id)
        except Exception as e:
            self.app.notify(title="Error", message=f"Error on delete host: {str(e)}", severity="error")

    def load_group_info(self):
        self.group = self.group_repo.get_group_by_id(self.group_id)

    def load_hosts(self):
        self.hosts = self.host_repo.list_hosts_by_group_id(self.group_id)
        