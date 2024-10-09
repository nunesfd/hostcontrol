-- Criação da tabela groups para armazenar informações sobre grupos
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    name TEXT NOT NULL,
    total_hosts INTEGER DEFAULT (0),
    hosts_status TEXT -- Use 'active', 'inactive', or 'not_applied'
);

-- Criação da tabela hosts_file para armazenar o conteúdo do arquivo /etc/hosts
CREATE TABLE IF NOT EXISTS hosts_file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    hostname TEXT NOT NULL,
    created_at TEXT DEFAULT (DATETIME('now')),
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);
