import sys

from IPython.external.qt_for_kernel import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication
from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea


import asyncio

from golem_garden.golems.golem import Golem

class CustomMainWindow(QMainWindow):
    def __init__(self, dark_mode=True):
        super().__init__()
        central_dock_area = DockArea()

        # Create the Jupyter console widget (and dock)
        self.jupyter_console_widget = CustomJupyterWidget()
        jupyter_console_dock = Dock("Jupyter Console Dock")
        jupyter_console_dock.addWidget(self.jupyter_console_widget)
        central_dock_area.addDock(jupyter_console_dock)

        # Create the plot widget (and dock)
        self.plot_widget = pg.PlotWidget()
        plot_dock = Dock(name="Plot Widget Dock", closable=True)
        plot_dock.addWidget(self.plot_widget)
        central_dock_area.addDock(plot_dock)

        self.setCentralWidget(central_dock_area)

        app = QtWidgets.QApplication.instance()
        app.aboutToQuit.connect(self.jupyter_console_widget.shutdown_kernel)

        kernel = self.jupyter_console_widget.kernel_manager.kernel
        kernel.shell.push(dict(np=np, pw=self.plot_widget))

        # Set dark mode
        if dark_mode:
            self.jupyter_console_widget.set_default_style("linux")

class CustomJupyterWidget(RichJupyterWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute_on_complete_input = False
        self.golem = Golem(user_id="UnknownUser", session_id="CLI-Qt")

        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

    def _handle_execute_reply(self, msg) -> None:
        """Handle the execution reply from the kernel."""
        super()._handle_execute_reply(msg)
        # Process Golem's response here

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle key press events."""
        if event.type() == QtCore.QEvent.KeyPress and obj is self._control:
            key = event.key()
            # Detect when the user presses the Enter or Return key
            if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
                user_input = self.input_buffer
                if user_input.lower() in ["quit", "exit"]:
                    self.kernel_client.stop_channels()
                    self.kernel_manager.shutdown_kernel()
                    self.close()
                    return True

                if user_input.startswith("!"):  # Check for the special character
                    self.execute(user_input[1:])  # Execute the user input without the special character as a command
                else:
                    self.execute(f"print('{user_input}')")

                response = asyncio.run(self.golem.chat(user_input))
                self._append_plain_text(f"{self.golem.name}: {response}\n", True)
                self.input_buffer = ''
                return True
        return super().eventFilter(obj, event)

    # def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
    #     """Handle key press events."""
    #     if event.type() == QtCore.QEvent.KeyPress and obj is self._control:
    #         key = event.key()
    #         # Detect when the user presses the Enter or Return key
    #         if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
    #             user_input = self.input_buffer
    #             if user_input.lower() in ["quit", "exit"]:
    #                 self.kernel_client.stop_channels()
    #                 self.kernel_manager.shutdown_kernel()
    #                 self.close()
    #                 return True
    #
    #             self.execute(user_input)  # Execute the user input as a command
    #             response = asyncio.run(self.golem.chat(user_input))
    #             self._append_plain_text(f"{self.golem.name}: {response}\n", True)
    #             self.input_buffer = ''
    #             return True
    #     return super().eventFilter(obj, event)

    # def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
    #     """Handle key press events."""
    #     if event.type() == QtCore.QEvent.KeyPress and obj is self._control:
    #         key = event.key()
    #         # Detect when the user presses the Enter or Return key
    #         if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
    #             user_input = self.input_buffer
    #             if user_input.lower() in ["quit", "exit"]:
    #                 self.kernel_client.stop_channels()
    #                 self.kernel_manager.shutdown_kernel()
    #                 self.close()
    #                 return True
    #
    #             response = asyncio.run(self.golem.chat(user_input))
    #             self._append_plain_text(f"{self.golem.name}: {response}\n", True)
    #             self.input_buffer = ''
    #             return True
    #     return super().eventFilter(obj, event)

    def shutdown_kernel(self):
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()




def run_qtconsole():
    app = QApplication([])
    main = CustomMainWindow(dark_mode=True)
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_qtconsole()