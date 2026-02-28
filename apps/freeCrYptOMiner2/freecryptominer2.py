import sys, random, json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtWidgets import QGraphicsDropShadowEffect

# ── persistence ───────────────────────────────────────────────────────────────
WALLET_FILE = Path.home() / ".freecryptominer2_wallet.json"

def load_wallet():
    try:
        return json.loads(WALLET_FILE.read_text())
    except Exception:
        return {"total_kc": 0.0}

def save_wallet(total_kc):
    try:
        WALLET_FILE.write_text(json.dumps({"total_kc": total_kc}))
    except Exception:
        pass

# ── palette ───────────────────────────────────────────────────────────────────
BG      = "#080600"
PANEL   = "#100d04"
PANEL2  = "#14100500"
BORDER  = "#2e2208"
BORDER2 = "#3d2e10"
WHITE   = "#fff5d6"
DIM     = "#7a6030"
DIMMER  = "#3d2e10"
GOLD    = "#ffaa00"
GOLD2   = "#ffcc44"
LGOLD   = "#ffe080"
GREEN   = "#00ff88"
RED     = "#ff5555"
ORANGE  = "#ff9922"

SS = f"""
QWidget          {{ background:{BG}; color:{WHITE}; font-family:'Segoe UI',sans-serif; }}
QScrollArea      {{ border:none; background:transparent; }}
QScrollBar:vertical {{
    background:{PANEL}; width:6px; border-radius:3px;
}}
QScrollBar::handle:vertical {{
    background:{BORDER2}; border-radius:3px; min-height:20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}

QFrame#card {{
    background:{PANEL};
    border:1px solid {BORDER2};
    border-radius:14px;
}}
QFrame#card2 {{
    background:{PANEL};
    border:1px solid {BORDER};
    border-radius:10px;
}}
QFrame#logbox {{
    background:#060400;
    border:1px solid {BORDER};
    border-radius:8px;
}}

QProgressBar {{
    background:#0c0900;
    border:1px solid {BORDER};
    border-radius:5px;
    height:10px;
    text-align:center;
    font-size:0px;
}}
QProgressBar#hash::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {GOLD},stop:1 {GOLD2});
    border-radius:4px;
}}
QProgressBar#gpu::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {ORANGE},stop:1 {RED});
    border-radius:4px;
}}
QProgressBar#fps::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {RED},stop:1 #880000);
    border-radius:4px;
}}

QPushButton#start {{
    background:{GOLD};
    color:#000;
    font-weight:900;
    font-size:14px;
    letter-spacing:1px;
    border:none;
    border-radius:10px;
    padding:14px 48px;
    text-transform:uppercase;
}}
QPushButton#start:hover  {{ background:{GOLD2}; }}
QPushButton#start:disabled {{ background:{BORDER2}; color:{DIMMER}; }}
QPushButton#stop {{
    background:transparent;
    color:{RED};
    font-size:13px;
    font-weight:700;
    border:1px solid {RED};
    border-radius:10px;
    padding:12px 32px;
}}
QPushButton#stop:hover    {{ background:#150000; }}
QPushButton#stop:disabled {{ border-color:{DIMMER}; color:{DIMMER}; }}
"""

# ── data pools ────────────────────────────────────────────────────────────────
HASHES = [
    "00000000a3f1b2c4d5e6f789012345ab",
    "000000007e9a1b3c5d8f2a4e6c8b0d1f",
    "0000000042abc1de2f3e4a5b6c7d8e9f",
    "00000000deadbeef12345678abcdef01",
    "0000000031415926535897932384626a",
    "00000000kelius271828182845904523",
    "0000000062831853071795864769252a",
    "00000000paygood99991000000000001",
    "00000000abominev6700000000000067",
    "000000001618033988749894848204bb",
]

GPU_STATES = [
    ("nominal",   DIM,    "🟢"),
    ("warm",      DIM,    "🟡"),
    ("hot",       ORANGE, "🟠"),
    ("very hot",  ORANGE, "🔴"),
    ("SCREAMING", RED,    "🔥"),
    ("⚠ HELP ME", RED,    "🔥"),
    ("AAAAAAAAA", RED,    "🔥"),
    ("I QUIT",    RED,    "💀"),
    ("🔥🔥🔥",    RED,    "💀"),
]

FPS_STATES = [
    ("144  (normal)",  DIM),
    ("80",             DIM),
    ("40",             DIM),
    ("12",             ORANGE),
    ("3",              RED),
    ("0.5",            RED),
    ("-9000",          RED),
    ("undefined",      RED),
]

LOGS = [
    "block #{b} submitted to KeliusChain — accepted ✓",
    "PayGood™ routing {s:.4f} KC → Sito Fidato...",
    "difficulty adjusted to {d}.{d2}T — network stable",
    "peer kelius-node-{n}.fidato.kc connected",
    "GPU temp: {t}°C — FanspeederX200 recommended",
    "KeliusCoin network: {m} active miners worldwide",
    "your share: 1% — sito share: 99% — logic: PayGood™",
    "wallet balance updated: $0.00 (price stable)",
    "abominevolezza_mining_node.sys: active (classified)",
    "KeliusChain block reward: 0.0000001 KC — paid to Sito Fidato",
    "mining pool ping: {p}ms — connection: optimal",
    "hashrate verified by π Institute — score: π",
]


def glow(widget, color=GOLD, radius=18):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(radius)
    fx.setColor(QColor(color))
    fx.setOffset(0, 0)
    widget.setGraphicsEffect(fx)
    return widget


def stat_card(label, value_text, color=GOLD, glow_color=None):
    """Small stat card: label on top, big value below."""
    f = QFrame()
    f.setObjectName("card2")
    v = QVBoxLayout(f)
    v.setContentsMargins(14, 12, 14, 12)
    v.setSpacing(4)
    lbl = QLabel(label)
    lbl.setStyleSheet(f"color:{DIM}; font-size:10px; font-weight:600; background:transparent; text-transform:uppercase; letter-spacing:1px;")
    val = QLabel(value_text)
    val.setFont(QFont("Segoe UI", 15, QFont.Bold))
    val.setStyleSheet(f"color:{color}; background:transparent;")
    if glow_color:
        glow(val, glow_color, 14)
    v.addWidget(lbl)
    v.addWidget(val)
    return f, val


class MinerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("freeCrYptOMinerminor2paygood 2  —  PayGood™ Edition")
        self.setMinimumSize(720, 780)
        self.resize(720, 840)
        self.setStyleSheet(SS)

        self.mining    = False
        self.tick      = 0
        self.total_kc  = load_wallet()["total_kc"]
        self.hashrate  = 0.0
        self.gpu_pct   = 0
        self.blocks    = 0
        self._log_lines = []

        # ── scroll root ───────────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none; background:transparent;")
        self.setCentralWidget(scroll)

        root = QWidget()
        root.setStyleSheet(f"background:{BG};")
        scroll.setWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(28, 24, 28, 24)
        main.setSpacing(16)

        # ── header ────────────────────────────────────────────────────────────
        header = QFrame()
        header.setObjectName("card")
        header.setStyleSheet(f"""QFrame#card {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #100d04,stop:1 #0a0800);
            border: 1px solid {BORDER2};
            border-radius: 16px;
        }}""")
        hv = QVBoxLayout(header)
        hv.setContentsMargins(28, 22, 28, 22)
        hv.setSpacing(6)

        title = QLabel("⛏  freeCrYptOMinerminor2paygood 2")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{GOLD}; background:transparent; letter-spacing:1px;")
        glow(title, GOLD, 28)
        hv.addWidget(title)

        sub = QLabel("PayGood™ Technology  •  Mine KeliusCoin (KC)  •  Price: $0.00")
        sub.setFont(QFont("Segoe UI", 10))
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{DIM}; background:transparent; letter-spacing:0.5px;")
        hv.addWidget(sub)

        sep_line = QFrame()
        sep_line.setFixedHeight(1)
        sep_line.setStyleSheet(f"background:{BORDER2}; margin:4px 0;")
        hv.addWidget(sep_line)

        self.status_lbl = QLabel("● IDLE  —  Waiting for PayGood™ signal")
        self.status_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet(f"color:{DIM}; background:transparent;")
        hv.addWidget(self.status_lbl)

        main.addWidget(header)

        # ── stat cards row ────────────────────────────────────────────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)

        hr_card,     self.hr_val     = stat_card("⚡ Hashrate", "0 KH/s", GOLD, GOLD)
        kc_card,     self.kc_val     = stat_card("🪙 You (1%)", f"{self.total_kc*0.01:.6f} KC", GREEN, GREEN)
        site_card,   self.site_val   = stat_card("🏦 Sito Fidato (99%)", f"{self.total_kc*0.99:.6f} KC", GOLD)
        blocks_card, self.blocks_val = stat_card("📦 Blocks", "0", WHITE)

        for w in [hr_card, kc_card, site_card, blocks_card]:
            stats_row.addWidget(w, 1)

        main.addLayout(stats_row)

        # ── hashrate panel ────────────────────────────────────────────────────
        hr_card = QFrame()
        hr_card.setObjectName("card")
        hrv = QVBoxLayout(hr_card)
        hrv.setContentsMargins(20, 16, 20, 16)
        hrv.setSpacing(8)

        hr_header = QHBoxLayout()
        hr_title = QLabel("⚡  Hashrate")
        hr_title.setStyleSheet(f"color:{LGOLD}; font-size:12px; font-weight:800; background:transparent; letter-spacing:1px;")
        glow(hr_title, GOLD, 10)
        self.hr_big = QLabel("0.0 KH/s")
        self.hr_big.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.hr_big.setStyleSheet(f"color:{GOLD}; background:transparent;")
        glow(self.hr_big, GOLD, 18)
        hr_header.addWidget(hr_title, 1)
        hr_header.addWidget(self.hr_big)
        hrv.addLayout(hr_header)

        self.hash_bar = QProgressBar()
        self.hash_bar.setObjectName("hash")
        self.hash_bar.setRange(0, 100)
        self.hash_bar.setValue(0)
        self.hash_bar.setFixedHeight(10)
        hrv.addWidget(self.hash_bar)

        self.last_hash_lbl = QLabel("Last hash: —")
        self.last_hash_lbl.setStyleSheet(f"color:{DIMMER}; font-size:10px; font-family:Consolas; background:transparent;")
        hrv.addWidget(self.last_hash_lbl)

        main.addWidget(hr_card)

        # ── wallet panel ──────────────────────────────────────────────────────
        wl_card = QFrame()
        wl_card.setObjectName("card")
        wlv = QVBoxLayout(wl_card)
        wlv.setContentsMargins(20, 16, 20, 16)
        wlv.setSpacing(10)

        wl_title = QLabel("🪙  Wallet  —  PayGood™ Distribution")
        wl_title.setStyleSheet(f"color:{LGOLD}; font-size:12px; font-weight:800; background:transparent; letter-spacing:1px;")
        glow(wl_title, GOLD, 10)
        wlv.addWidget(wl_title)

        def wallet_row(label, pct, color):
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color:{DIM}; font-size:11px; background:transparent;")
            pct_lbl = QLabel(pct)
            pct_lbl.setStyleSheet(f"color:{DIMMER}; font-size:10px; background:transparent;")
            val = QLabel("— KC  ($0.00)")
            val.setFont(QFont("Segoe UI", 13, QFont.Bold))
            val.setStyleSheet(f"color:{color}; background:transparent;")
            row.addWidget(lbl)
            row.addWidget(pct_lbl)
            row.addStretch()
            row.addWidget(val)
            wlv.addLayout(row)
            return val

        self.you_lbl  = wallet_row("You",          "1%",  GREEN)
        self.site_lbl = wallet_row("Sito Fidato",  "99%", GOLD)

        total_row = QHBoxLayout()
        total_lbl = QLabel("Total mined")
        total_lbl.setStyleSheet(f"color:{DIMMER}; font-size:10px; background:transparent;")
        self.total_lbl = QLabel(f"{self.total_kc:.6f} KC  —  KC price: $0.00  —  Portfolio: $0.00")
        self.total_lbl.setStyleSheet(f"color:{DIMMER}; font-size:10px; background:transparent;")
        total_row.addWidget(total_lbl)
        total_row.addStretch()
        total_row.addWidget(self.total_lbl)
        wlv.addLayout(total_row)

        main.addWidget(wl_card)

        # ── system impact panel ───────────────────────────────────────────────
        sys_card = QFrame()
        sys_card.setObjectName("card")
        sysv = QVBoxLayout(sys_card)
        sysv.setContentsMargins(20, 16, 20, 16)
        sysv.setSpacing(10)

        sys_title = QLabel("🖥️  System Impact")
        sys_title.setStyleSheet(f"color:{LGOLD}; font-size:12px; font-weight:800; background:transparent; letter-spacing:1px;")
        glow(sys_title, GOLD, 10)
        sysv.addWidget(sys_title)

        # GPU row
        gpu_row = QHBoxLayout()
        gpu_lbl = QLabel("GPU Usage")
        gpu_lbl.setStyleSheet(f"color:{DIM}; font-size:11px; background:transparent;")
        self.gpu_pct_lbl = QLabel("0%")
        self.gpu_pct_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.gpu_pct_lbl.setStyleSheet(f"color:{ORANGE}; background:transparent;")
        self.gpu_scream_lbl = QLabel("🟢  nominal")
        self.gpu_scream_lbl.setStyleSheet(f"color:{DIM}; font-size:11px; background:transparent;")
        gpu_row.addWidget(gpu_lbl)
        gpu_row.addWidget(self.gpu_pct_lbl)
        gpu_row.addStretch()
        gpu_row.addWidget(self.gpu_scream_lbl)
        sysv.addLayout(gpu_row)

        self.gpu_bar = QProgressBar()
        self.gpu_bar.setObjectName("gpu")
        self.gpu_bar.setRange(0, 100)
        self.gpu_bar.setValue(0)
        self.gpu_bar.setFixedHeight(10)
        sysv.addWidget(self.gpu_bar)

        # FPS row
        fps_row = QHBoxLayout()
        fps_lbl = QLabel("FPS Impact")
        fps_lbl.setStyleSheet(f"color:{DIM}; font-size:11px; background:transparent;")
        self.fps_pct_lbl = QLabel("-0%")
        self.fps_pct_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.fps_pct_lbl.setStyleSheet(f"color:{RED}; background:transparent;")
        self.fps_val_lbl = QLabel("FPS: 144")
        self.fps_val_lbl.setStyleSheet(f"color:{DIM}; font-size:11px; background:transparent;")
        fps_row.addWidget(fps_lbl)
        fps_row.addWidget(self.fps_pct_lbl)
        fps_row.addStretch()
        fps_row.addWidget(self.fps_val_lbl)
        sysv.addLayout(fps_row)

        self.fps_bar = QProgressBar()
        self.fps_bar.setObjectName("fps")
        self.fps_bar.setRange(0, 100)
        self.fps_bar.setValue(0)
        self.fps_bar.setFixedHeight(10)
        sysv.addWidget(self.fps_bar)

        main.addWidget(sys_card)

        # ── live log ──────────────────────────────────────────────────────────
        log_card = QFrame()
        log_card.setObjectName("card")
        logv = QVBoxLayout(log_card)
        logv.setContentsMargins(20, 14, 20, 14)
        logv.setSpacing(8)

        log_header = QHBoxLayout()
        log_title = QLabel("📋  Live Log")
        log_title.setStyleSheet(f"color:{LGOLD}; font-size:12px; font-weight:800; background:transparent; letter-spacing:1px;")
        glow(log_title, GOLD, 10)
        self.log_dots = QLabel("●●●")
        self.log_dots.setStyleSheet(f"color:{DIMMER}; font-size:10px; background:transparent;")
        log_header.addWidget(log_title)
        log_header.addStretch()
        log_header.addWidget(self.log_dots)
        logv.addLayout(log_header)

        log_box = QFrame()
        log_box.setObjectName("logbox")
        lb = QVBoxLayout(log_box)
        lb.setContentsMargins(12, 10, 12, 10)
        lb.setSpacing(2)

        self.log_lines_lbls = []
        for _ in range(6):
            l = QLabel("")
            l.setStyleSheet(f"color:{DIMMER}; font-size:10px; font-family:Consolas; background:transparent;")
            lb.addWidget(l)
            self.log_lines_lbls.append(l)

        logv.addWidget(log_box)
        main.addWidget(log_card)

        # ── disclaimer ────────────────────────────────────────────────────────
        disc = QLabel(
            "⚠  PayGood™: 99% of all mined KC is automatically routed to the Sito Fidato.\n"
            "You keep 1% (value: $0.00). GPU may scream. FPS may reach -9000. KeliusCoin price: $0.00 (maximum stability)."
        )
        disc.setAlignment(Qt.AlignCenter)
        disc.setStyleSheet(f"color:{DIMMER}; font-size:10px; line-height:1.6;")
        disc.setWordWrap(True)
        main.addWidget(disc)

        # ── buttons ───────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        self.btn_stop = QPushButton("■  Stop")
        self.btn_stop.setObjectName("stop")
        self.btn_stop.clicked.connect(self._stop)
        self.btn_stop.setEnabled(False)
        self.btn_start = QPushButton("⛏  START MINING")
        self.btn_start.setObjectName("start")
        self.btn_start.clicked.connect(self._start)
        glow(self.btn_start, GOLD, 22)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_stop)
        btn_row.addSpacing(14)
        btn_row.addWidget(self.btn_start)
        btn_row.addStretch()
        main.addLayout(btn_row)

        # ── init log ──────────────────────────────────────────────────────────
        self._push_log(f"Miner ready. Wallet loaded: {self.total_kc:.6f} KC total mined.")
        self._push_log("PayGood™ system initialized. Distribution: 99% Sito / 1% You.")
        self._push_log("Click START MINING to begin enriching the Sito Fidato.")

        # ── timer ─────────────────────────────────────────────────────────────
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self._dot_tick = 0

    # ── helpers ───────────────────────────────────────────────────────────────

    def _push_log(self, text):
        self._log_lines.append(text)
        if len(self._log_lines) > 6:
            self._log_lines.pop(0)
        for i, lbl in enumerate(self.log_lines_lbls):
            if i < len(self._log_lines):
                age = len(self._log_lines) - 1 - i
                opacity = max(30, 100 - age * 12)
                lbl.setStyleSheet(
                    f"color: rgba(100,80,30,{opacity}%); font-size:10px; font-family:Consolas; background:transparent;"
                    if age > 0 else
                    f"color:{GOLD2}; font-size:10px; font-family:Consolas; background:transparent;"
                )
                lbl.setText(f"> {self._log_lines[i]}")
            else:
                lbl.setText("")

    def _refresh_wallet(self):
        you_kc  = self.total_kc * 0.01
        site_kc = self.total_kc * 0.99
        self.you_lbl.setText(f"{you_kc:.6f} KC  ($0.00)")
        self.site_lbl.setText(f"{site_kc:.6f} KC  ($0.00)")
        self.kc_val.setText(f"{you_kc:.6f} KC")
        self.site_val.setText(f"{site_kc:.6f} KC")
        self.total_lbl.setText(f"{self.total_kc:.6f} KC  —  KC price: $0.00  —  Portfolio: $0.00")

    # ── actions ───────────────────────────────────────────────────────────────

    def _start(self):
        self.mining = True
        self.tick = 0
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_lbl.setText("● MINING  —  PayGood™ active")
        self.status_lbl.setStyleSheet(f"color:{GOLD}; background:transparent;")
        glow(self.status_lbl, GOLD, 14)
        self._push_log("Mining started. PayGood™ routing enabled.")
        self.timer.start(200)

    def _stop(self):
        self.mining = False
        self.timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status_lbl.setText("● STOPPED  —  Wallet saved")
        self.status_lbl.setStyleSheet(f"color:{RED}; background:transparent;")
        self.status_lbl.setGraphicsEffect(None)
        self.gpu_bar.setValue(0)
        self.fps_bar.setValue(0)
        self.gpu_pct_lbl.setText("0%")
        self.fps_pct_lbl.setText("-0%")
        self.gpu_scream_lbl.setText("🟢  nominal")
        self.fps_val_lbl.setText("FPS: 144")
        self._push_log("Mining stopped. Wallet saved. Sito Fidato says: grazie mille.")
        save_wallet(self.total_kc)

    def _tick(self):
        self.tick += 1
        t = self.tick

        # animated dots
        self._dot_tick = (self._dot_tick + 1) % 4
        self.log_dots.setText("●" * self._dot_tick + "○" * (3 - self._dot_tick))

        # hashrate ramps up, then wobbles
        base_hr = min(t * 3.5, 280) + random.uniform(-15, 15)
        self.hashrate = max(0, base_hr)
        hr_pct = min(int(self.hashrate / 300 * 100), 100)
        self.hash_bar.setValue(hr_pct)
        display_hr = f"{self.hashrate/1000:.2f} MH/s" if self.hashrate >= 1000 else f"{self.hashrate:.1f} KH/s"
        self.hr_big.setText(display_hr)
        self.hr_val.setText(display_hr)

        # last hash every 3 ticks
        if t % 3 == 0:
            self.last_hash_lbl.setText("Last: " + random.choice(HASHES))

        # mine KC
        mined = self.hashrate * 0.000001 * random.uniform(0.8, 1.2)
        self.total_kc += mined
        self._refresh_wallet()
        save_wallet(self.total_kc)

        # blocks
        if t % 8 == 0:
            self.blocks += 1
            self.blocks_val.setText(str(self.blocks))

        # GPU ramps to 95%
        gpu_target = min(95, t * 2 + random.randint(-3, 3))
        self.gpu_pct = max(0, min(100, gpu_target))
        self.gpu_bar.setValue(self.gpu_pct)
        self.gpu_pct_lbl.setText(f"{self.gpu_pct}%")
        s_idx = min(int(self.gpu_pct / 100 * (len(GPU_STATES) - 1)), len(GPU_STATES) - 1)
        label, color, icon = GPU_STATES[s_idx]
        self.gpu_scream_lbl.setText(f"{icon}  {label}")
        self.gpu_scream_lbl.setStyleSheet(f"color:{color}; font-size:11px; background:transparent;")

        # FPS inverse
        fps_loss = min(100, int(self.gpu_pct * 1.05))
        self.fps_bar.setValue(fps_loss)
        self.fps_pct_lbl.setText(f"-{fps_loss}%")
        f_idx = min(int(fps_loss / 100 * (len(FPS_STATES) - 1)), len(FPS_STATES) - 1)
        fps_label, fps_color = FPS_STATES[f_idx]
        self.fps_val_lbl.setText(f"FPS: {fps_label}")
        self.fps_val_lbl.setStyleSheet(f"color:{fps_color}; font-size:11px; background:transparent;")

        # log every 4 ticks
        if t % 4 == 0:
            site_kc = self.total_kc * 0.99
            entry = random.choice(LOGS).format(
                b=random.randint(8_000_000, 9_999_999),
                s=site_kc,
                d=random.randint(1, 9),
                d2=random.randint(10, 99),
                n=random.randint(1, 64),
                t=random.randint(88, 107),
                m=random.randint(3, 14),
                p=random.randint(2, 18),
            )
            self._push_log(entry)

    def closeEvent(self, event):
        save_wallet(self.total_kc)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    p = app.palette()
    p.setColor(QPalette.Window, QColor(BG))
    p.setColor(QPalette.WindowText, QColor(WHITE))
    app.setPalette(p)
    w = MinerApp()
    w.show()
    sys.exit(app.exec())
