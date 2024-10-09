import logging
from config import config
from database.migration import run_migrations
from shared.utils import ensure_directory_for_database
from ui.host_control_app import HostControlApp
from textual.logging import TextualHandler

def main() -> None:
    if config.get_app_env() == "development":
        logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])

    ensure_directory_for_database()
    run_migrations()

    app = HostControlApp()
    app.run()

if __name__ == "__main__":
    main()
