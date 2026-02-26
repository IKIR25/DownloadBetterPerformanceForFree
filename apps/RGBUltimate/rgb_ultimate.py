#!/usr/bin/env python3
"""
RGB Ultimare
DownloadBetterPerformanceForFree — RGB Everything. Even Things That Shouldn't Be.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QSlider, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor

DARK = "#0a0a0a"

QSS = """
QWidget {
    background-color: #0a0a0a;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}
QLabel { background: transparent; }
QPushButton {
    background-color: #141414;
    color: #e0e0e0;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    font-weight: 700;
    font-size: 13px;
    padding: 10px 24px;
}
QPushButton:hover { border-color: #555; color: #fff; }
QPushButton#accept {
    background: #0d2a0d; color: #00ff88;
    border-color: #00ff88; font-size: 14px; padding: 12px 28px;
}
QPushButton#accept:hover { background: #1a3a1a; }
QPushButton#exit_btn {
    background: #1a0505; color: #ff4444;
    border-color: #ff4444;
}
QPushButton#exit_btn:hover { background: #2a0a0a; }
QSlider::groove:horizontal {
    background: #1a1a1a; height: 4px; border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #666; width: 14px; height: 14px;
    margin: -5px 0; border-radius: 7px;
}
QComboBox {
    background: #111; border: 1px solid #222;
    border-radius: 6px; padding: 6px 12px; color: #666;
}
QComboBox::drop-down { border: none; width: 0; }
QComboBox QAbstractItemView {
    background: #111; border: 1px solid #222; color: #777;
    selection-background-color: #1a1a1a;
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def label(text, size=12, bold=False, color="#e0e0e0", mono=False, align=Qt.AlignLeft):
    lbl = QLabel(text)
    font = QFont("Courier New" if mono else "Segoe UI", size)
    font.setBold(bold)
    lbl.setFont(font)
    lbl.setStyleSheet(f"color: {color}; background: transparent;")
    lbl.setAlignment(align)
    return lbl

def hline(color="#111"):
    f = QFrame(); f.setFrameShape(QFrame.HLine)
    f.setStyleSheet(f"color:{color}; background:{color}; max-height:1px;")
    return f

def vline():
    f = QFrame(); f.setFrameShape(QFrame.VLine)
    f.setStyleSheet("color:#0f0f0f; background:#0f0f0f; max-width:1px;")
    return f

DEVICES = [
    ("🖥️  CPU Cooler",       "Certified RGB"),
    ("🧠  RAM × 4",          "200 TB DDR7"),
    ("🎮  GPU",              "RTX 5090 × 2"),
    ("⌨️  Keyboard",         "MechaniRGB Pro"),
    ("🖱️  Mouse",            "CursorX RGB"),
    ("📡  Wi-Fi Antenna",    "RouterGlow 6E"),
    ("🪑  Chair",             "GamerSeat Pro"),
    ("💡  Room Lighting",    "404 LEDs"),
    ("🔋  Power Supply",     "PiWatt 850W"),
    ("👻  Your Soul",        "Immaterial"),
]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — Disclaimer
# ══════════════════════════════════════════════════════════════════════════════
class DisclaimerPage(QWidget):
    def __init__(self, on_accept, on_exit):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(0)
        lay.addStretch(2)

        # Warning box
        box = QFrame()
        box.setStyleSheet(
            "QFrame { background:#120000; border:2px solid #ff4444; border-radius:14px; }")
        box.setFixedWidth(580)
        bl = QVBoxLayout(box)
        bl.setContentsMargins(40, 36, 40, 36)
        bl.setSpacing(0)

        icon = QLabel("⚠")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFont(QFont("Segoe UI", 44))
        icon.setStyleSheet("color:#ff4444; background:transparent;")
        bl.addWidget(icon)
        bl.addSpacing(10)

        bl.addWidget(label("PHOTOSENSITIVE SEIZURE WARNING", 14, bold=True,
                           color="#ff4444", mono=True, align=Qt.AlignHCenter))
        bl.addSpacing(20)

        # Real warning — kept genuine
        txt = QLabel(
            "This application contains rapidly flashing lights and "
            "rapidly cycling colors that may trigger photosensitive "
            "epileptic seizures in a small percentage of people.\n\n"
            "If you or anyone nearby has a history of epilepsy or "
            "seizures, consult a doctor before using this application.\n\n"
            "Stop immediately and seek medical attention if you experience "
            "dizziness, altered vision, eye or muscle twitching, loss of "
            "awareness, or convulsions."
        )
        txt.setWordWrap(True)
        txt.setAlignment(Qt.AlignCenter)
        txt.setFont(QFont("Segoe UI", 11))
        txt.setStyleSheet("color:#bb7777; background:transparent; line-height:1.7;")
        bl.addWidget(txt)
        bl.addSpacing(20)

        bl.addWidget(hline("#2a0000"))
        bl.addSpacing(14)

        bl.addWidget(label("(The app also does absolutely nothing useful for your PC.)",
                           10, color="#331111", align=Qt.AlignHCenter))
        bl.addSpacing(22)

        btn_row = QHBoxLayout(); btn_row.setSpacing(14)
        btn_row.addStretch()
        eb = QPushButton("✕  Exit"); eb.setObjectName("exit_btn")
        eb.setCursor(Qt.PointingHandCursor); eb.clicked.connect(on_exit)
        ab = QPushButton("✓  I understand — continue"); ab.setObjectName("accept")
        ab.setCursor(Qt.PointingHandCursor); ab.clicked.connect(on_accept)
        btn_row.addWidget(eb); btn_row.addWidget(ab); btn_row.addStretch()
        bl.addLayout(btn_row)

        wrap = QHBoxLayout()
        wrap.addStretch(); wrap.addWidget(box); wrap.addStretch()
        lay.addLayout(wrap)

        lay.addStretch(3)
        lay.addWidget(label("RGB Ultimare — DownloadBetterPerformanceForFree",
                            9, color="#1a1a1a", align=Qt.AlignHCenter))
        lay.addSpacing(10)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — RGB panel
# ══════════════════════════════════════════════════════════════════════════════
class RGBPage(QWidget):
    def __init__(self):
        super().__init__()
        self._hue   = 0
        self._speed = 3
        self._ultra = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._offsets = [i * (360 // len(DEVICES)) for i in range(len(DEVICES))]

        # ── Root layout ───────────────────────────────────────────────────
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────
        self._header = QWidget()
        self._header.setFixedHeight(52)
        hl = QHBoxLayout(self._header)
        hl.setContentsMargins(22, 0, 22, 0)
        self._title = QLabel("🌈  RGB ULTIMARE")
        self._title.setFont(QFont("Segoe UI", 17, QFont.Bold))
        self._title.setStyleSheet("background:transparent; color:#fff;")
        hl.addWidget(self._title)
        hl.addStretch()
        self._hdr_status = label("RGB ACTIVE • 10 devices synced • Reality: distorted",
                                 9, color="#333", mono=True)
        hl.addWidget(self._hdr_status)
        root.addWidget(self._header)
        root.addWidget(hline("#0f0f0f"))

        # ── Body: left + right ────────────────────────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # Left — device list
        left = QWidget()
        left.setFixedWidth(310)
        left.setStyleSheet("background:#080808;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(18, 18, 16, 16)
        ll.setSpacing(0)
        ll.addWidget(label("DETECTED DEVICES", 8, color="#2a2a2a", mono=True))
        ll.addSpacing(12)

        self._dots = []
        for name, spec in DEVICES:
            row = QHBoxLayout(); row.setSpacing(8)
            dot = QLabel("●")
            dot.setFont(QFont("Segoe UI", 13))
            dot.setFixedWidth(20)
            dot.setStyleSheet("background:transparent; color:#ff0000;")
            col = QVBoxLayout(); col.setSpacing(1)
            col.addWidget(label(name, 10, bold=True, color="#777"))
            col.addWidget(label(spec, 8, color="#252525", mono=True))
            row.addWidget(dot)
            row.addLayout(col)
            row.addStretch()
            row.addWidget(label("SYNC", 7, color="#1a2a1a", mono=True))
            ll.addLayout(row)
            ll.addSpacing(10)
            self._dots.append(dot)

        ll.addStretch()
        ll.addWidget(hline("#0f0f0f"))
        ll.addSpacing(8)
        self._dev_footer = label("All 10 devices: ACTIVE", 8, color="#1e1e1e", mono=True)
        ll.addWidget(self._dev_footer)
        ll.addSpacing(4)

        body.addWidget(left)
        body.addWidget(vline())

        # Right — preview + controls
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        # Preview area
        self._preview = QWidget()
        self._preview.setMinimumHeight(220)
        pl = QVBoxLayout(self._preview)
        pl.setAlignment(Qt.AlignCenter)
        pl.setSpacing(4)

        self._big_rgb = QLabel("RGB")
        self._big_rgb.setAlignment(Qt.AlignCenter)
        self._big_rgb.setFont(QFont("Segoe UI", 80, QFont.Bold))
        self._big_rgb.setStyleSheet("background:transparent; color:#fff;")
        pl.addWidget(self._big_rgb)

        self._preview_sub = label("Syncing your reality…", 11, color="#333",
                                  mono=True, align=Qt.AlignHCenter)
        pl.addWidget(self._preview_sub)

        rl.addWidget(self._preview, stretch=1)
        rl.addWidget(hline("#0f0f0f"))

        # Controls
        ctrl = QWidget()
        ctrl.setFixedHeight(150)
        ctrl.setStyleSheet("background:#080808;")
        cl = QVBoxLayout(ctrl)
        cl.setContentsMargins(24, 14, 24, 14)
        cl.setSpacing(10)

        row1 = QHBoxLayout(); row1.setSpacing(28)

        sp_col = QVBoxLayout(); sp_col.setSpacing(4)
        sp_col.addWidget(label("SPEED", 8, color="#2a2a2a", mono=True))
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(1, 20); self._slider.setValue(3)
        self._slider.valueChanged.connect(lambda v: setattr(self, '_speed', v))
        sp_col.addWidget(self._slider)
        row1.addLayout(sp_col)

        pt_col = QVBoxLayout(); pt_col.setSpacing(4)
        pt_col.addWidget(label("PATTERN", 8, color="#2a2a2a", mono=True))
        self._pattern = QComboBox()
        for p in ["Rainbow Cycle", "RGB Pulse", "RGB Chaos",
                  "RGB π-Mode", "Ultra Instinct", "Epilepsy Speedrun %"]:
            self._pattern.addItem(p)
        pt_col.addWidget(self._pattern)
        row1.addLayout(pt_col)
        cl.addLayout(row1)

        row2 = QHBoxLayout(); row2.setSpacing(12); row2.addStretch()
        sync_btn = QPushButton("🔄  Sync All")
        sync_btn.setStyleSheet(
            "background:#111;color:#555;border:1px solid #1e1e1e;"
            "border-radius:8px;padding:8px 18px;font-size:12px;")
        sync_btn.setCursor(Qt.PointingHandCursor)

        self._ultra_btn = QPushButton("⚡  ULTRA MODE")
        self._ultra_btn.setStyleSheet(
            "background:#1a0a00;color:#ff6600;border:1px solid #ff6600;"
            "border-radius:8px;font-size:14px;font-weight:900;padding:10px 28px;")
        self._ultra_btn.setCursor(Qt.PointingHandCursor)
        self._ultra_btn.clicked.connect(self._toggle_ultra)

        row2.addWidget(sync_btn); row2.addWidget(self._ultra_btn); row2.addStretch()
        cl.addLayout(row2)

        self._ultra_msg = label("", 8, color="#ff6600", mono=True, align=Qt.AlignHCenter)
        cl.addWidget(self._ultra_msg)

        rl.addWidget(ctrl)
        body.addWidget(right, stretch=1)
        root.addLayout(body, stretch=1)

        # Footer
        foot = QWidget(); foot.setFixedHeight(26)
        foot.setStyleSheet("background:#050505;")
        fl = QHBoxLayout(foot)
        fl.setContentsMargins(16, 0, 16, 0)
        fl.addWidget(label(
            "RGB Ultimare v3.14  |  DownloadBetterPerformanceForFree"
            "  |  RGB is always the answer  |  Score: 6.28 / 6.28",
            8, color="#191919", mono=True))
        fl.addStretch()
        root.addWidget(foot)

    # ── Animation ─────────────────────────────────────────────────────────────
    def _tick(self):
        self._hue = (self._hue + self._speed) % 360
        h = self._hue

        # Preview background
        bg  = QColor.fromHsv(h, 255, 180)
        txt = QColor.fromHsv((h + 180) % 360, 255, 255)
        self._preview.setStyleSheet(f"background:{bg.name()};")
        self._big_rgb.setStyleSheet(
            f"background:transparent; color:{txt.name()};"
            f"font-size:80px; font-weight:900;")

        # Title
        tc = QColor.fromHsv(h, 200, 255)
        self._title.setStyleSheet(f"background:transparent; color:{tc.name()};")

        # Device dots — each with its own hue offset
        for i, dot in enumerate(self._dots):
            dh  = (h + self._offsets[i]) % 360
            dc  = QColor.fromHsv(dh, 255, 255)
            dot.setStyleSheet(f"background:transparent; color:{dc.name()};")

        # Header background pulse in ultra mode
        if self._ultra:
            hbg = QColor.fromHsv(h, 200, 25)
            self._header.setStyleSheet(f"background:{hbg.name()};")
            pbg = QColor.fromHsv((h + 60) % 360, 255, 160)
            self._preview_sub.setStyleSheet(
                f"background:transparent; color:{pbg.name()};")
        else:
            self._header.setStyleSheet("background:#0a0a0a;")

    def _toggle_ultra(self):
        self._ultra = not self._ultra
        if self._ultra:
            self._timer.setInterval(16)
            self._slider.setValue(15); self._speed = 15
            self._ultra_btn.setText("💀  ULTRA MODE  [ON]")
            self._ultra_btn.setStyleSheet(
                "background:#ff4400;color:#fff;border:none;"
                "border-radius:8px;font-size:14px;font-weight:900;padding:10px 28px;")
            self._ultra_msg.setText(
                "WARNING: ULTRA MODE ACTIVE — PC may achieve sentience — Putlin is watching")
        else:
            self._timer.setInterval(50)
            self._slider.setValue(3); self._speed = 3
            self._ultra_btn.setText("⚡  ULTRA MODE")
            self._ultra_btn.setStyleSheet(
                "background:#1a0a00;color:#ff6600;border:1px solid #ff6600;"
                "border-radius:8px;font-size:14px;font-weight:900;padding:10px 28px;")
            self._ultra_msg.setText("")
            self._header.setStyleSheet("background:#0a0a0a;")

    def start(self):
        self._timer.start(50)

    def stop(self):
        self._timer.stop()


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RGB Ultimare")
        self.setMinimumSize(800, 540)
        self.resize(960, 640)
        self._center()

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._d = DisclaimerPage(self._accept, self.close)
        self._r = RGBPage()
        self._stack.addWidget(self._d)  # 0
        self._stack.addWidget(self._r)  # 1
        self._stack.setCurrentIndex(0)

    def _center(self):
        g = QApplication.primaryScreen().geometry()
        self.move((g.width() - self.width()) // 2,
                  (g.height() - self.height()) // 2)

    def _accept(self):
        self._stack.setCurrentIndex(1)
        self._r.start()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
