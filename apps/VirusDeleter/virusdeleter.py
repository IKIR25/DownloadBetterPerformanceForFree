#!/usr/bin/env python3
"""
VirusDeleter Security Extreme 6.2
DownloadBetterPerformanceForFree — Finds Exactly π Viruses. Always.
"""

import sys, os, random, json
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QStackedWidget, QComboBox
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
QComboBox {{
    background: #111; border: 1px solid #222;
    border-radius: 6px; padding: 6px 12px; color: #777;
}}
QComboBox::drop-down {{ border: none; width: 0; }}
QComboBox QAbstractItemView {{
    background: #111; border: 1px solid #222; color: #888;
    selection-background-color: #1a1a1a;
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

# ── Scan types ────────────────────────────────────────────────────────────────
SCAN_TYPES = {
    "Quick Scan":  {"tick_ms": 50,  "max_files": 20_000,  "label": "~20k files"},
    "Full Scan":   {"tick_ms": 90,  "max_files": 84_000,  "label": "~84k files"},
    "Deep Scan":   {"tick_ms": 150, "max_files": 250_000, "label": "~250k files"},
}

# ── Virus pool ─────────────────────────────────────────────────────────────────
VIRUS_POOL = [
    # (name, severity, path, color)
    ("HateUSSR.exe",              "CRITICAL", "C:\\Windows\\System32\\HateUSSR.exe",             RED),
    ("putlin_approved.bat",       "HIGH",     "C:\\Users\\User\\AppData\\Roaming\\putlin.bat",    ORANGE),
    ("KimCancellation.dll",       "HIGH",     "C:\\Program Files\\Kim\\KimCancellation.dll",      ORANGE),
    ("FreeMinecraft.exe",         "HIGH",     "C:\\Users\\User\\Downloads\\FreeMinecraft.exe",    ORANGE),
    ("GoodVirusIPromise.jar",     "CRITICAL", "C:\\Program Files\\Java\\GoodVirusIPromise.jar",  RED),
    ("KeliusCoinMiner.exe",       "HIGH",     "C:\\Windows\\Temp\\KeliusCoinMiner.exe",          ORANGE),
    ("NotAVirus.pdf.exe",         "CRITICAL", "C:\\Users\\User\\Desktop\\NotAVirus.pdf.exe",     RED),
    ("TrustMeBro.dll",            "MEDIUM",   "C:\\Windows\\SysWOW64\\TrustMeBro.dll",           GOLD),
    ("PirateBay.torrent.bat",     "HIGH",     "C:\\Users\\User\\Downloads\\Pirates.torrent.bat", ORANGE),
    ("YesIKnowWhatImDoing.reg",   "HIGH",     "C:\\Windows\\System32\\YesIKnowWhatImDoing.reg",  ORANGE),
    ("WinBooster9000.exe",        "MEDIUM",   "C:\\Program Files (x86)\\WinBooster9000.exe",     GOLD),
    ("FBISurveillance.dll",       "CRITICAL", "C:\\Windows\\System32\\FBISurveillance.dll",      RED),
    ("CryptoRansomware.exe",      "CRITICAL", "C:\\ProgramData\\Temp\\CryptoRansomware.exe",     RED),
    ("SteamHack2024.exe",         "HIGH",     "C:\\Users\\User\\Desktop\\SteamHack2024.exe",     ORANGE),
    ("ILoveViruses.sys",          "CRITICAL", "C:\\Windows\\System32\\drivers\\ILoveViruses.sys",RED),
    ("AmericaSimulator.exe",      "MEDIUM",   "C:\\Program Files\\AmericaSimulator.exe",         GOLD),
]

# Partial virus (always the same 0.14 entry)
PARTIAL_VIRUS = ("batman_usb_payload.inf", "0.14 ⚠", "D:\\batman_usb_payload.inf", GOLD)

def pick_viruses():
    """Pick N full viruses (2-5) + 1 partial. Total = N.14"""
    n = random.randint(2, 5)
    full = random.sample(VIRUS_POOL, n)
    return full, PARTIAL_VIRUS

# ── Fake scan data ─────────────────────────────────────────────────────────────
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

# ── History ───────────────────────────────────────────────────────────────────
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".virusdeleter_history.json")

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_scan(scan_type, n_viruses):
    history = load_history()
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": scan_type,
        "threats": f"{n_viruses}.14",
    })
    history = history[-20:]
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — Home
# ══════════════════════════════════════════════════════════════════════════════
class HomePage(QWidget):
    def __init__(self, on_scan):
        super().__init__()
        self._on_scan = on_scan
        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 40, 60, 30)
        lay.setSpacing(0)
        lay.setAlignment(Qt.AlignCenter)

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
        panel.setObjectName("stat_panel")
        panel.setStyleSheet(
            "#stat_panel{background:#0d0d0d;border:1px solid #1a2a1a;border-radius:12px;}")
        pl = QVBoxLayout(panel)
        pl.setContentsMargins(28, 20, 28, 20)
        pl.setSpacing(10)

        for icon_t, txt, col in [
            ("✓", "Real-Time Protection: ACTIVE",           GREEN),
            ("✓", "π Scan Engine: v3.14.159",               GREEN),
            ("✓", "Virus Database: Up to date (6.28.0)",    GREEN),
            ("⚠", "Last scan: Never  (your PC is at risk)", ORANGE),
            ("✗", "Threats found in previous session: π",   RED),
        ]:
            row = QHBoxLayout()
            dot = label(icon_t, 11, bold=True, color=col, mono=True)
            dot.setFixedWidth(18)
            row.addWidget(dot)
            row.addWidget(label(txt, 11, color=col if col != GREEN else "#666"))
            row.addStretch()
            pl.addLayout(row)

        lay.addWidget(panel)
        lay.addSpacing(20)

        # Scan type selector
        type_row = QHBoxLayout(); type_row.addStretch()
        self._scan_type = QComboBox()
        for t in SCAN_TYPES:
            self._scan_type.addItem(t)
        self._scan_type.setCurrentIndex(1)  # default: Full Scan
        self._scan_type.setFixedWidth(200)
        type_row.addWidget(label("Scan type:", 10, color="#444"))
        type_row.addSpacing(8)
        type_row.addWidget(self._scan_type)
        type_row.addStretch()
        lay.addLayout(type_row)
        lay.addSpacing(16)

        btn = QPushButton("🔍  START SCAN")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedWidth(300)
        btn.clicked.connect(self._start)
        brow = QHBoxLayout()
        brow.addStretch(); brow.addWidget(btn); brow.addStretch()
        lay.addLayout(brow)
        lay.addSpacing(12)

        self._hint = label("", 9, color="#222", mono=True, align=Qt.AlignHCenter)
        lay.addWidget(self._hint)
        self._scan_type.currentIndexChanged.connect(self._update_hint)
        self._update_hint()

        # History
        lay.addSpacing(16)
        lay.addWidget(hline())
        lay.addSpacing(8)
        self._hist_layout = QVBoxLayout()
        self._hist_layout.setSpacing(2)
        lay.addLayout(self._hist_layout)

        lay.addStretch(2)
        lay.addWidget(hline())
        lay.addSpacing(8)
        lay.addWidget(label(
            "v6.2  |  π Institute Certified  |  0 real threats ever found  |  Kim disapproves",
            9, color="#1a1a1a", mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)

        self.refresh_history()

    def _update_hint(self):
        t = self._scan_type.currentText()
        info = SCAN_TYPES[t]
        self._hint.setText(
            f"Scan type: {t}  |  {info['label']}  |  Expected threats: π")

    def _start(self):
        self._on_scan(self._scan_type.currentText())

    def refresh_history(self):
        while self._hist_layout.count():
            item = self._hist_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        history = load_history()
        if not history:
            return
        self._hist_layout.addWidget(
            label("RECENT SCANS", 8, color="#222", mono=True, align=Qt.AlignHCenter))
        for entry in reversed(history[-4:]):
            txt = f"{entry['date']}  ·  {entry['type']}  ·  {entry['threats']} threats found"
            self._hist_layout.addWidget(
                label(txt, 8, color="#2a2a2a", mono=True, align=Qt.AlignHCenter))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Scanning
# ══════════════════════════════════════════════════════════════════════════════
class ScanPage(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done      = on_done
        self._pct         = 0
        self._files       = 0
        self._threats     = 0
        self._max_files   = 84_000
        self._viruses     = []
        self._partial     = None
        self._tick_timer  = QTimer(); self._tick_timer.timeout.connect(self._tick)
        self._log_timer   = QTimer(); self._log_timer.timeout.connect(self._add_log)
        self._log_lines   = []

        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 36, 60, 24)
        lay.setSpacing(0)

        self._title_lbl = label("SCANNING…", 18, bold=True,
                                color=GREEN, mono=True, align=Qt.AlignHCenter)
        lay.addWidget(self._title_lbl)
        lay.addSpacing(4)
        self._cur_file = label("Initializing π scan engine…", 9,
                               color="#333", mono=True, align=Qt.AlignHCenter)
        lay.addWidget(self._cur_file)
        lay.addSpacing(24)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100); self._bar.setValue(0)
        self._bar.setTextVisible(False); self._bar.setFixedHeight(10)
        lay.addWidget(self._bar)
        lay.addSpacing(10)

        stats = QHBoxLayout()
        self._lbl_files   = label("Files scanned: 0",  10, color="#444", mono=True)
        self._lbl_threats = label("Threats found: 0",  10, color="#444", mono=True)
        self._lbl_pct     = label("0%", 10, color=GREEN, mono=True)
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

    def start(self, scan_type, viruses, partial):
        self._pct = 0; self._files = 0; self._threats = 0
        self._viruses = viruses
        self._partial = partial
        cfg = SCAN_TYPES[scan_type]
        self._max_files = cfg["max_files"]
        self._bar.setValue(0)
        self._lbl_files.setText("Files scanned: 0")
        self._lbl_threats.setText("Threats found: 0")
        self._lbl_threats.setStyleSheet("color:#444; background:transparent;")
        self._lbl_pct.setText("0%")
        self._title_lbl.setText(f"SCANNING — {scan_type.upper()}…")
        for lbl in self._log_lines:
            self._log_layout.removeWidget(lbl); lbl.deleteLater()
        self._log_lines.clear()

        # Spread virus detections across [70%, 100%]
        n = len(viruses)
        detect_pcts = sorted(random.sample(range(70, 99), n))
        self._detect_at = {pct: v for pct, v in zip(detect_pcts, viruses)}
        self._partial_at = 99

        self._tick_timer.start(cfg["tick_ms"])
        self._log_timer.start(220)

    def _tick(self):
        self._pct += 1
        files_per_tick = self._max_files // 100
        self._files += random.randint(
            int(files_per_tick * 0.6), int(files_per_tick * 1.4))
        self._bar.setValue(self._pct)
        self._lbl_pct.setText(f"{self._pct}%")
        self._lbl_files.setText(f"Files scanned: {self._files:,}")

        if self._pct in self._detect_at:
            v = self._detect_at[self._pct]
            self._threats += 1
            self._lbl_threats.setText(f"Threats found: {self._threats}  ⚠")
            self._lbl_threats.setStyleSheet(f"color:{RED}; background:transparent; font-weight:700;")
            self._add_log(override=f"⚠ THREAT DETECTED — {v[0]}")

        if self._pct == self._partial_at:
            self._add_log(override=f"⚠ PARTIAL THREAT (0.14) — {self._partial[0]}")
            self._lbl_threats.setText(f"Threats found: {self._threats}.14  ⚠")

        if self._pct >= 100:
            self._tick_timer.stop()
            self._log_timer.stop()
            self._cur_file.setText("Scan complete.")
            QTimer.singleShot(800, self.on_done)

    def _add_log(self, override=None):
        if override:
            col  = RED if "THREAT" in override else GREEN
            text = override
            self._cur_file.setText(fake_path())
        else:
            text = f"[ OK ] {fake_path()}"
            col  = "#252525"
            self._cur_file.setText(text)
        lbl = label(text, 9, color=col, mono=True)
        if len(self._log_lines) >= 7:
            old = self._log_lines.pop(0)
            self._log_layout.removeWidget(old); old.deleteLater()
        self._log_layout.addWidget(lbl)
        self._log_lines.append(lbl)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Results
# ══════════════════════════════════════════════════════════════════════════════
class ResultsPage(QWidget):
    def __init__(self, on_delete, on_restart):
        super().__init__()
        self._on_delete  = on_delete
        self._on_restart = on_restart
        self._viruses    = []
        self._partial    = None

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(60, 36, 60, 24)
        self._lay.setSpacing(0)

        self._hdr = label("", 16, bold=True, color=RED, mono=True, align=Qt.AlignHCenter)
        self._lay.addWidget(self._hdr)
        self._lay.addSpacing(6)
        self._lay.addWidget(label("Your PC is infected. This is fine. We can fix it.",
                            10, color="#444", align=Qt.AlignHCenter))
        self._lay.addSpacing(24)

        self._cards_layout = QVBoxLayout()
        self._cards_layout.setSpacing(8)
        self._lay.addLayout(self._cards_layout)

        self._lay.addSpacing(10)
        self._lay.addWidget(hline())
        self._lay.addSpacing(16)

        self._summ_row = QHBoxLayout(); self._summ_row.addStretch()
        self._tag_threats = self._make_tag("Threats: ?", RED)
        self._tag_sev     = self._make_tag("Severity: CRITICAL", ORANGE)
        self._tag_files   = self._make_tag("Files: ?", "#4488ff")
        for t in (self._tag_threats, self._tag_sev, self._tag_files):
            self._summ_row.addWidget(t); self._summ_row.addSpacing(8)
        self._summ_row.addStretch()
        self._lay.addLayout(self._summ_row)
        self._lay.addSpacing(20)

        brow = QHBoxLayout(); brow.setSpacing(12); brow.addStretch()
        skip = QPushButton("Ignore (not recommended)")
        skip.setObjectName("secondary"); skip.setCursor(Qt.PointingHandCursor)
        skip.clicked.connect(on_restart)
        delete_btn = QPushButton("🗑  DELETE ALL THREATS")
        delete_btn.setObjectName("danger"); delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(on_delete)
        brow.addWidget(skip); brow.addWidget(delete_btn); brow.addStretch()
        self._lay.addLayout(brow)

        self._lay.addStretch()
        self._lay.addWidget(hline())
        self._lay.addSpacing(6)
        self._lay.addWidget(label(
            "VirusDeleter Security Extreme 6.2  |  π Scan Engine  |  Kim still disapproves",
            9, color="#1a1a1a", mono=True, align=Qt.AlignHCenter))
        self._lay.addSpacing(4)

    def _make_tag(self, txt, col):
        t = QLabel(txt)
        t.setStyleSheet(f"background:{col};color:#000;border-radius:4px;"
                        f"padding:3px 10px;font-weight:700;font-size:10px;")
        return t

    def show(self, viruses, partial, scanned_files):
        self._viruses = viruses
        self._partial = partial
        n = len(viruses)
        self._hdr.setText(f"⚠  SCAN COMPLETE — {n}.14 THREATS FOUND")
        self._tag_threats.setText(f"Threats: {n}.14")
        self._tag_files.setText(f"Files scanned: {scanned_files:,}")

        # Rebuild cards
        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        all_viruses = list(viruses) + [partial]
        for name, severity, path, col in all_viruses:
            card = QFrame()
            card.setObjectName("threat_card")
            card.setStyleSheet(
                "#threat_card{background:#0d0505;border:1px solid #2a0a0a;border-radius:10px;}")
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
            bar.setRange(0, 100)
            bar.setValue(14 if "0.14" in severity else 100)
            bar.setTextVisible(False); bar.setFixedHeight(4)
            cl.addWidget(bar)

            self._cards_layout.addWidget(card)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Deleting
# ══════════════════════════════════════════════════════════════════════════════
class DeletingPage(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done  = on_done
        self._step    = 0
        self._viruses = []
        self._timer   = QTimer(); self._timer.timeout.connect(self._tick)

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(60, 60, 60, 60)
        self._lay.setAlignment(Qt.AlignCenter)
        self._lay.setSpacing(0)
        self._lay.addStretch(1)

        self._title = label("DELETING THREATS…", 18, bold=True,
                            color=RED, mono=True, align=Qt.AlignHCenter)
        self._lay.addWidget(self._title)
        self._lay.addSpacing(30)

        self._rows_layout = QVBoxLayout()
        self._rows_layout.setSpacing(10)
        self._lay.addLayout(self._rows_layout)

        self._lay.addSpacing(24)
        self._msg = label("", 10, color="#444", mono=True, align=Qt.AlignHCenter)
        self._lay.addWidget(self._msg)
        self._lay.addStretch(2)

    def start(self, viruses, partial):
        self._viruses = list(viruses) + [partial]
        self._step    = 0

        # Rebuild rows
        while self._rows_layout.count():
            item = self._rows_layout.takeAt(0)
            w = item.widget()
            if not w:
                lay = item.layout()
                if lay:
                    while lay.count():
                        i2 = lay.takeAt(0)
                        if i2.widget():
                            i2.widget().deleteLater()
            if w:
                w.deleteLater()

        self._status_lbls = []
        for name, _, _, col in self._viruses:
            row = QHBoxLayout(); row.setSpacing(12)
            status = label("  ⏳", 13, color="#333", mono=True)
            status.setFixedWidth(28)
            row.addStretch()
            row.addWidget(status)
            row.addWidget(label(name, 12, bold=True, color=col))
            row.addStretch()
            self._rows_layout.addLayout(row)
            self._status_lbls.append(status)

        self._msg.setText("Initializing quantum deletion…")
        self._timer.start(900)

    def _tick(self):
        if self._step < len(self._viruses):
            name = self._viruses[self._step][0]
            self._status_lbls[self._step].setText("  ✓")
            self._status_lbls[self._step].setStyleSheet(
                f"color:{GREEN}; background:transparent; font-weight:700;")
            self._msg.setText(f"Eliminating {name}…")
        self._step += 1
        if self._step > len(self._viruses):
            self._timer.stop()
            self._msg.setText("All threats eliminated.")
            QTimer.singleShot(900, self.on_done)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — All clear
# ══════════════════════════════════════════════════════════════════════════════
class ClearPage(QWidget):
    def __init__(self, on_restart):
        super().__init__()
        self._on_restart = on_restart
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

        self._sub = label("π THREATS ELIMINATED", 13, bold=True,
                          color=GREEN, mono=True, align=Qt.AlignHCenter)
        self._sub.setStyleSheet(f"color:{GREEN}; background:transparent; letter-spacing:3px;")
        lay.addWidget(self._sub)
        lay.addSpacing(28)

        # Stats panel
        panel = QFrame()
        panel.setObjectName("stats_panel")
        panel.setStyleSheet(
            "#stats_panel{background:#080808;border:1px solid #1a2a1a;border-radius:12px;}")
        self._pl = QHBoxLayout(panel)
        self._pl.setContentsMargins(32, 20, 32, 20)
        self._pl.setSpacing(0)

        self._stat_vals = []
        for val, lbl_txt in [("π", "Threats deleted"), ("6.28%", "PC safer"),
                              ("0", "Remaining"), ("?s", "Time taken")]:
            col = QVBoxLayout(); col.setAlignment(Qt.AlignCenter); col.setSpacing(4)
            v = label(val, 22, bold=True, color=GREEN, mono=True, align=Qt.AlignHCenter)
            col.addWidget(v)
            col.addWidget(label(lbl_txt, 9, color="#333", mono=True, align=Qt.AlignHCenter))
            self._pl.addLayout(col)
            self._stat_vals.append(v)
            if lbl_txt != "Time taken":
                sep = QFrame(); sep.setFrameShape(QFrame.VLine)
                sep.setStyleSheet("background:#1a1a1a; color:#1a1a1a; max-width:1px;")
                self._pl.addWidget(sep)

        lay.addWidget(panel)
        lay.addSpacing(16)

        self._note = label("", 10, color="#2a2a2a", align=Qt.AlignHCenter)
        self._note.setWordWrap(True)
        lay.addWidget(self._note)
        lay.addSpacing(28)

        # History
        self._hist_layout = QVBoxLayout()
        self._hist_layout.setSpacing(2)
        lay.addLayout(self._hist_layout)
        lay.addSpacing(8)

        brow = QHBoxLayout(); brow.addStretch()
        btn = QPushButton("🔍  Scan Again")
        btn.setCursor(Qt.PointingHandCursor); btn.clicked.connect(on_restart)
        brow.addWidget(btn); brow.addStretch()
        lay.addLayout(brow)

        lay.addStretch(3)
        lay.addWidget(hline())
        lay.addSpacing(8)
        lay.addWidget(label(
            "VirusDeleter Security Extreme 6.2  |  Next scan will also find exactly π viruses",
            9, color="#191919", mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(4)

    def show(self, n_viruses, scan_time_s):
        self._sub.setText(f"{n_viruses}.14 THREATS ELIMINATED")
        self._stat_vals[0].setText(f"{n_viruses}.14")
        self._stat_vals[3].setText(f"{scan_time_s:.1f}s")
        self._note.setText(
            f"ℹ  The 0.14 fractional virus has been safely fragmented.\n"
            f"The {n_viruses} integer viruses came pre-installed with Windows. This is normal.")

        # History
        while self._hist_layout.count():
            item = self._hist_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        history = load_history()
        if history:
            self._hist_layout.addWidget(
                label("SCAN HISTORY", 8, color="#222", mono=True, align=Qt.AlignHCenter))
            for entry in reversed(history[-3:]):
                txt = f"{entry['date']}  ·  {entry['type']}  ·  {entry['threats']} threats"
                self._hist_layout.addWidget(
                    label(txt, 8, color="#2a2a2a", mono=True, align=Qt.AlignHCenter))


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VirusDeleter Security Extreme 6.2")
        self.setMinimumSize(720, 560)
        self.resize(860, 640)
        self._center()

        self._viruses   = []
        self._partial   = None
        self._scan_type = "Full Scan"
        self._scan_start = None

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

    def _go_scan(self, scan_type):
        self._scan_type = scan_type
        self._viruses, self._partial = pick_viruses()
        self._scan_start = datetime.now()
        self._stack.setCurrentIndex(1)
        self._scan.start(scan_type, self._viruses, self._partial)

    def _go_results(self):
        scanned = self._scan._files
        self._stack.setCurrentIndex(2)
        self._results.show(self._viruses, self._partial, scanned)

    def _go_deleting(self):
        self._stack.setCurrentIndex(3)
        self._deleting.start(self._viruses, self._partial)

    def _go_clear(self):
        elapsed = (datetime.now() - self._scan_start).total_seconds() if self._scan_start else 0
        n = len(self._viruses)
        save_scan(self._scan_type, n)
        self._home.refresh_history()
        self._clear.show(n, elapsed)
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
