from typing import Literal

GroupHostsStatus = Literal['active', 'inactive', 'not_applied']

class Group:
    def __init__(self, group_id, created_at, name, hosts_status: GroupHostsStatus, total_hosts=0):
        self.id = group_id
        self.created_at = created_at
        self.name = name
        self.hosts_status = hosts_status
        self.total_hosts = total_hosts

    def __repr__(self):
        return f"Group(id={self.id}, created_at={self.created_at}, name={self.name}, status={self.hosts_status}, total_hosts={self.total_hosts})"
