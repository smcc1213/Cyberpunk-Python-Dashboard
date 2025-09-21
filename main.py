import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QGridLayout, QPushButton
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFontDatabase, QFont
from dotenv import load_dotenv

from log_highlighter import LogHighlighterWidget
from weather import WeatherWidget
from system_monitor import SystemMonitor
from graph_widget import GraphWidget

# Load .env values
load_dotenv()
USER_NAME = os.getenv("USER_NAME", "Cyberpunk Operator")
ZEEK_LOG_DIR = os.getenv("ZEEK_LOG_DIR", os.path.expanduser("~/zeek_logs"))
ZEEK_INTERFACE = os.getenv("ZEEK_INTERFACE", "eth0")

class CyberpunkDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyberpunk Dashboard")
        self.setStyleSheet("background-color: black;")

        # Load custom font
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Orbitron-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # Base central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # EXIT button (top-left, neon red)
        exit_button = QPushButton("EXIT")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff003c;
                color: black;
                font-weight: bold;
                border: 2px solid #ff003c;
                border-radius: 6px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: black;
                color: #ff003c;
            }
        """)
        exit_button.clicked.connect(self.close)

        # Top bar with exit + stretch (can add other controls later)
        top_bar = QHBoxLayout()
        top_bar.addWidget(exit_button, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        main_layout.addLayout(top_bar)

        # Grid for main content
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(15)

        # Name (center, neon pink)
        name_label = QLabel(USER_NAME)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont(font_family, 30, QFont.Bold))
        name_label.setStyleSheet("color: #ff00ff; text-shadow: 0 0 10px #ff00ff;")
        grid.addWidget(name_label, 0, 0, 1, 3)

        # Date under name
        date_label = QLabel(QDate.currentDate().toString("dddd, MMMM d, yyyy"))
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setFont(QFont(font_family, 14))
        date_label.setStyleSheet("color: #39ff14;")
        grid.addWidget(date_label, 1, 0, 1, 3)

        # Weather (top-right)
        weather_widget = WeatherWidget()
        weather_widget.setStyleSheet("color: #ffff33; font-size: 16px; font-weight: bold;")
        grid.addWidget(weather_widget, 2, 2, alignment=Qt.AlignRight)

        # Ensure log folder exists
        os.makedirs(ZEEK_LOG_DIR, exist_ok=True)

        # Start Zeek logging to log_dir
        self.zeek_process = None
        try:
            self.zeek_process = subprocess.Popen([
                "zeek", "-i", ZEEK_INTERFACE, f"Log::default_logdir={ZEEK_LOG_DIR}"
            ])
        except Exception as e:
            print(f"[ERROR] Failed to start Zeek: {e}")

        # ZEEK Logs section
        self.log_viewer = LogHighlighterWidget()
        self.log_viewer.setMinimumHeight(300)
        zeek_logs_layout = QVBoxLayout()
        zeek_logs_label = QLabel("ZEEK Logs")
        zeek_logs_label.setAlignment(Qt.AlignCenter)
        zeek_logs_label.setStyleSheet("color: #ff6600; font-size: 16px; font-weight: bold;")
        zeek_logs_layout.addWidget(zeek_logs_label)
        zeek_logs_layout.addWidget(self.log_viewer)
        zeek_logs_widget = QWidget()
        zeek_logs_widget.setLayout(zeek_logs_layout)
        zeek_logs_widget.setStyleSheet("""
            QWidget {
                border: 2px solid #00ffcc;
                background-color: #111111;
                border-radius: 6px;
            }
        """)
        grid.addWidget(zeek_logs_widget, 3, 0, 1, 3)

        # Bottom row (System Monitor + Graphs)
        system_monitor = SystemMonitor()
        system_monitor_layout = QVBoxLayout()
        system_label = QLabel("System Monitor")
        system_label.setAlignment(Qt.AlignCenter)
        system_label.setStyleSheet("color: #ff6600; font-size: 16px; font-weight: bold;")
        system_monitor_layout.addWidget(system_label)
        system_monitor_layout.addWidget(system_monitor)
        system_monitor_widget = QWidget()
        system_monitor_widget.setLayout(system_monitor_layout)
        system_monitor_widget.setStyleSheet("""
            QWidget {
                border: 2px solid #00ffcc;
                background-color: #111111;
                border-radius: 6px;
                color: #ff00ff;
            }
        """)
        grid.addWidget(system_monitor_widget, 4, 0, 1, 1)

        graph_widget = GraphWidget()
        graph_layout = QVBoxLayout()
        graph_label = QLabel("Network Graphs")
        graph_label.setAlignment(Qt.AlignCenter)
        graph_label.setStyleSheet("color: #ff6600; font-size: 16px; font-weight: bold;")
        graph_layout.addWidget(graph_label)
        graph_layout.addWidget(graph_widget)
        graph_widget_container = QWidget()
        graph_widget_container.setLayout(graph_layout)
        graph_widget_container.setStyleSheet("""
            QWidget {
                border: 2px solid #00ffcc;
                background-color: #111111;
                border-radius: 6px;
            }
        """)
        grid.addWidget(graph_widget_container, 4, 1, 1, 2)

        main_layout.addLayout(grid)

        self.setCentralWidget(central_widget)
        self.showFullScreen()

        # Auto-refresh logs every 10 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.load_zeek_logs(self.log_viewer))
        self.timer.start(10000)

    def load_zeek_logs(self, log_viewer):
        log_path = os.path.join(ZEEK_LOG_DIR, "conn.log")
        try:
            scroll_bar = log_viewer.verticalScrollBar()
            scroll_pos = scroll_bar.value()

            with open(log_path, "r") as file:
                contents = file.read()
                log_viewer.setPlainText(contents)

            scroll_bar.setValue(scroll_pos)
        except Exception as e:
            log_viewer.setPlainText(f"[ERROR]: {e}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """Ensure Zeek subprocess is killed when dashboard closes."""
        if self.zeek_process:
            try:
                self.zeek_process.terminate()
                self.zeek_process.wait(timeout=5)
            except Exception as e:
                print(f"[WARN] Could not terminate Zeek: {e}")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = CyberpunkDashboard()
    sys.exit(app.exec_())
