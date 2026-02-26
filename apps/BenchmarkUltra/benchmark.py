#!/usr/bin/env python3
"""
BenchmarkUltra π Edition
DownloadBetterPerformanceForFree — Certified by the π Institute
Always scores 6.28. No exceptions. No refunds.
"""

import sys, os, random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QStackedWidget
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
"""

# ── Benchmark tests ───────────────────────────────────────────────────────────
TESTS = [
    ("⚙️  CPU",      "Ryzen 9 92759X5D",        2600),
    ("🎮  GPU",      "RTX 5090 × 2",             2800),
    ("🧠  RAM",      "200 TB DDR7 @ −274K",      2400),
    ("💾  SSD",      "8 TB No_Scam SSD",         2200),
    ("🌍  Reality",  "INeverTouchGrass Module",  3000),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
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
        lay.addSpacing(40)

        btn = QPushButton("▶  START BENCHMARK")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedWidth(280)
        btn.clicked.connect(on_start)
        row = QHBoxLayout()
        row.addStretch(); row.addWidget(btn); row.addStretch()
        lay.addLayout(row)
        lay.addSpacing(20)

        lay.addWidget(label("ℹ  Score is calculated using the π algorithm. The result is always accurate.",
                            10, color="#333", align=Qt.AlignHCenter))
        lay.addStretch(3)

        lay.addWidget(label("v6.28  |  π Institute Certified  |  Putlin Anti-HateUSSR Lab Approved",
                            9, color="#1e1e1e", align=Qt.AlignHCenter))
        lay.addSpacing(12)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Benchmark running  (info on the left, video fills the right)
# ══════════════════════════════════════════════════════════════════════════════
class BenchmarkPage(QWidget):
    def __init__(self, on_done, video_path=None):
        super().__init__()
        self.on_done      = on_done
        self._video_path  = video_path
        self._test_idx    = 0
        self._progress    = 0
        self._tick_timer  = QTimer(); self._tick_timer.timeout.connect(self._tick)
        self._log_timer   = QTimer(); self._log_timer.timeout.connect(self._add_log)
        self._player      = None
        self._audio       = None
        self._video_widget = None

        # ── Root: horizontal split ────────────────────────────────────────
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── LEFT panel — info ─────────────────────────────────────────────
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
        for name, spec, _ in TESTS:
            top = QHBoxLayout()
            l_name = label(name, 10, bold=True, color="#777")
            l_pct  = label("  0%", 9, color=GREEN, mono=True)
            l_pct.setFixedWidth(34); l_pct.setAlignment(Qt.AlignRight)
            top.addWidget(l_name); top.addStretch(); top.addWidget(l_pct)

            bar = QProgressBar()
            bar.setRange(0, 100); bar.setValue(0)
            bar.setTextVisible(False); bar.setFixedHeight(5)

            ll.addLayout(top)
            ll.addWidget(label(spec, 8, color="#222", mono=True))
            ll.addWidget(bar)
            ll.addSpacing(11)
            self._bars.append(bar); self._pct_labels.append(l_pct)

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

        # ── RIGHT panel — video (fills remaining space) ───────────────────
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

    # ── Public API ────────────────────────────────────────────────────────────
    def start(self):
        self._test_idx = 0
        self._progress = 0
        for b in self._bars:    b.setValue(0)
        for p in self._pct_labels: p.setText("  0%")
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

    # ── Video ─────────────────────────────────────────────────────────────────
    def _start_video(self, path):
        # Tear down previous instance
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

    # ── Progress ──────────────────────────────────────────────────────────────
    def _start_test(self):
        if self._test_idx >= len(TESTS):
            self._log_timer.stop()
            self._header.setText("CALCULATING FINAL SCORE…")
            self._subheader.setText("Applying π-based normalisation algorithm…")
            QTimer.singleShot(2200, self.on_done)
            return
        _, spec, duration = TESTS[self._test_idx]
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

    # ── Log ───────────────────────────────────────────────────────────────────
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
        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 40, 60, 24)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(0)

        # ── Score card ────────────────────────────────────────────────────
        card = QFrame(); card.setObjectName("result_card")
        cl   = QVBoxLayout(card)
        cl.setAlignment(Qt.AlignCenter)
        cl.setContentsMargins(40, 28, 40, 28)
        cl.setSpacing(4)

        cl.addWidget(label("BenchmarkUltra π — FINAL SCORE", 11, bold=True,
                           color="#333", mono=True, align=Qt.AlignHCenter))
        cl.addSpacing(12)

        self._score_lbl = QLabel("0.00")
        self._score_lbl.setAlignment(Qt.AlignCenter)
        self._score_lbl.setStyleSheet(
            f"color: {GREEN}; background: transparent; "
            f"font-size: 80px; font-weight: 900; font-family: 'Segoe UI';")
        cl.addWidget(self._score_lbl)

        cl.addWidget(label("POINTS", 12, bold=True, color="#444",
                           mono=True, align=Qt.AlignHCenter))
        cl.addSpacing(6)
        cl.addWidget(label("= 2π  ·  PERFECT SCORE  ·  π INSTITUTE CERTIFIED",
                           10, color=GREEN, mono=True, align=Qt.AlignHCenter))
        cl.addSpacing(14)

        tags = QHBoxLayout(); tags.addStretch()
        for txt, col in [("World Record: 6.28", GOLD),
                         ("Holder: IKIR25",    GREEN),
                         ("HateUSSR: 0",       "#4488ff")]:
            t = QLabel(txt)
            t.setStyleSheet(f"background:{col};color:#000;border-radius:4px;"
                            f"padding:3px 10px;font-weight:700;font-size:10px;")
            tags.addWidget(t)
        tags.addStretch()
        cl.addLayout(tags)
        lay.addWidget(card)
        lay.addSpacing(20)

        # ── Per-test breakdown ────────────────────────────────────────────
        lay.addWidget(label("TEST BREAKDOWN", 9, color="#222",
                            mono=True, align=Qt.AlignHCenter))
        lay.addSpacing(10)

        row = QHBoxLayout(); row.setSpacing(10); row.addStretch()
        for test, score in [("CPU","1.26"),("GPU","1.26"),("RAM","1.25"),
                             ("SSD","1.25"),("Reality","1.26")]:
            col = QVBoxLayout(); col.setAlignment(Qt.AlignCenter); col.setSpacing(2)
            col.addWidget(label(score, 16, bold=True, color=GREEN,
                                mono=True, align=Qt.AlignHCenter))
            col.addWidget(label(test, 8, color="#333",
                                mono=True, align=Qt.AlignHCenter))
            wrap = QWidget(); wrap.setLayout(col)
            wrap.setStyleSheet("background:#0d0d0d;border:1px solid #1a1a1a;border-radius:8px;")
            wrap.setFixedWidth(90)
            row.addWidget(wrap)
        row.addStretch()
        lay.addLayout(row)
        lay.addSpacing(28)

        # ── Buttons ───────────────────────────────────────────────────────
        btn_row = QHBoxLayout(); btn_row.addStretch()
        rb = QPushButton("↺  Run Again")
        rb.setObjectName("secondary"); rb.setCursor(Qt.PointingHandCursor)
        rb.clicked.connect(on_restart)
        btn_row.addWidget(rb); btn_row.addStretch()
        lay.addLayout(btn_row)
        lay.addSpacing(16)
        lay.addWidget(label("This result cannot be disputed.  |  Kim disapproves.",
                            9, color="#1a1a1a", align=Qt.AlignHCenter))

    def show_results(self):
        self._score_val = 0.0
        self._counter = QTimer()
        self._counter.timeout.connect(self._step)
        self._counter.start(28)

    def _step(self):
        self._score_val = min(self._score_val + 0.10, 6.28)
        self._score_lbl.setText(f"{self._score_val:.2f}")
        if self._score_val >= 6.28:
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

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._t = TitlePage(self._go_bench)
        self._b = BenchmarkPage(self._go_results, video_path=video_path)
        self._r = ResultsPage(self._go_title)

        self._stack.addWidget(self._t)   # 0
        self._stack.addWidget(self._b)   # 1
        self._stack.addWidget(self._r)   # 2
        self._stack.setCurrentIndex(0)

    def _center(self):
        g = QApplication.primaryScreen().geometry()
        self.move((g.width() - self.width()) // 2,
                  (g.height() - self.height()) // 2)

    def _go_bench(self):
        self._stack.setCurrentIndex(1)
        self._b.start()

    def _go_results(self):
        self._b.stop()
        self._stack.setCurrentIndex(2)
        self._r.show_results()

    def _go_title(self):
        self._stack.setCurrentIndex(0)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════
def find_video():
    # 1. Bundled video (PyInstaller onefile extracts to sys._MEIPASS)
    try:
        bundled = os.path.join(sys._MEIPASS, "benchmark_video.webm")
        if os.path.isfile(bundled):
            return bundled
    except AttributeError:
        pass

    # 2. Same folder as the script/exe, then Desktop
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
