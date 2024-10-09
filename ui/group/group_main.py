import logging
from textual.widgets import Static, Digits
from textual.reactive import reactive
from textual.events import Message
from textual.containers import ScrollableContainer

from textual import on

from config import config
from models.group import Group
from repositories.group_repository import GroupRepository
from repositories.host_repository import HostRepository
from services.host_manager import HostsManager
from shared.utils import format_group_name
from ui.about.about_main import AboutMainView
from ui.group.group_form import GroupFormView
from textual.app import ComposeResult

from ui.widgets.box_message import BoxMessage
from ui.widgets.confirmation import Confirmation

WELCOME_MESSAGE = f"""🎉 Welcome to [bold cyan]{config.APP_NAME}[/bold cyan]

👉 Press [bold yellow]a[/bold yellow] to add your first group"""

STATUS_LEGEND = "🟢 active [bold yellow]|[/bold yellow] 🟡 not applied [bold yellow]|[/bold yellow] 🔴 inactive"

class GridBoxItem(Static):
    can_focus = True
    is_selected = reactive(False)

    def __init__(self, index, **kwargs) -> None:
        super().__init__(**kwargs)
        self.index = index

    def watch_is_selected(self, is_selected: bool):
        if is_selected:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    class Selected(Message):
        def __init__(self, group_id, index) -> None:
            super().__init__()
            self.group_id = group_id
            self.index = index

    class Deselected(Message):
        def __init__(self, group_id, index) -> None:
            super().__init__()
            self.group_id = group_id
            self.index = index
        
    def on_focus(self):
        self.is_selected = True
        self.post_message(self.Selected(self.name, self.index))

    def on_blur(self):
        self.is_selected = False
        self.post_message(self.Deselected(self.name, self.index))
        

class GroupsGrid(Static):
    can_focus = True
    items: reactive[list[Group]] = reactive([], recompose=True, init=False)
    
    selected_index: reactive[int] = reactive(0)
    group_selected = None

    class GroupSelected(Message):
        def __init__(self, group) -> None:
            self.group = group
            super().__init__()

    def on_mount(self):
        self.load_groups()

    def compose(self) -> ComposeResult:
        if len(self.items) == 0:
            yield BoxMessage(WELCOME_MESSAGE)
        else :
            with Static(classes="box-grid"):
                for index, item in enumerate(self.items):
                    grid = GridBoxItem(index, name=item.id, classes="box")
                    grid.border_title=format_group_name(item.name, item.hosts_status)
                    with grid:
                        yield Digits(str(item.total_hosts))

        self.call_after_refresh(self.update_selection)

    def update_selection(self):
        if self.items and 0 <= self.selected_index < len(self.items):
            self.box_item_selected = self.items[self.selected_index].id
            self.query(GridBoxItem)[self.selected_index].focus()
        else:
            self.focus()

    def load_groups(self):
        repo = GroupRepository()
        self.items = repo.list_groups()

    @on(GridBoxItem.Selected)
    def handle_item_selected(self, message: GridBoxItem.Selected):
        self.selected_index = message.index
        self.group_selected = self.items[self.selected_index]

    @on(GridBoxItem.Deselected)
    def handle_item_deselected(self, message: GridBoxItem.Deselected):
        self.selected_index = 0
        self.group_selected = None

    def on_key(self, event) -> None:
        columns = 3  # Número de colunas no grid
        if event.key == "up":
            # Movimenta para cima (3 itens de uma vez)
            if self.selected_index - columns >= 0:
                self.selected_index -= columns
                self.update_selection()
        elif event.key == "down":
            # Movimenta para baixo (3 itens de uma vez)
            if self.selected_index + columns < len(self.items):
                self.selected_index += columns
                self.update_selection()
        elif event.key == "left":
            # Movimenta para a esquerda (1 item de cada vez)
            if self.selected_index % columns > 0:  # Certifica-se de que não está na primeira coluna
                self.selected_index -= 1
                self.update_selection()
        elif event.key == "right":
            # Movimenta para a direita (1 item de cada vez)
            if self.selected_index % columns < columns - 1 and self.selected_index < len(self.items) - 1:
                self.selected_index += 1
                self.update_selection()
        elif event.key == "enter":
            if self.group_selected is not None:
                self.post_message(self.GroupSelected(self.group_selected))


class GroupMainView(Static):
    BINDINGS = [
        ("a", "add_group", "add"),
        ("e", "edit_group", "edit"),
        ("r", "remove_group", "remove"),
        ("ctrl+a", "active_group", "active"),
        ("ctrl+d", "disable_group", "disable"),
        ("ctrl+b", "about", "about")
    ]

    groups_grid = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.group_repo = GroupRepository()
        self.host_repo = HostRepository()
        self.host_manager = HostsManager()
    
    def compose(self) -> ComposeResult:
        self.groups_grid = GroupsGrid(classes="groups-grid")
        with ScrollableContainer():
            yield self.groups_grid
            yield Static(STATUS_LEGEND, classes="header")

    # ACTIONS AND HANDLERS
    # create group
    def action_add_group(self) -> None:
        self.app.push_screen(GroupFormView(), self.handle_group_created)

    def handle_group_created(self, has_created: bool) -> None:
        if has_created:
            self.groups_grid.load_groups()

    # update group
    def action_edit_group(self):
        group_selected = self.groups_grid.group_selected
        if group_selected is None:
            return
        self.app.push_screen(GroupFormView(update_group=group_selected), self.handle_group_edited)

    def handle_group_edited(self, has_updated: bool) -> None:
        if has_updated:
            self.groups_grid.load_groups()

    # remove group
    def action_remove_group(self):
        group_selected = self.groups_grid.group_selected
        if group_selected is None:
            return
        
        mConfirm = Confirmation(question=f"Are you sure you want to remove this group?")

        self.app.push_screen(mConfirm, self.handle_removal_confirmation)

    def handle_removal_confirmation(self, info) -> None:
        group_selected = self.groups_grid.group_selected
        if info == "yes":

            if group_selected is None:
                logging.info("No group selected")
                return

            self.group_repo.delete_group(group_selected.id)
            self.host_repo.delete_host_by_group_id(group_selected.id)
            self.host_manager.remove_hosts(group_selected.id)

            self.groups_grid.load_groups()

    # active group
    def action_active_group(self):
        group_selected = self.groups_grid.group_selected
        if group_selected is None:
            return

        if group_selected.hosts_status != "active":
            self.group_repo.update_hosts_status(group_selected.id, "active")
            hosts = self.host_repo.list_hosts_by_group_id(group_selected.id)
            self.host_manager.create_or_replace_hosts(group_id=group_selected.id, group_name=group_selected.name, hosts=hosts)
            self.groups_grid.load_groups()
        else:
            self.app.notify("Group already active", title="Warning", severity="warning")

    def action_disable_group(self):
        group_selected = self.groups_grid.group_selected
        if group_selected is None:
            return

        if group_selected.hosts_status != "inactive":
            self.group_repo.update_hosts_status(group_selected.id, "inactive")
            self.host_manager.remove_hosts(group_selected.id)
            self.groups_grid.load_groups()
        else:
            self.app.notify("Group already inactive", title="Warning", severity="warning")

    def action_about(self):
        self.app.push_screen(AboutMainView())
