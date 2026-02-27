#!/usr/bin/env python3
"""
VirusDeleter Security Extreme 6.2
DownloadBetterPerformanceForFree — Finds Exactly 3.14 Viruses. Always.
"""

import sys, random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

GREEN  = "#00ff88"
RED    = "#ff3333"
ORANGE = "#ff8800"
DARK   = "#0a0a0a"
GOLD   = "#ffd700"

QSS = f"""
QWidget {{
    background-color: {DARK};
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}}
QLabel {{ background: transparent; }}
QPushButton {{
    background-color: {GREEN};
    color: #000;
    border: none;
    border-radius: 8px;
    font-weight: 900;
    font-size: 14px;
    padding: 13px 32px;
}}
QPushButton:hover  {{ background-color: #33ffaa; }}
QPushButton:pressed {{ background-color: #00cc66; }}
QPushButton#danger {{
    background-color: {RED};
    color: #fff;
    font-size: 15px;
    padding: 14px 36px;
}}
QPushButton#danger:hover  {{ background-color: #ff5555; }}
QPushButton#danger:pressed {{ background-color: #cc2222; }}
QPushButton#secondary {{
    background-color: transparent;
    color: #444;
    border: 1px solid #222;
    font-size: 12px;
    padding: 9px 22px;
}}
QPushButton#secondary:hover {{ color: {GREEN}; border-color: {GREEN}; }}
QProgressBar {{
    background-color: #111;
    border: 1px solid #1a3a1a;
    border-radius: 4px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {GREEN}, stop:1 #00cc66);
    border-radius: 4px;
}}
QProgressBar#threat_bar {{
    border-color: #3a1a1a;
}}
QProgressBar#threat_bar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {RED}, stop:1 #cc2200);
}}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def label(text, size=12, bold=False, color="#e0e0e0", mono=False, align=Qt.AlignLeft):
    lbl = QLabel(text)
    f = QFont("Courier New" if mono else "Segoe UI", size)
    f.setBold(bold)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color:{color}; background:transparent;")
    lbl.setAlignment(align)
    return lbl

def hline(col="#111"):
    f = QFrame(); f.setFrameShape(QFrame.HLine)
    f.setStyleSheet(f"color:{col}; background:{col}; max-height:1px;")
    return f

# ── Fake scan data ────────────────────────────────────────────────────────────
SCAN_DIRS = [
    "C:\\Windows\\System32\\", "C:\\Windows\\SysWOW64\\",
    "C:\\Users\\User\\AppData\\Local\\Temp\\",
    "C:\\Program Files\\", "C:\\Program Files (x86)\\",
    "C:\\Users\\User\\AppData\\Roaming\\",
    "C:\\ProgramData\\", "C:\\Windows\\Prefetch\\",
]
SCAN_FILES = [
    "ntdll.dll","kernel32.dll","user32.dll","msvcrt.dll","winlogon.exe",
    "svchost.exe","explorer.exe","lsass.exe","chrome.dll","discord.exe",
    "steam.dll","python314.dll","config.sys","winhelp.exe","mspaint.exe",
    "calc.exe","notepad.exe","regedit.exe","cmd.exe","taskmgr.exe",
    "dwm.exe","csrss.exe","smss.exe","wininit.exe","services.exe",
]
def fake_path():
    return random.choice(SCAN_DIRS) + random.choice(SCAN_FILES)

VIRUSES = [
    ("HateUSSR.exe",            "CRITICAL",  "C:\\Windows\\System32\\HateUSSR.exe",          RED),
    ("putlin_approved.bat",     "HIGH",      "C:\\Users\\User\\AppData\\Roaming\\putlin.bat", ORANGE),
    ("KimCancellation.dll",     "HIGH",      "C:\\Program Files\\Kim\\KimCancellation.dll",   ORANGE),
    ("batman_usb_payload.inf",  "0.14 ⚠",   "D:\\batman_usb_payload.inf",                    GOLD),
]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — Home
# ══════════════════════════════════════════════════════════════════════════════
class HomePage(QWidget):
    def __init__(self, on_scan):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 40, 60, 30)
        lay.setSpacing(0)
        lay.setAlignment(Qt.AlignCenter)

        # Header
        lay.addStretch(1)
        icon = label("🛡️", 56, align=Qt.AlignHCenter)
        icon.setStyleSheet("background:transparent; font-size:56px;")
        lay.addWidget(icon)
        lay.addSpacing(10)
        lay.addWidget(label("VirusDeleter", 32, bold=True,
                            color="#fff", align=Qt.AlignHCenter))
        sub = label("S E C U R I T Y   E X T R E M E   6.2", 12, bold=True,
                    color=GREEN, mono=True, align=Qt.AlignHCenter)
        sub.setStyleSheet(f"color:{GREEN}; background:transparent; letter-spacing:4px;")
        lay.addWidget(sub)
        lay.addSpacing(4)
        lay.addWidget(label("DownloadBetterPerformanceForFree — π Scan Engine™",
                            10, color="#333", align=Qt.AlignHCenter))
        lay.addSpacing(32)

        # Status panel
        panel = QFrame()
        panel.setStyleSheet(
            "QFrame{background:#0d0d0d;border:1px solid #1a2a1a;border-radius:12px;}")
        pl = QVBoxLayout(panel)
        pl.setContentsMargins(28, 20, 28, 20)
        pl.setSpacing(10)

        for icon_t, txt, col in [
            ("✓", "Real-Time Protection: ACTIVE",           GREEN),
            ("✓", "π Scan Engine: v3.14.159",               GREEN),
            ("✓", "Virus Database: Up to date (6.28.0)",    GREEN),
            ("✓", "Last scan: Never  (your PC is at risk)", ORANGE),
            ("✓", "Threats found in previous session: 3.14",RED),
        ]:
            row = QHBoxLayout()
            dot = label(icon_t, 11, bold=True, color=col, mono=True)
            dot.setFixedWidth(18)
            row.addWidget(dot)
            row.addWidget(label(txt, 11, color=col if col != GREEN else "#666"))
            row.addStretch()
            pl.addLayout(row)

        lay.addWidget(panel)
        lay.addSpacing(30)

        # Scan button
        btn = QPushButton("🔍  START FULL SCAN")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedWidth(300)
        btn.clicked.connect(on_scan)
        brow = QHBoxLayout()
        brow.addStretch(); brow.addWidget(btn); brow.addStretch()
        lay.addLayout(brow)
        lay.addSpacing(12)
        lay.addWidget(label("Estimated scan time: 3.14 seconds  |  Expected threats: 3.14",
                            9, color="#222", mono=True, align=Qt.AlignHCenter))
        lay.addStretch(2)

        # Footer
        lay.addWidget(hline())
        lay.addSpacing(8)
        lay.addWidget(label(
            "v6.2  |  π Institute Certified  |  0 real threats ever found  |  Kim disapproves",
            9, color="#1a1a1a", mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Scanning
# ══════════════════════════════════════════════════════════════════════════════
class ScanPage(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done
        self._pct        = 0
        self._files      = 0
        self._threats    = 0
        self._tick_timer = QTimer(); self._tick_timer.timeout.connect(self._tick)
        self._log_timer  = QTimer(); self._log_timer.timeout.connect(self._add_log)
        self._log_lines  = []

        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 36, 60, 24)
        lay.setSpacing(0)

        lay.addWidget(label("SCANNING…", 18, bold=True,
                            color=GREEN, mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)
        self._cur_file = label("Initializing π scan engine…", 9,
                               color="#333", mono=True, align=Qt.AlignHCenter)
        lay.addWidget(self._cur_file)
        lay.addSpacing(24)

        # Progress bar
        self._bar = QProgressBar()
        self._bar.setRange(0, 100); self._bar.setValue(0)
        self._bar.setTextVisible(False); self._bar.setFixedHeight(10)
        lay.addWidget(self._bar)
        lay.addSpacing(10)

        # Stats row
        stats = QHBoxLayout()
        self._lbl_files   = label("Files scanned: 0",      10, color="#444", mono=True)
        self._lbl_threats = label("Threats found: 0",      10, color="#444", mono=True)
        self._lbl_pct     = label("0%", 10, color=GREEN,   mono=True)
        self._lbl_pct.setAlignment(Qt.AlignRight)
        stats.addWidget(self._lbl_files)
        stats.addStretch()
        stats.addWidget(self._lbl_threats)
        stats.addStretch()
        stats.addWidget(self._lbl_pct)
        lay.addLayout(stats)
        lay.addSpacing(20)
        lay.addWidget(hline())
        lay.addSpacing(10)

        # Log area
        lay.addWidget(label("SCAN LOG", 8, color="#1e1e1e", mono=True))
        lay.addSpacing(6)
        self._log_layout = QVBoxLayout()
        self._log_layout.setSpacing(2)
        lay.addLayout(self._log_layout)

        lay.addStretch()
        lay.addWidget(hline())
        lay.addSpacing(6)
        lay.addWidget(label(
            "Do not turn off your PC  |  VirusDeleter Security Extreme 6.2",
            8, color="#191919", mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)

    def start(self):
        self._pct = 0; self._files = 0; self._threats = 0
        self._bar.setValue(0)
        self._lbl_files.setText("Files scanned: 0")
        self._lbl_threats.setText("Threats found: 0")
        self._lbl_threats.setStyleSheet("color:#444; background:transparent;")
        self._lbl_pct.setText("0%")
        for lbl in self._log_lines:
            self._log_layout.removeWidget(lbl); lbl.deleteLater()
        self._log_lines.clear()
        self._tick_timer.start(90)   # 100 ticks × 90ms ≈ 9s
        self._log_timer.start(220)

    def _tick(self):
        self._pct += 1
        self._files += random.randint(600, 1400)
        self._bar.setValue(self._pct)
        self._lbl_pct.setText(f"{self._pct}%")
        self._lbl_files.setText(f"Files scanned: {self._files:,}")

        # At 82% suddenly discover threats
        if self._pct == 82:
            self._threats = 3
            self._lbl_threats.setText(f"Threats found: {self._threats}  ⚠")
            self._lbl_threats.setStyleSheet(f"color:{RED}; background:transparent; font-weight:700;")
            self._add_log(override=f"⚠ THREAT DETECTED — HateUSSR.exe")
        if self._pct == 88:
            self._add_log(override=f"⚠ THREAT DETECTED — putlin_approved.bat")
        if self._pct == 94:
            self._add_log(override=f"⚠ THREAT DETECTED — KimCancellation.dll")
        if self._pct == 98:
            self._add_log(override=f"⚠ PARTIAL THREAT (0.14) — batman_usb_payload.inf")
            self._lbl_threats.setText("Threats found: 3.14  ⚠")

        if self._pct >= 100:
            self._tick_timer.stop()
            self._log_timer.stop()
            self._cur_file.setText("Scan complete.")
            QTimer.singleShot(800, self.on_done)

    def _add_log(self, override=None):
        if override:
            col  = RED if "THREAT" in override else GREEN
            text = override
        else:
            text = f"[ OK ] {fake_path()}"
            col  = "#252525"
        self._cur_file.setText(text if not override else fake_path())
        lbl = label(text, 9, color=col, mono=True)
        if len(self._log_lines) >= 7:
            old = self._log_lines.pop(0)
            self._log_layout.removeWidget(old); old.deleteLater()
        self._log_layout.addWidget(lbl)
        self._log_lines.append(lbl)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Results (threats found)
# ══════════════════════════════════════════════════════════════════════════════
class ResultsPage(QWidget):
    def __init__(self, on_delete, on_restart):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 36, 60, 24)
        lay.setSpacing(0)

        # Header
        hdr = label("⚠  SCAN COMPLETE — 3.14 THREATS FOUND", 16, bold=True,
                    color=RED, mono=True, align=Qt.AlignHCenter)
        lay.addWidget(hdr)
        lay.addSpacing(6)
        lay.addWidget(label("Your PC is infected. This is fine. We can fix it.",
                            10, color="#444", align=Qt.AlignHCenter))
        lay.addSpacing(24)

        # Threat cards
        for name, severity, path, col in VIRUSES:
            card = QFrame()
            card.setStyleSheet(
                f"QFrame{{background:#0d0505;border:1px solid #2a0a0a;border-radius:10px;}}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 14, 20, 14)
            cl.setSpacing(4)

            top = QHBoxLayout()
            top.addWidget(label("🦠", 14))
            top.addWidget(label(name, 13, bold=True, color=col))
            top.addStretch()
            sev = QLabel(severity)
            sev.setStyleSheet(
                f"background:{col}; color:#000; border-radius:4px; "
                f"padding:2px 10px; font-weight:900; font-size:10px;")
            top.addWidget(sev)
            cl.addLayout(top)
            cl.addWidget(label(path, 9, color="#333", mono=True))

            bar = QProgressBar(); bar.setObjectName("threat_bar")
            bar.setRange(0, 100); bar.setValue(100 if severity != "0.14 ⚠" else 14)
            bar.setTextVisible(False); bar.setFixedHeight(4)
            cl.addWidget(bar)

            lay.addWidget(card)
            lay.addSpacing(8)

        lay.addSpacing(10)
        lay.addWidget(hline())
        lay.addSpacing(16)

        # Summary
        summ = QHBoxLayout(); summ.addStretch()
        for txt, col in [("Threats: 3.14", RED), ("Severity: CRITICAL", ORANGE),
                          ("Files scanned: ~84,000", "#4488ff")]:
            t = QLabel(txt)
            t.setStyleSheet(f"background:{col};color:#000;border-radius:4px;"
                            f"padding:3px 10px;font-weight:700;font-size:10px;")
            summ.addWidget(t)
            summ.addSpacing(8)
        summ.addStretch()
        lay.addLayout(summ)
        lay.addSpacing(20)

        # Buttons
        brow = QHBoxLayout(); brow.setSpacing(12); brow.addStretch()
        skip = QPushButton("Ignore (not recommended)")
        skip.setObjectName("secondary"); skip.setCursor(Qt.PointingHandCursor)
        skip.clicked.connect(on_restart)
        delete_btn = QPushButton("🗑  DELETE ALL THREATS")
        delete_btn.setObjectName("danger"); delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(on_delete)
        brow.addWidget(skip); brow.addWidget(delete_btn); brow.addStretch()
        lay.addLayout(brow)

        lay.addStretch()
        lay.addWidget(hline())
        lay.addSpacing(6)
        lay.addWidget(label(
            "VirusDeleter Security Extreme 6.2  |  π Scan Engine  |  Kim still disapproves",
            9, color="#1a1a1a", mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Deleting
# ══════════════════════════════════════════════════════════════════════════════
class DeletingPage(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done  = on_done
        self._step    = 0
        self._timer   = QTimer(); self._timer.timeout.connect(self._tick)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 60, 60, 60)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(0)
        lay.addStretch(1)

        lay.addWidget(label("DELETING THREATS…", 18, bold=True,
                            color=RED, mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(30)

        self._rows = []
        for name, severity, _, col in VIRUSES:
            row = QHBoxLayout(); row.setSpacing(12)
            status = label("  ⏳", 13, color="#333", mono=True)
            status.setFixedWidth(28)
            row.addStretch()
            row.addWidget(status)
            row.addWidget(label(name, 12, bold=True, color=col))
            row.addStretch()
            lay.addLayout(row)
            lay.addSpacing(10)
            self._rows.append(status)

        lay.addSpacing(24)
        self._msg = label("", 10, color="#444", mono=True, align=Qt.AlignHCenter)
        lay.addWidget(self._msg)
        lay.addStretch(2)

    def start(self):
        self._step = 0
        for r in self._rows:
            r.setText("  ⏳"); r.setStyleSheet("color:#333; background:transparent;")
        self._msg.setText("Initializing quantum deletion…")
        self._timer.start(900)

    def _tick(self):
        msgs = [
            "Neutralizing HateUSSR.exe…",
            "Removing putlin_approved.bat…",
            "Uninstalling KimCancellation.dll…",
            "Fragmenting 0.14 of batman_usb_payload.inf…",
        ]
        if self._step < len(self._rows):
            self._rows[self._step].setText("  ✓")
            self._rows[self._step].setStyleSheet(f"color:{GREEN}; background:transparent; font-weight:700;")
            self._msg.setText(msgs[self._step] if self._step < len(msgs) else "")
        self._step += 1
        if self._step > len(self._rows):
            self._timer.stop()
            self._msg.setText("All threats eliminated.")
            QTimer.singleShot(900, self.on_done)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — All clear
# ══════════════════════════════════════════════════════════════════════════════
class ClearPage(QWidget):
    def __init__(self, on_restart):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 40, 60, 30)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(0)
        lay.addStretch(2)

        icon = label("✓", 80, bold=True, color=GREEN, align=Qt.AlignHCenter)
        icon.setStyleSheet(f"color:{GREEN}; background:transparent; font-size:80px; font-weight:900;")
        lay.addWidget(icon)
        lay.addSpacing(14)

        lay.addWidget(label("YOUR PC IS SAFE", 26, bold=True,
                            color="#fff", align=Qt.AlignHCenter))
        sub = label("3.14 THREATS ELIMINATED", 13, bold=True,
                    color=GREEN, mono=True, align=Qt.AlignHCenter)
        sub.setStyleSheet(f"color:{GREEN}; background:transparent; letter-spacing:3px;")
        lay.addWidget(sub)
        lay.addSpacing(28)

        # Stats panel
        panel = QFrame()
        panel.setStyleSheet(
            "QFrame{background:#080808;border:1px solid #1a2a1a;border-radius:12px;}")
        pl = QHBoxLayout(panel)
        pl.setContentsMargins(32, 20, 32, 20)
        pl.setSpacing(0)
        for val, lbl_txt in [("3.14", "Threats deleted"), ("6.28%", "PC safer"),
                              ("0", "Remaining threats"), ("3.14s", "Time taken")]:
            col = QVBoxLayout(); col.setAlignment(Qt.AlignCenter); col.setSpacing(4)
            col.addWidget(label(val, 22, bold=True, color=GREEN,
                                mono=True, align=Qt.AlignHCenter))
            col.addWidget(label(lbl_txt, 9, color="#333",
                                mono=True, align=Qt.AlignHCenter))
            pl.addLayout(col)
            if lbl_txt != "Time taken":
                sep = QFrame(); sep.setFrameShape(QFrame.VLine)
                sep.setStyleSheet("background:#1a1a1a; color:#1a1a1a; max-width:1px;")
                pl.addWidget(sep)
        lay.addWidget(panel)
        lay.addSpacing(16)

        lay.addWidget(label(
            "ℹ  The 0.14 fractional virus has been safely fragmented.\n"
            "The 3 integer viruses came pre-installed with Windows. This is normal.",
            10, color="#2a2a2a", align=Qt.AlignHCenter))
        lay.addSpacing(28)

        brow = QHBoxLayout(); brow.addStretch()
        btn = QPushButton("🔍  Scan Again")
        btn.setCursor(Qt.PointingHandCursor); btn.clicked.connect(on_restart)
        brow.addWidget(btn); brow.addStretch()
        lay.addLayout(brow)

        lay.addStretch(3)
        lay.addWidget(hline())
        lay.addSpacing(8)
        lay.addWidget(label(
            "VirusDeleter Security Extreme 6.2  |  Next scan will also find exactly 3.14 viruses",
            9, color="#191919", mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VirusDeleter Security Extreme 6.2")
        self.setMinimumSize(720, 560)
        self.resize(820, 620)
        self._center()

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._home     = HomePage(self._go_scan)
        self._scan     = ScanPage(self._go_results)
        self._results  = ResultsPage(self._go_deleting, self._go_home)
        self._deleting = DeletingPage(self._go_clear)
        self._clear    = ClearPage(self._go_home)

        for w in (self._home, self._scan, self._results, self._deleting, self._clear):
            self._stack.addWidget(w)
        self._stack.setCurrentIndex(0)

    def _center(self):
        g = QApplication.primaryScreen().geometry()
        self.move((g.width() - self.width()) // 2,
                  (g.height() - self.height()) // 2)

    def _go_scan(self):
        self._stack.setCurrentIndex(1)
        self._scan.start()

    def _go_results(self):
        self._stack.setCurrentIndex(2)

    def _go_deleting(self):
        self._stack.setCurrentIndex(3)
        self._deleting.start()

    def _go_clear(self):
        self._stack.setCurrentIndex(4)

    def _go_home(self):
        self._stack.setCurrentIndex(0)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
