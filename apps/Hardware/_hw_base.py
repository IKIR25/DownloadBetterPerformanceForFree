"""
Shared base for GPU, CPU, Storage hardware installers.
Each component file calls run() with its constants.
"""
import sys, json, time
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

BG    = "#0a0a0a"
PANEL = "#111111"
WHITE = "#e0e0e0"
GREY  = "#557755"
RED   = "#ff4444"


def hw_file(hw_type: str) -> Path:
    return Path.home() / f".dbpff_{hw_type}.json"


def load_hw(hw_type: str) -> dict:
    try:
        f = hw_file(hw_type)
        if f.exists():
            return json.loads(f.read_text())
    except Exception:
        pass
    return {"tier": 0, "name": "none", "spec": "", "date": ""}


def save_hw(hw_type: str, tier: int, name: str, spec: str):
    hw_file(hw_type).write_text(json.dumps({
        "tier": tier,
        "name": name,
        "spec": spec,
        "date": time.strftime("%Y-%m-%d %H:%M"),
    }))


def lbl(text: str, size=14, color=WHITE, bold=False) -> QLabel:
    l = QLabel(text)
    f = QFont("Segoe UI", size)
    f.setBold(bold)
    l.setFont(f)
    l.setAlignment(Qt.AlignCenter)
    l.setStyleSheet(f"color: {color}; background: transparent;")
    l.setWordWrap(True)
    return l


class HWInstaller(QMainWindow):
    def __init__(self, hw_type: str, tier: int, name: str,
                 spec: str, full_name: str, color: str, steps: list):
        super().__init__()
        self.hw_type  = hw_type
        self.tier     = tier
        self.name     = name
        self.spec     = spec
        self.color    = color
        self.steps    = steps

        self.setWindowTitle(f"Hardware Installer — {name}")
        self.setMinimumSize(520, 350)
        self.resize(520, 350)
        self.setStyleSheet(
            f"QWidget {{ background: {BG}; color: {WHITE}; font-family: 'Segoe UI', sans-serif; }}"
        )

        current = load_hw(hw_type)

        if current["tier"] > tier:
            self._show_worse(current)
        elif current["tier"] == tier:
            self._show_same(current)
        else:
            self._show_download()

    # ── Already have better ──────────────────────────────────────
    def _show_worse(self, current):
        w = QWidget(); v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter); v.setSpacing(14)
        v.setContentsMargins(40, 30, 40, 30)

        v.addWidget(lbl("⛔", 56))
        v.addWidget(lbl("You already have better hardware!", 18, WHITE, bold=True))
        v.addWidget(lbl(f"Your component:  {current['name']}", 14, self.color))
        v.addWidget(lbl(f"This package:    {self.name}", 14, GREY))
        v.addWidget(lbl("Downgrade not allowed. Keep your superior hardware.", 11, GREY))

        btn = QPushButton("Close"); btn.setFixedWidth(130)
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
        w = QWidget(); v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter); v.setSpacing(14)
        v.setContentsMargins(40, 30, 40, 30)

        v.addWidget(lbl("✅", 56))
        v.addWidget(lbl(f"{self.name} already installed!", 18, self.color, bold=True))
        v.addWidget(lbl(self.spec, 12, GREY))
        v.addWidget(lbl(f"Installed: {current.get('date', '—')}", 11, GREY))

        btn = QPushButton("Close"); btn.setFixedWidth(130)
        btn.clicked.connect(self.close)
        btn.setStyleSheet(
            f"QPushButton {{ background: {PANEL}; color: {self.color}; "
            f"border: 1px solid {self.color}44; padding: 8px 16px; "
            f"border-radius: 4px; font-weight: bold; }}"
        )
        v.addWidget(btn, alignment=Qt.AlignCenter)
        self.setCentralWidget(w)

    # ── Download ─────────────────────────────────────────────────
    def _show_download(self):
        self._step = 0; self._prog = 0

        w = QWidget(); v = QVBoxLayout(w)
        v.setContentsMargins(40, 25, 40, 25); v.setSpacing(10)

        v.addWidget(lbl(f"⬇  Downloading {self.name}", 19, self.color, bold=True))
        v.addWidget(lbl(self.spec, 12, GREY))
        v.addSpacing(10)

        self._status = lbl("Initializing...", 13, WHITE)
        v.addWidget(self._status)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100); self._bar.setValue(0)
        self._bar.setTextVisible(False); self._bar.setFixedHeight(10)
        self._bar.setStyleSheet(
            f"QProgressBar {{ background: #0a0a14; border: 1px solid {self.color}33; border-radius: 5px; }}"
            f"QProgressBar::chunk {{ background: {self.color}; border-radius: 4px; }}"
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
                save_hw(self.hw_type, self.tier, self.name, self.spec)
                self._show_success()

    # ── Success ──────────────────────────────────────────────────
    def _show_success(self):
        w = QWidget(); v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignCenter); v.setSpacing(14)
        v.setContentsMargins(40, 30, 40, 30)

        v.addWidget(lbl("✅", 56))
        v.addWidget(lbl(f"{self.name} installed!", 22, self.color, bold=True))
        v.addWidget(lbl(self.spec, 12, GREY))
        v.addWidget(lbl("Restart your PC to feel the hardware.", 11, GREY))

        btn = QPushButton("Close"); btn.setFixedWidth(130)
        btn.clicked.connect(self.close)
        btn.setStyleSheet(
            f"QPushButton {{ background: {PANEL}; color: {self.color}; border: none; "
            f"padding: 8px 16px; border-radius: 4px; font-weight: bold; }}"
            f"QPushButton:hover {{ opacity: 0.8; }}"
        )
        v.addWidget(btn, alignment=Qt.AlignCenter)
        self.setCentralWidget(w)


def run(hw_type: str, tier: int, name: str, spec: str,
        full_name: str, color: str, steps: list):
    app = QApplication(sys.argv)
    win = HWInstaller(hw_type, tier, name, spec, full_name, color, steps)
    win.show()
    sys.exit(app.exec())
