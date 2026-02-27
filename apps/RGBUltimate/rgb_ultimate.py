#!/usr/bin/env python3
"""
RGB Ultimare
DownloadBetterPerformanceForFree — RGB Everything. Even Things That Shouldn't Be.
"""

import sys, os, json, math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QSlider, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor

DARK = "#0a0a0a"
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".rgbultimate_settings.json")

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

PATTERNS = [
    "Rainbow Cycle",
    "Breathing",
    "Wave",
    "Solid Color",
    "Chaos",
    "π-Mode",
    "Epilepsy Speedrun %",
]

# ── Persistence ───────────────────────────────────────────────────────────────
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

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

def device_color(device_idx, tick, pattern, brightness, num_devices):
    """Return a QColor for a device given current animation state."""
    offset = device_idx * (360 // num_devices)
    h = tick % 360

    if pattern == "Rainbow Cycle":
        hue = (h + offset) % 360
        return QColor.fromHsv(hue, 255, brightness)

    elif pattern == "Breathing":
        # sin-based brightness pulse, offset per device
        phase = (tick * 0.06 + device_idx * 0.5) % (2 * math.pi)
        v = int((math.sin(phase) * 0.5 + 0.5) * brightness)
        return QColor.fromHsv((h + offset) % 360, 220, max(20, v))

    elif pattern == "Wave":
        # hue wave that propagates across devices
        hue = (h + device_idx * 30) % 360
        return QColor.fromHsv(hue, 255, brightness)

    elif pattern == "Solid Color":
        # All devices same hue, slowly rotating
        return QColor.fromHsv(h, 200, brightness)

    elif pattern == "Chaos":
        import random
        hue = random.randint(0, 359)
        sat = random.randint(180, 255)
        return QColor.fromHsv(hue, sat, brightness)

    elif pattern == "π-Mode":
        # Hue steps through π-related values
        pi_hues = [114, 228, 57, 171, 285, 99, 213, 42, 156, 270]
        hue = pi_hues[device_idx % len(pi_hues)]
        phase = (tick * 0.04 + device_idx) % (2 * math.pi)
        v = int((math.sin(phase) * 0.4 + 0.6) * brightness)
        return QColor.fromHsv(hue, 255, max(30, v))

    elif pattern == "Epilepsy Speedrun %":
        # Flashing between fully saturated complementary colors
        flip = (tick // 2 + device_idx) % 2
        hue = (h * 2 + device_idx * 37) % 360 if flip else (h * 3 + device_idx * 73 + 180) % 360
        return QColor.fromHsv(hue, 255, brightness)

    return QColor.fromHsv((h + offset) % 360, 255, brightness)


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

        box = QFrame()
        box.setObjectName("warn_box")
        box.setStyleSheet(
            "#warn_box { background:#120000; border:2px solid #ff4444; border-radius:14px; }")
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
        txt.setStyleSheet("color:#bb7777; background:transparent;")
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
        self._tick    = 0
        self._speed   = 3
        self._bright  = 200
        self._ultra   = False
        self._timer   = QTimer()
        self._timer.timeout.connect(self._on_tick)

        settings = load_settings()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
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

        # Body
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # Left — device list
        left = QWidget()
        left.setFixedWidth(310)
        self._left_widget = left
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

        # Right
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

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
        ctrl.setFixedHeight(165)
        ctrl.setStyleSheet("background:#080808;")
        cl = QVBoxLayout(ctrl)
        cl.setContentsMargins(24, 14, 24, 14)
        cl.setSpacing(8)

        row1 = QHBoxLayout(); row1.setSpacing(20)

        # Speed
        sp_col = QVBoxLayout(); sp_col.setSpacing(4)
        sp_col.addWidget(label("SPEED", 8, color="#2a2a2a", mono=True))
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(1, 20)
        self._slider.setValue(settings.get("speed", 3))
        self._speed = self._slider.value()
        self._slider.valueChanged.connect(self._on_speed)
        sp_col.addWidget(self._slider)
        row1.addLayout(sp_col)

        # Brightness
        br_col = QVBoxLayout(); br_col.setSpacing(4)
        br_col.addWidget(label("BRIGHTNESS", 8, color="#2a2a2a", mono=True))
        self._br_slider = QSlider(Qt.Horizontal)
        self._br_slider.setRange(10, 255)
        self._br_slider.setValue(settings.get("brightness", 200))
        self._bright = self._br_slider.value()
        self._br_slider.valueChanged.connect(self._on_bright)
        br_col.addWidget(self._br_slider)
        row1.addLayout(br_col)

        # Pattern
        pt_col = QVBoxLayout(); pt_col.setSpacing(4)
        pt_col.addWidget(label("PATTERN", 8, color="#2a2a2a", mono=True))
        self._pattern = QComboBox()
        for p in PATTERNS:
            self._pattern.addItem(p)
        saved_pat = settings.get("pattern", 0)
        self._pattern.setCurrentIndex(saved_pat)
        self._pattern.currentIndexChanged.connect(self._on_pattern)
        pt_col.addWidget(self._pattern)
        row1.addLayout(pt_col)

        cl.addLayout(row1)

        row2 = QHBoxLayout(); row2.setSpacing(12); row2.addStretch()

        self._ultra_btn = QPushButton("⚡  ULTRA MODE")
        self._ultra_btn.setStyleSheet(
            "background:#1a0a00;color:#ff6600;border:1px solid #ff6600;"
            "border-radius:8px;font-size:14px;font-weight:900;padding:10px 28px;")
        self._ultra_btn.setCursor(Qt.PointingHandCursor)
        self._ultra_btn.clicked.connect(self._toggle_ultra)

        row2.addWidget(self._ultra_btn); row2.addStretch()
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

    # ── Slots ─────────────────────────────────────────────────────────────────
    def _on_speed(self, v):
        self._speed = v
        if not self._ultra:
            self._save()

    def _on_bright(self, v):
        self._bright = v
        self._save()

    def _on_pattern(self, idx):
        self._save()

    def _save(self):
        save_settings({
            "speed":      self._slider.value(),
            "brightness": self._br_slider.value(),
            "pattern":    self._pattern.currentIndex(),
        })

    # ── Animation ─────────────────────────────────────────────────────────────
    def _on_tick(self):
        self._tick += self._speed
        t    = self._tick
        pat  = self._pattern.currentText()
        br   = self._bright
        n    = len(DEVICES)

        # Preview background (use device 0 color)
        bg  = device_color(0, t, pat, min(br, 180), n)
        txt = device_color(0, t + 180, pat, 255, n)
        self._preview.setStyleSheet(f"background:{bg.name()};")
        self._big_rgb.setStyleSheet(
            f"background:transparent; color:{txt.name()};"
            f"font-size:80px; font-weight:900;")

        # Title hue
        tc = device_color(0, t, pat, 255, n)
        self._title.setStyleSheet(f"background:transparent; color:{tc.name()};")

        # Device dots
        for i, dot in enumerate(self._dots):
            dc = device_color(i, t, pat, 255, n)
            dot.setStyleSheet(f"background:transparent; color:{dc.name()};")

        # Ultra: left panel bg + preview subtitle pulse
        if self._ultra:
            lbg = device_color(0, t, pat, 20, n)
            self._left_widget.setStyleSheet(f"background:{lbg.name()};")
            pbg = device_color(2, t, pat, 255, n)
            self._preview_sub.setStyleSheet(f"background:transparent; color:{pbg.name()};")
            hbg = device_color(1, t, pat, 25, n)
            self._header.setStyleSheet(f"background:{hbg.name()};")
        else:
            self._header.setStyleSheet("background:#0a0a0a;")

    def _toggle_ultra(self):
        self._ultra = not self._ultra
        if self._ultra:
            self._timer.setInterval(16)
            self._slider.setValue(20); self._speed = 20
            self._ultra_btn.setText("💀  ULTRA MODE  [ON]")
            self._ultra_btn.setStyleSheet(
                "background:#ff4400;color:#fff;border:none;"
                "border-radius:8px;font-size:14px;font-weight:900;padding:10px 28px;")
            self._ultra_msg.setText(
                "WARNING: ULTRA MODE ACTIVE — PC may achieve sentience — Putlin is watching")
        else:
            self._timer.setInterval(50)
            saved = load_settings()
            self._slider.setValue(saved.get("speed", 3))
            self._speed = self._slider.value()
            self._ultra_btn.setText("⚡  ULTRA MODE")
            self._ultra_btn.setStyleSheet(
                "background:#1a0a00;color:#ff6600;border:1px solid #ff6600;"
                "border-radius:8px;font-size:14px;font-weight:900;padding:10px 28px;")
            self._ultra_msg.setText("")
            self._header.setStyleSheet("background:#0a0a0a;")
            self._left_widget.setStyleSheet("background:#080808;")

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
