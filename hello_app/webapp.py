# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from . import view  # For import side-effects of setting up routes.
# import threading
# from view import poll_server

# poop = threading.Thread(target = poll_server, daemon=True)
# poop.start()

