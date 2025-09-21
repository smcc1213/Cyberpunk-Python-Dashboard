from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtWidgets import QTextEdit
import re

class LogHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Suspicious file extensions
        domain_format = QTextCharFormat()
        domain_format.setForeground(QColor("#ff6600"))  # neon orange
        domain_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append(
            (re.compile(r"\.(exe|scr|zip|rar|bat|cmd|dll)\b", re.IGNORECASE), domain_format)
        )

        # Suspicious domains
        tld_format = QTextCharFormat()
        tld_format.setForeground(QColor("#ff3333"))  # neon red
        tld_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append(
            (re.compile(r"\.(ru|cn|tk|top|xyz)\b", re.IGNORECASE), tld_format)
        )

        # Bad protocols
        proto_format = QTextCharFormat()
        proto_format.setForeground(QColor("#ffff33"))  # neon yellow
        proto_format.setFontWeight(QFont.Bold)
        for word in ["telnet", "ftp", "smb", "rdp", "vnc"]:
            self.highlighting_rules.append((re.compile(rf"\b{word}\b", re.IGNORECASE), proto_format))

        # Keywords
        alert_format = QTextCharFormat()
        alert_format.setForeground(QColor("#ff00ff"))  # magenta
        alert_format.setFontWeight(QFont.Bold)
        for word in ["ALERT", "MALWARE", "C2", "EXPLOIT", "SHELL", "PAYLOAD", "FAILED"]:
            self.highlighting_rules.append((re.compile(rf"\b{word}\b", re.IGNORECASE), alert_format))

        # IPs
        ip_format = QTextCharFormat()
        ip_format.setForeground(QColor("#00ffff"))  # cyan
        self.highlighting_rules.append(
            (re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"), ip_format)
        )

        # Ports
        port_format = QTextCharFormat()
        port_format.setForeground(QColor("#39ff14"))  # neon green
        self.highlighting_rules.append(
            (re.compile(r":\d{2,5}\b"), port_format)
        )

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)

class LogHighlighterWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #111; color: #ff3333; border: 2px solid #00ffcc;")
        self.setFont(QFont("Courier", 10))
        self.highlighter = LogHighlighter(self.document())
