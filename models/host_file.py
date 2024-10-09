class HostFile:
    def __init__(self, host_id, ip_address, hostname, created_at, group_id=None):
        self.id = host_id
        self.ip_address = ip_address
        self.hostname = hostname
        self.created_at = created_at
        self.group_id = group_id

    def __repr__(self):
        return (f"HostsFile(id={self.id}, ip_address={self.ip_address}, "
                f"hostname={self.hostname}, created_at={self.created_at}, "
                f"group_id={self.group_id})")
