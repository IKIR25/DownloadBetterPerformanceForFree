import sys, random, math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPalette

# ── palette ───────────────────────────────────────────────────────────────────
BLACK  = "#000000"
PANEL  = "#0a0800"
BORDER = "#2a1800"
WHITE  = "#ffe8aa"
GOLD   = "#ffaa00"
DGOLD  = "#cc7700"
GREY   = "#665500"
GREEN  = "#00ff88"
RED    = "#ff4444"
ORANGE = "#ff8800"

SS = f"""
QWidget {{ background:{BLACK}; color:{WHITE}; font-family:'Segoe UI',sans-serif; }}
QFrame#panel {{
    background:{PANEL}; border:1px solid {BORDER}; border-radius:12px;
}}
QProgressBar {{
    background:#0a0500; border:1px solid {BORDER}; border-radius:5px; height:12px; text-align:center; font-size:9px;
}}
QProgressBar#hash::chunk  {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {GOLD},stop:1 #ffdd44); border-radius:4px; }}
QProgressBar#gpu::chunk   {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {ORANGE},stop:1 {RED}); border-radius:4px; }}
QProgressBar#fps::chunk   {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {RED},stop:1 #880000); border-radius:4px; }}
QPushButton#start {{
    background:{GOLD}; color:#000; font-weight:900; font-size:14px;
    border:none; border-radius:10px; padding:13px 40px;
}}
QPushButton#start:hover {{ background:#ffcc44; }}
QPushButton#stop {{
    background:transparent; color:{RED}; font-size:13px;
    border:1px solid {RED}; border-radius:10px; padding:11px 32px;
}}
QPushButton#stop:hover {{ background:#1a0000; }}
"""

HASHES = [
    "00000000a3f1b2c4d5e6...",
    "000000007e9a1b3c5d8f...",
    "0000000042abc1de2f3e...",
    "00000000deadbeef1234...",
    "000000003141592653...",
    "00000000kelius271828...",
    "000000006283185307...",
    "00000000paygood9999...",
    "00000000abominev6.7...",
    "0000000016180339887...",
]

GPU_SCREAMS = [
    "GPU: nominal",
    "GPU: warm",
    "GPU: hot",
    "GPU: very hot",
    "GPU: SCREAMING",
    "GPU: ⚠ HELP ME",
    "GPU: AAAAAAAAA",
    "GPU: I QUIT",
    "GPU: 🔥🔥🔥",
]

FPS_MSGS = [
    "FPS: 144 (normal)",
    "FPS: 80",
    "FPS: 40",
    "FPS: 12",
    "FPS: 3",
    "FPS: 0.5",
    "FPS: -9000",
    "FPS: undefined",
]


class MinerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("freeCrYptOMinerminor2paygood 2 — PayGood™ Edition")
        self.setFixedSize(680, 720)
        self.setStyleSheet(SS)

        self.mining = False
        self.tick = 0
        self.total_kc = 0.0
        self.site_kc  = 0.0
        self.hashrate  = 0.0
        self.gpu_pct   = 0
        self.fps_drop  = 0

        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(24, 20, 24, 20)
        main.setSpacing(14)

        # ── title ────────────────────────────────────────────────────────────
        title = QLabel("⛏️  freeCrYptOMinerminor2paygood 2")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{GOLD}; text-shadow: 0 0 20px {GOLD};")
        main.addWidget(title)

        sub = QLabel("PayGood™ Technology  •  Mine KeliusCoin (KC)  •  Price: $0.00")
        sub.setFont(QFont("Segoe UI", 10))
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{GREY};")
        main.addWidget(sub)

        # ── status badge ─────────────────────────────────────────────────────
        self.status_lbl = QLabel("● IDLE")
        self.status_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet(f"color:{GREY};")
        main.addWidget(self.status_lbl)

        # ── hashrate panel ───────────────────────────────────────────────────
        hash_panel = self._panel()
        hp = QVBoxLayout(hash_panel)
        hp.setContentsMargins(18, 14, 18, 14)
        hp.setSpacing(8)

        hr_top = QHBoxLayout()
        hr_lbl = QLabel("⚡ Hashrate")
        hr_lbl.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")
        self.hr_val = QLabel("0 KH/s")
        self.hr_val.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.hr_val.setStyleSheet(f"color:{GOLD}; background:transparent;")
        hr_top.addWidget(hr_lbl)
        hr_top.addStretch()
        hr_top.addWidget(self.hr_val)
        hp.addLayout(hr_top)

        self.hash_bar = QProgressBar()
        self.hash_bar.setObjectName("hash")
        self.hash_bar.setRange(0, 100)
        self.hash_bar.setValue(0)
        self.hash_bar.setFormat("")
        hp.addWidget(self.hash_bar)

        self.last_hash = QLabel("Last hash: —")
        self.last_hash.setStyleSheet(f"color:#443300; font-size:10px; font-family:Consolas; background:transparent;")
        hp.addWidget(self.last_hash)

        main.addWidget(hash_panel)

        # ── wallet panel ─────────────────────────────────────────────────────
        wallet_panel = self._panel()
        wp = QVBoxLayout(wallet_panel)
        wp.setContentsMargins(18, 14, 18, 14)
        wp.setSpacing(6)

        w_title = QLabel("🪙  Wallet — PayGood™ Distribution")
        w_title.setStyleSheet(f"color:{GOLD}; font-size:12px; font-weight:700; background:transparent;")
        wp.addWidget(w_title)

        row1 = QHBoxLayout()
        you_lbl = QLabel("You (1%)")
        you_lbl.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")
        self.you_val = QLabel("0.000000 KC  ($0.00)")
        self.you_val.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.you_val.setStyleSheet(f"color:{GREEN}; background:transparent;")
        row1.addWidget(you_lbl)
        row1.addStretch()
        row1.addWidget(self.you_val)
        wp.addLayout(row1)

        row2 = QHBoxLayout()
        site_lbl = QLabel("Sito Fidato (99%)")
        site_lbl.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")
        self.site_val = QLabel("0.000000 KC  ($0.00)")
        self.site_val.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.site_val.setStyleSheet(f"color:{GOLD}; background:transparent;")
        row2.addWidget(site_lbl)
        row2.addStretch()
        row2.addWidget(self.site_val)
        wp.addLayout(row2)

        sep = QLabel("Total mined: 0.000000 KC  —  KC price: $0.00  —  Portfolio value: $0.00")
        sep.setObjectName("totallbl")
        sep.setStyleSheet(f"color:#332200; font-size:10px; background:transparent; margin-top:4px;")
        self.total_lbl = sep
        wp.addWidget(sep)

        main.addWidget(wallet_panel)

        # ── gpu / fps panel ──────────────────────────────────────────────────
        perf_panel = self._panel()
        pp = QVBoxLayout(perf_panel)
        pp.setContentsMargins(18, 14, 18, 14)
        pp.setSpacing(8)

        p_title = QLabel("🖥️  System Impact")
        p_title.setStyleSheet(f"color:{GREY}; font-size:12px; font-weight:700; background:transparent;")
        pp.addWidget(p_title)

        gpu_row = QHBoxLayout()
        self.gpu_lbl = QLabel("GPU: 0%")
        self.gpu_lbl.setStyleSheet(f"color:{ORANGE}; font-size:11px; font-weight:700; background:transparent;")
        self.gpu_scream = QLabel("GPU: nominal")
        self.gpu_scream.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")
        gpu_row.addWidget(self.gpu_lbl)
        gpu_row.addStretch()
        gpu_row.addWidget(self.gpu_scream)
        pp.addLayout(gpu_row)

        self.gpu_bar = QProgressBar()
        self.gpu_bar.setObjectName("gpu")
        self.gpu_bar.setRange(0, 100)
        self.gpu_bar.setValue(0)
        self.gpu_bar.setFormat("")
        pp.addWidget(self.gpu_bar)

        pp.addSpacing(6)

        fps_row = QHBoxLayout()
        self.fps_lbl = QLabel("FPS Impact: 0%")
        self.fps_lbl.setStyleSheet(f"color:{RED}; font-size:11px; font-weight:700; background:transparent;")
        self.fps_msg = QLabel("FPS: 144 (normal)")
        self.fps_msg.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")
        fps_row.addWidget(self.fps_lbl)
        fps_row.addStretch()
        fps_row.addWidget(self.fps_msg)
        pp.addLayout(fps_row)

        self.fps_bar = QProgressBar()
        self.fps_bar.setObjectName("fps")
        self.fps_bar.setRange(0, 100)
        self.fps_bar.setValue(0)
        self.fps_bar.setFormat("")
        pp.addWidget(self.fps_bar)

        main.addWidget(perf_panel)

        # ── log strip ────────────────────────────────────────────────────────
        log_panel = self._panel()
        lp = QVBoxLayout(log_panel)
        lp.setContentsMargins(18, 10, 18, 10)
        self.log_lbl = QLabel("Miner idle. Click Start to begin PayGood™ enrichment.")
        self.log_lbl.setStyleSheet(f"color:#443300; font-size:10px; font-family:Consolas; background:transparent;")
        self.log_lbl.setWordWrap(True)
        lp.addWidget(self.log_lbl)
        main.addWidget(log_panel)

        # ── disclaimer ───────────────────────────────────────────────────────
        disc = QLabel("⚠  PayGood™: 99% of mined KC goes directly to the Sito Fidato. You receive 1% (worth $0.00).\nGPU may scream. FPS may reach -9000. KeliusCoin price guaranteed stable at $0.00.")
        disc.setAlignment(Qt.AlignCenter)
        disc.setStyleSheet(f"color:#332200; font-size:10px;")
        disc.setWordWrap(True)
        main.addWidget(disc)

        # ── buttons ──────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        self.btn_start = QPushButton("⛏  START MINING")
        self.btn_start.setObjectName("start")
        self.btn_start.clicked.connect(self._start)
        self.btn_stop = QPushButton("■  Stop")
        self.btn_stop.setObjectName("stop")
        self.btn_stop.clicked.connect(self._stop)
        self.btn_stop.setEnabled(False)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_stop)
        btn_row.addSpacing(12)
        btn_row.addWidget(self.btn_start)
        btn_row.addStretch()
        main.addLayout(btn_row)

        # ── timer ────────────────────────────────────────────────────────────
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

    def _panel(self):
        f = QFrame()
        f.setObjectName("panel")
        return f

    def _start(self):
        self.mining = True
        self.tick = 0
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_lbl.setText("● MINING")
        self.status_lbl.setStyleSheet(f"color:{GOLD}; text-shadow: 0 0 12px {GOLD};")
        self.timer.start(200)

    def _stop(self):
        self.mining = False
        self.timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status_lbl.setText("● STOPPED")
        self.status_lbl.setStyleSheet(f"color:{RED};")
        self.gpu_bar.setValue(0)
        self.fps_bar.setValue(0)
        self.gpu_lbl.setText("GPU: 0%")
        self.fps_lbl.setText("FPS Impact: 0%")
        self.gpu_scream.setText("GPU: nominal")
        self.fps_msg.setText("FPS: 144 (normal)")
        self.log_lbl.setText("Mining stopped. KC stays in wallet. Sito Fidato says: grazie.")

    def _tick(self):
        self.tick += 1
        t = self.tick

        # hashrate — ramps up then wobbles
        base_hr = min(t * 3.5, 280) + random.uniform(-15, 15)
        self.hashrate = max(0, base_hr)
        hr_pct = min(int(self.hashrate / 300 * 100), 100)
        self.hash_bar.setValue(hr_pct)

        if self.hashrate >= 1000:
            self.hr_val.setText(f"{self.hashrate/1000:.2f} MH/s")
        else:
            self.hr_val.setText(f"{self.hashrate:.1f} KH/s")

        # last hash
        if t % 3 == 0:
            self.last_hash.setText("Last hash: " + random.choice(HASHES))

        # mine KC every tick
        mined = self.hashrate * 0.000001 * random.uniform(0.8, 1.2)
        self.total_kc += mined
        you_kc   = self.total_kc * 0.01
        site_kc  = self.total_kc * 0.99

        self.you_val.setText(f"{you_kc:.6f} KC  ($0.00)")
        self.site_val.setText(f"{site_kc:.6f} KC  ($0.00)")
        self.total_lbl.setText(
            f"Total mined: {self.total_kc:.6f} KC  —  KC price: $0.00  —  Portfolio value: $0.00"
        )

        # gpu ramps to ~95% and screams
        gpu_target = min(95, t * 2 + random.randint(-3, 3))
        self.gpu_pct = max(0, min(100, gpu_target))
        self.gpu_bar.setValue(self.gpu_pct)
        self.gpu_lbl.setText(f"GPU: {self.gpu_pct}%")
        scream_idx = min(int(self.gpu_pct / 100 * (len(GPU_SCREAMS) - 1)), len(GPU_SCREAMS) - 1)
        self.gpu_scream.setText(GPU_SCREAMS[scream_idx])
        if self.gpu_pct > 80:
            self.gpu_scream.setStyleSheet(f"color:{RED}; font-size:11px; font-weight:700; background:transparent;")
        else:
            self.gpu_scream.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")

        # fps drops inversely
        fps_loss = min(100, int(self.gpu_pct * 1.05))
        self.fps_bar.setValue(fps_loss)
        self.fps_lbl.setText(f"FPS Impact: -{fps_loss}%")
        fps_idx = min(int(fps_loss / 100 * (len(FPS_MSGS) - 1)), len(FPS_MSGS) - 1)
        self.fps_msg.setText(FPS_MSGS[fps_idx])
        if fps_loss > 80:
            self.fps_msg.setStyleSheet(f"color:{RED}; font-size:11px; font-weight:700; background:transparent;")
        else:
            self.fps_msg.setStyleSheet(f"color:{GREY}; font-size:11px; background:transparent;")

        # log
        logs = [
            f"block #{random.randint(8_000_000, 9_999_999)} submitted to KeliusChain",
            f"PayGood™ routing {site_kc:.4f} KC → Sito Fidato...",
            f"difficulty adjusted to {random.randint(1,9)}.{random.randint(10,99)}T",
            f"peer kelius-node-{random.randint(1,64)}.fidato.kc connected",
            f"GPU temp: {random.randint(88,104)}°C — cooling: insufficient",
            f"KeliusCoin network: {random.randint(3,14)} active miners (including you)",
            f"your share: 1% — sito share: 99% — logic: PayGood™",
            f"FanspeederX200 recommended at this temperature",
            f"wallet balance updated: $0.00",
            f"abominevolezza_mining_node.sys: active",
        ]
        if t % 4 == 0:
            self.log_lbl.setText(random.choice(logs))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    p = app.palette()
    p.setColor(QPalette.Window, QColor(BLACK))
    p.setColor(QPalette.WindowText, QColor(WHITE))
    app.setPalette(p)
    w = MinerApp()
    w.show()
    sys.exit(app.exec())
