"""
Shared base for all RAM installer apps.
Each tier file imports this and calls run() with its constants.
"""
import sys, json, time
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

BG     = "#0a0a0a"
GREEN  = "#00ff88"
GOLD   = "#ffd700"
PANEL  = "#111111"
BORDER = "#1e3a1e"
WHITE  = "#e0e0e0"
GREY   = "#557755"
RED    = "#ff4444"

RAM_FILE = Path.home() / ".dbpff_ram.json"


def load_ram() -> dict:
    try:
        if RAM_FILE.exists():
            return json.loads(RAM_FILE.read_text())
    except Exception:
        pass
    return {"tier": 0, "amount": "none", "spec": "", "date": ""}


def save_ram(tier: int, amount: str, spec: str):
    RAM_FILE.write_text(json.dumps({
        "tier": tier,
        "amount": amount,
        "spec": spec,
        "date": time.strftime("%Y-%m-%d %H:%M"),
    }))


def lbl(text: str, size=14, color=WHITE, bold=False) -> QLabel:
    l = QLabel(text)
    f = QFont("Segoe UI Emoji" if any(ord(c) > 127 for c in text) else "Segoe UI", size)
    f.setBold(bold)
    l.setFont(f)
    l.setAlignment(Qt.AlignCenter)
    l.setStyleSheet(f"color: {color}; background: transparent;")
    l.setWordWrap(True)
    return l


class RAMInstaller(QMainWindow):
    def __init__(self, tier: int, amount: str, spec: str, full_name: str):
        super().__init__()
        self.tier = tier
        self.amount = amount
        self.spec = spec

        self.steps = [
            "Preparing download servers...",
            f"Materializing {amount} of RAM...",
            "Bypassing laws of physics...",
            "Cooling to -274 K...",
            "Allocating memory addresses...",
            "Installing RAM drivers...",
            "Verifying installation...",
            "Complete!",
        ]

        self.setWindowTitle(f"RAM Installer — {amount}")
        self.setMinimumSize(500, 340)
        self.resize(500, 340)
        self.setStyleSheet(
            f"QWidget {{ background: {BG}; color: {WHITE}; font-family: 'Segoe UI', sans-serif; }}"
        )

        current = load_ram()

        if current["tier"] > tier:
            self._show_worse(current)
        elif current["tier"] == tier:
            self._show_same(current)
        else:
            self._show_download()

    # ── Already have better ──────────────────────────────────────
    def _show_worse(self, current):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter)
        v.setSpacing(14)
        v.setContentsMargins(40, 30, 40, 30)

        v.addWidget(lbl("⛔", 56))
        v.addWidget(lbl("You already have better RAM!", 18, WHITE, bold=True))
        v.addWidget(lbl(f"Your RAM:      {current['amount']}", 14, GREEN))
        v.addWidget(lbl(f"This package:  {self.amount}", 14, GREY))
        v.addWidget(lbl("Downgrade not allowed. Keep your superior RAM.", 11, GREY))

        btn = QPushButton("Close")
        btn.setFixedWidth(130)
        btn.clicked.connect(self.close)
        btn.setStyleSheet(
            f"QPushButton {{ background: #2a0d0d; color: {RED}; border: none; "
            f"padding: 8px 16px; border-radius: 4px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: #3a1111; }}"
        )
        v.addWidget(btn, alignment=Qt.AlignCenter)
        self.setCentralWidget(w)

    # ── Already have same ────────────────────────────────────────
    def _show_same(self, current):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter)
        v.setSpacing(14)
        v.setContentsMargins(40, 30, 40, 30)

        v.addWidget(lbl("✅", 56))
        v.addWidget(lbl(f"{self.amount} already installed!", 18, GREEN, bold=True))
        v.addWidget(lbl(self.spec, 12, GREY))
        v.addWidget(lbl(f"Installed: {current.get('date', '—')}", 11, GREY))

        btn = QPushButton("Close")
        btn.setFixedWidth(130)
        btn.clicked.connect(self.close)
        btn.setStyleSheet(
            f"QPushButton {{ background: {PANEL}; color: {GREEN}; border: 1px solid {BORDER}; "
            f"padding: 8px 16px; border-radius: 4px; font-weight: bold; }}"
        )
        v.addWidget(btn, alignment=Qt.AlignCenter)
        self.setCentralWidget(w)

    # ── Download / upgrade ───────────────────────────────────────
    def _show_download(self):
        self._step = 0
        self._prog = 0

        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(40, 25, 40, 25)
        v.setSpacing(10)

        v.addWidget(lbl(f"⬇  Downloading {self.amount} of RAM", 19, GREEN, bold=True))
        v.addWidget(lbl(self.spec, 12, GREY))
        v.addSpacing(10)

        self._status = lbl("Initializing...", 13, WHITE)
        v.addWidget(self._status)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(10)
        self._bar.setStyleSheet(
            f"QProgressBar {{ background: #0a1a0a; border: 1px solid {BORDER}; border-radius: 5px; }}"
            f"QProgressBar::chunk {{ background: {GREEN}; border-radius: 4px; }}"
        )
        v.addWidget(self._bar)

        self._pct = lbl("0%", 11, GREY)
        v.addWidget(self._pct)

        self.setCentralWidget(w)

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(70)

    def _tick(self):
        target = int((self._step + 1) * 100 / len(self.steps))
        if self._prog < min(target, 100):
            self._prog += 1
            self._bar.setValue(self._prog)
            self._pct.setText(f"{self._prog}%")
        else:
            self._step += 1
            if self._step < len(self.steps):
                self._status.setText(self.steps[self._step])
            if self._step >= len(self.steps):
                self._timer.stop()
                save_ram(self.tier, self.amount, self.spec)
                self._show_success()

    # ── Success ──────────────────────────────────────────────────
    def _show_success(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter)
        v.setSpacing(14)
        v.setContentsMargins(40, 30, 40, 30)

        v.addWidget(lbl("✅", 56))
        v.addWidget(lbl(f"{self.amount} installed!", 22, GREEN, bold=True))
        v.addWidget(lbl(self.spec, 12, GREY))
        v.addWidget(lbl("Restart your PC to feel the RAM.", 11, GREY))

        btn = QPushButton("Close")
        btn.setFixedWidth(130)
        btn.clicked.connect(self.close)
        btn.setStyleSheet(
            f"QPushButton {{ background: #0d3320; color: {GREEN}; border: none; "
            f"padding: 8px 16px; border-radius: 4px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: #0f4428; }}"
        )
        v.addWidget(btn, alignment=Qt.AlignCenter)
        self.setCentralWidget(w)


def run(tier: int, amount: str, spec: str, full_name: str):
    app = QApplication(sys.argv)
    win = RAMInstaller(tier, amount, spec, full_name)
    win.show()
    sys.exit(app.exec())
