#!/usr/bin/env python3
"""
BenchmarkUltra π Edition
DownloadBetterPerformanceForFree — Certified by the π Institute
Score varies. Results are always accurate. No refunds.
"""

import sys, os, random, json
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QStackedWidget, QLineEdit
)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

# ── Palette ───────────────────────────────────────────────────────────────────
GREEN  = "#00ff88"
DARK   = "#0a0a0a"
CARD   = "#111111"
GOLD   = "#ffd700"

QSS = f"""
QWidget {{
    background-color: {DARK};
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}}
QLabel {{
    background: transparent;
}}
QPushButton {{
    background-color: {GREEN};
    color: #000;
    border: none;
    border-radius: 8px;
    font-weight: 900;
    font-size: 15px;
    padding: 14px 36px;
    letter-spacing: 1px;
}}
QPushButton:hover  {{ background-color: #33ffaa; }}
QPushButton:pressed {{ background-color: #00cc66; }}
QPushButton#secondary {{
    background-color: transparent;
    color: #444;
    border: 1px solid #222;
    font-size: 12px;
    padding: 8px 20px;
}}
QPushButton#secondary:hover {{
    color: {GREEN};
    border-color: {GREEN};
}}
QProgressBar {{
    background-color: #111;
    border: 1px solid #1e3a1e;
    border-radius: 3px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {GREEN}, stop:1 #00cc66);
    border-radius: 3px;
}}
QFrame#result_card {{
    background-color: #080808;
    border: 2px solid {GREEN};
    border-radius: 16px;
}}
QLineEdit {{
    background-color: #111;
    color: #aaa;
    border: 1px solid #222;
    border-radius: 6px;
    padding: 7px 14px;
    font-size: 13px;
}}
QLineEdit:focus {{
    border-color: {GREEN};
    color: #e0e0e0;
}}
"""

# ── Score pool ─────────────────────────────────────────────────────────────────
SCORES = [
    (3.14159,  "π",       "π Institute Certified"),
    (6.28318,  "2π",      "World Record · 2π Certified"),
    (9.42477,  "3π",      "LEGENDARY — Triple-π"),
    (1.57079,  "π/2",     "Half-π Certified"),
    (2.71828,  "e",       "Euler Institute Certified"),
    (1.41421,  "√2",      "Root Institute Certified"),
    (2.30258,  "ln(10)",  "Natural Log Institute"),
    (0.31830,  "1/π",     "Inverse-π Certified"),
    (1.61803,  "φ",       "Golden Ratio Institute"),
]

# ── Hardware pools ─────────────────────────────────────────────────────────────
CPU_POOL = [
    "Ryzen 9 92759X5D", "Core Ultra 9 285K", "Ryzen AI 9 HX 475",
    "Xeon W-5595X × 2", "Apple M4 Ultra (borrowed)", "Qualcomm X Elite (confused)",
    "Intel Arc (ironic)", "Ryzen Threadripper 7995WX",
]
GPU_POOL = [
    "RTX 5090 × 2", "RX 9070 XT", "RTX 4090 Ti (doesn't exist)",
    "GTX 480 (brave choice)", "Intel Arc B580 × 4", "RTX 5080 (found on street)",
    "Radeon VII (vintage)", "RTX 3090 Ti × 3",
]
RAM_POOL = [
    "200 TB DDR7 @ −274K", "64 GB DDR5-8400",
    "128 GB DDR5-6000 OC", "32 GB DDR4-3600 (bottleneck)",
    "16 TB LPDDR6X (server memory installed incorrectly)",
    "4 GB DDR3 (historical artifact)", "96 GB DDR5-5600",
]
SSD_POOL = [
    "8 TB No_Scam SSD", "Samsung 990 Pro 4 TB",
    "WD Black SN850X 8 TB", "Seagate HDD 500 GB (brave)",
    "PCIe 5.0 NVMe 12 TB", "16× USB drives in RAID 0",
    "NVMe Optane (RIP)", "2× Samsung 990 Pro in RAID 0",
]
REALITY_POOL = [
    "INeverTouchGrass Module", "Basement Dweller v2.0",
    "Social Life: Not Found", "Skill Issue Detector v6.28",
    "Touch Grass Sensor (OFFLINE)", "π Reality Distortion Field",
    "Delusion Engine 3000", "YesItWorks Trust Me Module",
]

TEST_NAMES = ["⚙️  CPU", "🎮  GPU", "🧠  RAM", "💾  SSD", "🌍  Reality"]
TEST_DURATIONS = [2600, 2800, 2400, 2200, 3000]

# ── History ───────────────────────────────────────────────────────────────────
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".benchmarkultra_history.json")

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_score(pc_name, score_val, score_name):
    history = load_history()
    history.append({
        "pc": pc_name or "Unknown PC",
        "score": score_val,
        "name": score_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    history = history[-20:]  # keep last 20
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

# ── Helpers ───────────────────────────────────────────────────────────────────
def generate_tests():
    specs = [
        random.choice(CPU_POOL),
        random.choice(GPU_POOL),
        random.choice(RAM_POOL),
        random.choice(SSD_POOL),
        random.choice(REALITY_POOL),
    ]
    return [(TEST_NAMES[i], specs[i], TEST_DURATIONS[i]) for i in range(5)]

def make_breakdown(score_val):
    """Distribute score_val across 5 tests with random variance (sum = score_val)."""
    weights = [random.uniform(0.15, 0.25) for _ in range(5)]
    total = sum(weights)
    parts = [score_val * w / total for w in weights]
    # round to 2dp and fix rounding error on last
    parts = [round(p, 2) for p in parts]
    diff = round(score_val - sum(parts), 2)
    parts[-1] = round(parts[-1] + diff, 2)
    return parts

def label(text, size=13, bold=False, color="#e0e0e0", mono=False, align=Qt.AlignLeft):
    lbl = QLabel(text)
    font = QFont("Courier New" if mono else "Segoe UI", size)
    font.setBold(bold)
    lbl.setFont(font)
    lbl.setStyleSheet(f"color: {color}; background: transparent;")
    lbl.setAlignment(align)
    return lbl

def hline():
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet("color: #1a2a1a; background: #1a2a1a; max-height: 1px;")
    return f

def vline():
    f = QFrame()
    f.setFrameShape(QFrame.VLine)
    f.setStyleSheet("color: #111; background: #111; max-width: 1px;")
    return f


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Title
# ══════════════════════════════════════════════════════════════════════════════
class TitlePage(QWidget):
    def __init__(self, on_start):
        super().__init__()
        self._on_start = on_start
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(0)
        lay.addStretch(2)

        badge = label("π", 72, bold=True, color=GREEN, align=Qt.AlignHCenter)
        badge.setStyleSheet(f"color: {GREEN}; background: transparent;")
        lay.addWidget(badge)
        lay.addSpacing(10)

        lay.addWidget(label("BenchmarkUltra", 36, bold=True, color="#ffffff",
                            align=Qt.AlignHCenter))

        sub = label("π  E D I T I O N", 14, bold=True, color=GREEN,
                    mono=True, align=Qt.AlignHCenter)
        sub.setStyleSheet(f"color: {GREEN}; background: transparent; letter-spacing: 6px;")
        lay.addWidget(sub)
        lay.addSpacing(6)

        tagline = label(
            "DownloadBetterPerformanceForFree — Certified benchmark suite\n"
            "Endorsed by IlonMisk · Putlin · JeffEinstein · Trimp",
            11, color="#444", align=Qt.AlignHCenter)
        tagline.setWordWrap(True)
        lay.addWidget(tagline)
        lay.addSpacing(30)

        # PC Name input
        name_row = QHBoxLayout()
        name_row.addStretch()
        self._pc_name = QLineEdit()
        self._pc_name.setPlaceholderText("Enter your PC name (optional)")
        self._pc_name.setFixedWidth(280)
        self._pc_name.setMaxLength(32)
        name_row.addWidget(self._pc_name)
        name_row.addStretch()
        lay.addLayout(name_row)
        lay.addSpacing(14)

        btn = QPushButton("▶  START BENCHMARK")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedWidth(280)
        btn.clicked.connect(self._start)
        row = QHBoxLayout()
        row.addStretch(); row.addWidget(btn); row.addStretch()
        lay.addLayout(row)
        lay.addSpacing(20)

        lay.addWidget(label("ℹ  Score is calculated using the π algorithm. The result is always accurate.",
                            10, color="#333", align=Qt.AlignHCenter))
        lay.addSpacing(20)

        # History
        lay.addWidget(hline())
        lay.addSpacing(8)
        self._hist_layout = QVBoxLayout()
        self._hist_layout.setSpacing(2)
        lay.addLayout(self._hist_layout)
        lay.addSpacing(8)

        lay.addStretch(3)
        lay.addWidget(label("v6.28  |  π Institute Certified  |  Putlin Anti-HateUSSR Lab Approved",
                            9, color="#1e1e1e", align=Qt.AlignHCenter))
        lay.addSpacing(12)

    def _start(self):
        self._on_start(self._pc_name.text().strip())

    def refresh_history(self):
        # Clear old widgets
        while self._hist_layout.count():
            item = self._hist_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        history = load_history()
        if not history:
            self._hist_layout.addWidget(
                label("No previous runs.", 9, color="#222", mono=True, align=Qt.AlignHCenter))
            return

        self._hist_layout.addWidget(
            label("RECENT RUNS", 8, color="#222", mono=True, align=Qt.AlignHCenter))
        for entry in reversed(history[-5:]):
            txt = f"{entry['date']}  ·  {entry['pc']}  ·  {entry['score']:.5f} ({entry['name']})"
            self._hist_layout.addWidget(
                label(txt, 8, color="#2a2a2a", mono=True, align=Qt.AlignHCenter))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Benchmark running
# ══════════════════════════════════════════════════════════════════════════════
class BenchmarkPage(QWidget):
    def __init__(self, on_done, video_path=None):
        super().__init__()
        self.on_done      = on_done
        self._video_path  = video_path
        self._test_idx    = 0
        self._progress    = 0
        self._tests       = []
        self._tick_timer  = QTimer(); self._tick_timer.timeout.connect(self._tick)
        self._log_timer   = QTimer(); self._log_timer.timeout.connect(self._add_log)
        self._player      = None
        self._audio       = None
        self._video_widget = None

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # LEFT panel
        left = QWidget()
        left.setFixedWidth(360)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(26, 26, 20, 12)
        ll.setSpacing(0)

        self._header = label("BENCHMARK IN PROGRESS…", 12, bold=True, color=GREEN, mono=True)
        ll.addWidget(self._header)
        ll.addSpacing(2)
        self._subheader = label("Initializing…", 9, color="#444", mono=True)
        ll.addWidget(self._subheader)
        ll.addSpacing(18)

        self._bars       = []
        self._pct_labels = []
        self._spec_labels = []
        for name in TEST_NAMES:
            top = QHBoxLayout()
            l_name = label(name, 10, bold=True, color="#777")
            l_pct  = label("  0%", 9, color=GREEN, mono=True)
            l_pct.setFixedWidth(34); l_pct.setAlignment(Qt.AlignRight)
            top.addWidget(l_name); top.addStretch(); top.addWidget(l_pct)

            bar = QProgressBar()
            bar.setRange(0, 100); bar.setValue(0)
            bar.setTextVisible(False); bar.setFixedHeight(5)

            spec_lbl = label("—", 8, color="#222", mono=True)

            ll.addLayout(top)
            ll.addWidget(spec_lbl)
            ll.addWidget(bar)
            ll.addSpacing(11)
            self._bars.append(bar)
            self._pct_labels.append(l_pct)
            self._spec_labels.append(spec_lbl)

        ll.addWidget(hline())
        ll.addSpacing(7)
        ll.addWidget(label("SYSTEM LOG", 8, color="#1c1c1c", mono=True))
        ll.addSpacing(3)

        self._log_widget = QVBoxLayout()
        self._log_widget.setSpacing(2)
        self._log_lines  = []
        ll.addLayout(self._log_widget)

        ll.addStretch()
        ll.addWidget(hline())
        ll.addSpacing(5)
        ll.addWidget(label("Do not turn off your PC.", 8, color="#191919", mono=True))
        ll.addSpacing(4)

        root.addWidget(left)
        root.addWidget(vline())

        # RIGHT panel — video
        self._right = QWidget()
        self._right.setStyleSheet("background: #000;")
        self._rl = QVBoxLayout(self._right)
        self._rl.setContentsMargins(0, 0, 0, 0)
        self._rl.setSpacing(0)

        self._placeholder = label(
            "[ No video found ]\n\nPlace a .mp4 / .webm\non your Desktop.",
            12, color="#1a1a1a", mono=True, align=Qt.AlignCenter)
        self._placeholder.setWordWrap(True)
        self._rl.addWidget(self._placeholder)

        root.addWidget(self._right, stretch=1)

    def start(self, tests):
        self._tests = tests
        self._test_idx = 0
        self._progress = 0
        for b in self._bars:    b.setValue(0)
        for p in self._pct_labels: p.setText("  0%")
        for i, (_, spec, _) in enumerate(tests):
            self._spec_labels[i].setText(spec)
        self._header.setText("BENCHMARK IN PROGRESS…")
        self._subheader.setText("Initializing…")
        self._start_test()
        self._log_timer.start(380)
        if self._video_path and os.path.isfile(self._video_path):
            self._start_video(self._video_path)

    def stop(self):
        self._tick_timer.stop()
        self._log_timer.stop()
        if self._player:
            self._player.stop()

    def _start_video(self, path):
        if self._video_widget:
            self._rl.removeWidget(self._video_widget)
            self._video_widget.deleteLater()
            self._video_widget = None
        if self._player:
            self._player.stop()
            self._player.deleteLater()
            self._player = None

        self._placeholder.hide()

        self._video_widget = QVideoWidget()
        self._rl.addWidget(self._video_widget)

        self._audio = QAudioOutput()
        self._audio.setVolume(1.0)

        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio)
        self._player.setVideoOutput(self._video_widget)
        self._player.setSource(QUrl.fromLocalFile(os.path.abspath(path)))
        self._player.play()

    def _start_test(self):
        if self._test_idx >= len(self._tests):
            self._log_timer.stop()
            self._header.setText("CALCULATING FINAL SCORE…")
            self._subheader.setText("Applying π-based normalisation algorithm…")
            QTimer.singleShot(2200, self.on_done)
            return
        _, spec, duration = self._tests[self._test_idx]
        self._progress = 0
        self._subheader.setText(f"Testing: {spec}")
        self._tick_timer.start(duration // 100)

    def _tick(self):
        self._progress += 1
        idx = self._test_idx
        self._bars[idx].setValue(self._progress)
        self._pct_labels[idx].setText(f"{self._progress:3d}%")
        if self._progress >= 100:
            self._tick_timer.stop()
            self._test_idx += 1
            QTimer.singleShot(160, self._start_test)

    _LOG = [
        "[ OK ] CPU temp: {r1}°C  |  Throttle: none",
        "[ OK ] GPU mem: {r2} MB / 24576 MB",
        "[ OK ] RAM ch{r3}: {r4} GB/s",
        "[INFO] SSD IOPS: {r6}  |  queue: {r5}",
        "[ OK ] Reality hash: 0x{r7}",
        "[INFO] Pixels: {r8} π-units",
        "[ OK ] HateUSSR modules: 0 found",
        "[INFO] KeliusCoin miner: disabled",
        "[ OK ] FanspeederX200: {r9} RPM",
        "[ OK ] VirusDeleter: 3.14 viruses removed",
        "[INFO] Thread {r3}: running at −274K",
        "[ OK ] No_Scam integrity: VERIFIED",
        "[INFO] π-normalizer: pass {r3} of {r5}",
        "[ OK ] Putlin approval: GRANTED",
    ]

    def _add_log(self):
        r  = lambda a, b: random.randint(a, b)
        msg = random.choice(self._LOG).format(
            r1=r(42,89), r2=r(4000,23000), r3=r(1,8),
            r4=r(50,320), r5=r(16,128), r6=r(100000,999999),
            r7=hex(random.randint(0xabc000,0xffffff))[2:].upper(),
            r8=r(10000,99999), r9=r(2000,6900))
        lbl = label(msg, 9, color="#262626", mono=True)
        if len(self._log_lines) >= 5:
            old = self._log_lines.pop(0)
            self._log_widget.removeWidget(old)
            old.deleteLater()
        self._log_widget.addWidget(lbl)
        self._log_lines.append(lbl)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Results
# ══════════════════════════════════════════════════════════════════════════════
class ResultsPage(QWidget):
    def __init__(self, on_restart):
        super().__init__()
        self._on_restart = on_restart
        self._target     = 6.28318
        self._score_val  = 0.0
        self._counter    = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 40, 60, 24)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(0)

        # Score card
        card = QFrame(); card.setObjectName("result_card")
        cl   = QVBoxLayout(card)
        cl.setAlignment(Qt.AlignCenter)
        cl.setContentsMargins(40, 28, 40, 28)
        cl.setSpacing(4)

        cl.addWidget(label("BenchmarkUltra π — FINAL SCORE", 11, bold=True,
                           color="#333", mono=True, align=Qt.AlignHCenter))
        cl.addSpacing(12)

        self._score_lbl = QLabel("0.00000")
        self._score_lbl.setAlignment(Qt.AlignCenter)
        self._score_lbl.setStyleSheet(
            f"color: {GREEN}; background: transparent; "
            f"font-size: 72px; font-weight: 900; font-family: 'Segoe UI';")
        cl.addWidget(self._score_lbl)

        cl.addWidget(label("POINTS", 12, bold=True, color="#444",
                           mono=True, align=Qt.AlignHCenter))
        cl.addSpacing(6)

        self._cert_lbl = label("= 2π  ·  PERFECT SCORE  ·  π INSTITUTE CERTIFIED",
                               10, color=GREEN, mono=True, align=Qt.AlignHCenter)
        cl.addWidget(self._cert_lbl)
        cl.addSpacing(14)

        self._tags_row = QHBoxLayout(); self._tags_row.addStretch()
        self._tag_score = self._make_tag("Score: 6.28318", GOLD)
        self._tag_name  = self._make_tag("2π Certified", GREEN)
        self._tag_hate  = self._make_tag("HateUSSR: 0", "#4488ff")
        for t in (self._tag_score, self._tag_name, self._tag_hate):
            self._tags_row.addWidget(t)
        self._tags_row.addStretch()
        cl.addLayout(self._tags_row)
        lay.addWidget(card)
        lay.addSpacing(20)

        # Per-test breakdown
        lay.addWidget(label("TEST BREAKDOWN", 9, color="#222",
                            mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(10)

        self._breakdown_row = QHBoxLayout()
        self._breakdown_row.setSpacing(10)
        self._breakdown_row.addStretch()
        self._breakdown_lbls = []
        for name in ["CPU", "GPU", "RAM", "SSD", "Reality"]:
            col = QVBoxLayout(); col.setAlignment(Qt.AlignCenter); col.setSpacing(2)
            val_lbl = label("—", 16, bold=True, color=GREEN,
                            mono=True, align=Qt.AlignHCenter)
            col.addWidget(val_lbl)
            col.addWidget(label(name, 8, color="#333",
                                mono=True, align=Qt.AlignHCenter))
            wrap = QWidget(); wrap.setLayout(col)
            wrap.setStyleSheet("background:#0d0d0d;border:1px solid #1a1a1a;border-radius:8px;")
            wrap.setFixedWidth(90)
            self._breakdown_row.addWidget(wrap)
            self._breakdown_lbls.append(val_lbl)
        self._breakdown_row.addStretch()
        lay.addLayout(self._breakdown_row)
        lay.addSpacing(20)

        # History
        self._hist_layout = QVBoxLayout()
        self._hist_layout.setSpacing(2)
        lay.addLayout(self._hist_layout)
        lay.addSpacing(12)

        # Buttons
        btn_row = QHBoxLayout(); btn_row.addStretch()
        rb = QPushButton("↺  Run Again")
        rb.setObjectName("secondary"); rb.setCursor(Qt.PointingHandCursor)
        rb.clicked.connect(on_restart)
        btn_row.addWidget(rb); btn_row.addStretch()
        lay.addLayout(btn_row)
        lay.addSpacing(10)
        lay.addWidget(label("This result cannot be disputed.  |  Kim disapproves.",
                            9, color="#1a1a1a", align=Qt.AlignHCenter))

    def _make_tag(self, txt, col):
        t = QLabel(txt)
        t.setStyleSheet(f"background:{col};color:#000;border-radius:4px;"
                        f"padding:3px 10px;font-weight:700;font-size:10px;")
        return t

    def show_results(self, score_val, score_name, score_cert, breakdown, pc_name):
        self._target    = score_val
        self._score_val = 0.0
        self._step      = score_val / 63  # ~63 steps

        self._cert_lbl.setText(f"= {score_name}  ·  {score_cert}")
        self._tag_score.setText(f"Score: {score_val:.5f}")
        self._tag_name.setText(score_name)

        for i, val in enumerate(breakdown):
            self._breakdown_lbls[i].setText(f"{val:.2f}")

        # History display
        while self._hist_layout.count():
            item = self._hist_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        history = load_history()
        if history:
            self._hist_layout.addWidget(
                label("HISTORY", 8, color="#222", mono=True, align=Qt.AlignHCenter))
            for entry in reversed(history[-3:]):
                txt = f"{entry['date']}  ·  {entry['pc']}  ·  {entry['score']:.5f} ({entry['name']})"
                self._hist_layout.addWidget(
                    label(txt, 8, color="#2a2a2a", mono=True, align=Qt.AlignHCenter))

        if self._counter:
            self._counter.stop()
        self._counter = QTimer()
        self._counter.timeout.connect(self._step_anim)
        self._counter.start(22)

    def _step_anim(self):
        self._score_val = min(self._score_val + self._step, self._target)
        self._score_lbl.setText(f"{self._score_val:.5f}")
        if self._score_val >= self._target:
            self._score_lbl.setText(f"{self._target:.5f}")
            self._counter.stop()


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self, video_path=None):
        super().__init__()
        self.setWindowTitle("BenchmarkUltra π Edition")
        self.setMinimumSize(860, 580)
        self.resize(1000, 680)
        self._center()
        self._pc_name = ""
        self._tests   = []
        self._score   = None

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._t = TitlePage(self._go_bench)
        self._b = BenchmarkPage(self._go_results, video_path=video_path)
        self._r = ResultsPage(self._go_title)

        self._stack.addWidget(self._t)   # 0
        self._stack.addWidget(self._b)   # 1
        self._stack.addWidget(self._r)   # 2
        self._stack.setCurrentIndex(0)
        self._t.refresh_history()

    def _center(self):
        g = QApplication.primaryScreen().geometry()
        self.move((g.width() - self.width()) // 2,
                  (g.height() - self.height()) // 2)

    def _go_bench(self, pc_name):
        self._pc_name = pc_name or "Anonymous PC"
        self._score   = random.choice(SCORES)
        self._tests   = generate_tests()
        self._stack.setCurrentIndex(1)
        self._b.start(self._tests)

    def _go_results(self):
        self._b.stop()
        score_val, score_name, score_cert = self._score
        breakdown = make_breakdown(score_val)
        save_score(self._pc_name, score_val, score_name)
        self._stack.setCurrentIndex(2)
        self._r.show_results(score_val, score_name, score_cert, breakdown, self._pc_name)

    def _go_title(self):
        self._t.refresh_history()
        self._stack.setCurrentIndex(0)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════
def find_video():
    try:
        bundled = os.path.join(sys._MEIPASS, "benchmark_video.webm")
        if os.path.isfile(bundled):
            return bundled
    except AttributeError:
        pass

    exts = (".mp4", ".avi", ".mkv", ".mov", ".webm", ".wmv", ".m4v")
    for folder in (os.path.dirname(os.path.abspath(sys.argv[0])),
                   os.path.expanduser("~/Desktop")):
        try:
            for f in os.listdir(folder):
                if f.lower().endswith(exts):
                    return os.path.join(folder, f)
        except OSError:
            pass
    return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    win = MainWindow(video_path=find_video())
    win.show()
    sys.exit(app.exec())
