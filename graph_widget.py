from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import psutil

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Setup figure with black background
        self.figure = Figure(facecolor="#000000")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)

        # Store historical data
        self.data_sent = [0] * 20
        self.data_recv = [0] * 20
        self.last_io = psutil.net_io_counters()  # initial reading

        # Initial draw
        self.update_graph()

        # Auto-refresh every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(5000)

    def update_graph(self):
        # Get current network I/O
        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent - self.last_io.bytes_sent
        recv = net_io.bytes_recv - self.last_io.bytes_recv
        self.last_io = net_io  # update baseline

        # Append new values and trim old ones
        self.data_sent.append(sent)
        self.data_recv.append(recv)
        self.data_sent.pop(0)
        self.data_recv.pop(0)

        # Clear and redraw
        self.ax.clear()
        self.ax.set_facecolor("#111111")

        # Plot two lines: Sent (pink), Received (cyan)
        self.ax.plot(self.data_sent, color="#ff00ff", linewidth=2, label="Sent")
        self.ax.plot(self.data_recv, color="#00ffcc", linewidth=2, label="Received")

        # Set labels and title in theme
        self.ax.set_title("System Network Traffic", color="#ff00ff", fontsize=12, fontweight="bold")
        self.ax.set_xlabel("Time (5s intervals)", color="#ff6600", fontsize=10, fontweight="bold")
        self.ax.set_ylabel("Bytes", color="#ff6600", fontsize=10, fontweight="bold")

        # Style ticks and grid
        self.ax.tick_params(colors="#00ffcc", labelsize=8)
        self.ax.grid(True, color="#00ffcc", linestyle="--", alpha=0.4)

        # Legend
        self.ax.legend(facecolor="#111111", edgecolor="#00ffcc", labelcolor="#00ffcc")

        self.canvas.draw()
