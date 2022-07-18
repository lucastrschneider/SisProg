from prog_sys.event_controller import EventController
from prog_sys.loader import Loader
from prog_sys.dumper import Dumper
from prog_sys.gui import ProgSysGUI

if __name__ == "__main__":
    event_controller = EventController()

    event_controller.register_motor(Loader())
    event_controller.register_motor(Dumper())

    gui = ProgSysGUI()

    try:
        gui.start()
    except KeyboardInterrupt:
        gui.stop()
