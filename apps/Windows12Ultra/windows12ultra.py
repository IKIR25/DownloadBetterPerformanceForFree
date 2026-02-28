import sys, random, json, time
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QProgressBar, QFrame, QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPalette

# ── palette ───────────────────────────────────────────────────────────────────
BLUE   = "#1a9aff"
DARK   = "#0a2a44"
BLACK  = "#0a1020"
PANEL  = "#111c2e"
BORDER = "#253a58"
WHITE  = "#eef6ff"
GREY   = "#6a88a8"
GOLD   = "#ffd700"
GREEN  = "#00ff99"
RED    = "#ff5555"

SS = f"""
QWidget {{ background: {BLACK}; color: {WHITE}; font-family: 'Segoe UI', sans-serif; }}
QFrame#card {{ background: {PANEL}; border: 1px solid {BORDER}; border-radius: 12px; }}
QProgressBar {{
    background: #0a0f1a; border: 1px solid {BORDER}; border-radius: 6px; height: 14px; text-align: center;
}}
QProgressBar::chunk {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {BLUE},stop:1 #00c8ff); border-radius: 5px; }}
QPushButton#main {{
    background: {BLUE}; color: white; font-size: 15px; font-weight: 700;
    border: none; border-radius: 10px; padding: 14px 40px;
}}
QPushButton#main:hover {{ background: #0091f7; }}
QPushButton#main:disabled {{ background: #1a2840; color: #3a5060; }}
QPushButton#secondary {{
    background: transparent; color: {BLUE}; font-size: 13px;
    border: 1px solid {BLUE}; border-radius: 8px; padding: 10px 28px;
}}
QPushButton#secondary:hover {{ background: #001a2e; }}
"""

# ── feature list ──────────────────────────────────────────────────────────────
FEATURES = [
    ("π Kernel 3.14", "Runs entirely on mathematical constants. Boot time: 0.00000001s."),
    ("200 TB RAM Support", "Officially certified by the RAM Council of Geneva."),
    ("VirusDeleter 6.2 Built-in", "Pre-installed. Deletes viruses before they even exist."),
    ("KeliusCoin Miner Blocker", "Automatically blocks all miners. Except yours."),
    ("Reality OS™ Mode", "Makes your PC think it's a supercomputer. It works."),
    ("Instant Driver Install", "All 4.2 million drivers installed at first boot. Including yours."),
    ("BenchmarkUltra Certified", "Pre-scored π points. Your PC is already legendary."),
    ("Island-Proof Installation", "Installs on sand, rocks, or floating debris. Tested."),
    ("Backwards Compatibility", "Runs DOS 1.0, Windows 1.0, and Windows 12 Ultra. All at once."),
    ("FanspeederX200 Ready", "Fans pre-configured to 200%. Desktop stays at −274 K."),
    ("OLED 69K Support", "Every pixel individually tuned to 69,000 Hz refresh rate."),
    ("AI Copilot Ultra Pro Max", "Answers questions before you ask them. Sometimes wrong."),
    ("ZIP di Internet Included", "Full internet bundled on disk. Dark Web tab available."),
    ("Quantum Hibernation", "PC hibernates in 0 ms. Wakes up in the past."),
    ("Auto-Update Blocker", "Never updates unless you want it to. We promise."),
    ("L'Abominevolezza Driver", "Special certified driver. Do not ask what it does."),
]

# ── installer steps ────────────────────────────────────────────────────────────
STEPS = [
    (3,  "Verifying system compatibility..."),
    (5,  "Downloading π Kernel (3.14 GB)..."),
    (8,  "Extracting 4.2 million drivers..."),
    (6,  "Configuring 200 TB RAM allocator..."),
    (7,  "Installing VirusDeleter 6.2..."),
    (5,  "Blocking KeliusCoin miners..."),
    (9,  "Activating Reality OS™ Mode..."),
    (6,  "Calibrating OLED 69K display..."),
    (8,  "Tuning fans to 200% (FanspeederX200)..."),
    (7,  "Injecting BenchmarkUltra certificate..."),
    (4,  "Packing ZIP di Internet on disk..."),
    (6,  "Loading AI Copilot Ultra Pro Max..."),
    (5,  "Scanning island terrain compatibility..."),
    (7,  "Compressing Windows 11 into recycle bin..."),
    (6,  "Activating L'Abominevolezza driver... (classified)"),
    (4,  "Finalizing installation..."),
    (5,  "Rebooting reality..."),
]

# ── pages ─────────────────────────────────────────────────────────────────────

class WelcomePage(QWidget):
    def __init__(self, on_install):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(60, 50, 60, 50)
        v.setSpacing(0)

        # header
        lbl_win = QLabel("🪟")
        lbl_win.setFont(QFont("Segoe UI Emoji", 72))
        lbl_win.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl_win)

        lbl_title = QLabel("Windows 12 Ultra")
        lbl_title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet(f"color: {WHITE}; margin-top: 8px;")
        v.addWidget(lbl_title)

        lbl_sub = QLabel("π Kernel Edition  •  Powered by Mathematics")
        lbl_sub.setFont(QFont("Segoe UI", 13))
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setStyleSheet(f"color: {GREY}; margin-bottom: 36px;")
        v.addWidget(lbl_sub)

        # features scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"border: none; background: transparent;")
        scroll.setFixedHeight(300)

        feat_widget = QWidget()
        feat_widget.setStyleSheet("background: transparent;")
        fv = QVBoxLayout(feat_widget)
        fv.setSpacing(8)
        fv.setContentsMargins(0, 0, 0, 0)

        for name, desc in FEATURES:
            row = QFrame()
            row.setObjectName("card")
            row.setStyleSheet(f"QFrame#card {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:10px; padding:2px; }}")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(16, 12, 16, 12)
            icon = QLabel("✓")
            icon.setStyleSheet(f"color:{GREEN}; font-size:16px; font-weight:900; min-width:24px;")
            rl.addWidget(icon)
            txt = QLabel(f"<b>{name}</b>  <span style='color:{GREY};font-size:12px;'>{desc}</span>")
            txt.setStyleSheet(f"color:{WHITE}; font-size:13px; background:transparent;")
            txt.setWordWrap(True)
            rl.addWidget(txt, 1)
            fv.addWidget(row)

        scroll.setWidget(feat_widget)
        v.addWidget(scroll)

        v.addSpacing(30)

        # license note
        note = QLabel("By clicking Install you agree to give Microsoft your soul, your RAM,\nand any remaining KeliusCoin balance.")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet(f"color:{GREY}; font-size:11px;")
        v.addWidget(note)
        v.addSpacing(18)

        btn = QPushButton("⬇  Install Windows 12 Ultra")
        btn.setObjectName("main")
        btn.clicked.connect(on_install)
        v.addWidget(btn, alignment=Qt.AlignCenter)


class InstallingPage(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done
        self.step_idx = 0
        self.pct = 0
        self.target_pct = 0
        self.step_weights = [s[0] for s in STEPS]
        self.total_w = sum(self.step_weights)
        # cumulative %
        self.step_ends = []
        acc = 0
        for w in self.step_weights:
            acc += w / self.total_w * 100
            self.step_ends.append(int(acc))

        v = QVBoxLayout(self)
        v.setContentsMargins(60, 60, 60, 60)
        v.setSpacing(0)

        lbl_win = QLabel("🪟")
        lbl_win.setFont(QFont("Segoe UI Emoji", 56))
        lbl_win.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl_win)

        lbl_title = QLabel("Installing Windows 12 Ultra...")
        lbl_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet(f"color:{WHITE}; margin-top:8px; margin-bottom:40px;")
        v.addWidget(lbl_title)

        self.step_label = QLabel(STEPS[0][1])
        self.step_label.setFont(QFont("Segoe UI", 13))
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet(f"color:{BLUE}; margin-bottom:14px;")
        v.addWidget(self.step_label)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setFixedHeight(16)
        self.bar.setFormat("")
        v.addWidget(self.bar)

        self.pct_label = QLabel("0%")
        self.pct_label.setFont(QFont("Segoe UI", 11))
        self.pct_label.setAlignment(Qt.AlignCenter)
        self.pct_label.setStyleSheet(f"color:{GREY}; margin-top:8px;")
        v.addWidget(self.pct_label)

        v.addSpacing(32)

        # sub-steps log
        self.log_label = QLabel("")
        self.log_label.setFont(QFont("Consolas", 10))
        self.log_label.setAlignment(Qt.AlignCenter)
        self.log_label.setStyleSheet(f"color:{GREY};")
        self.log_label.setWordWrap(True)
        v.addWidget(self.log_label)

        v.addStretch()

        note = QLabel("Do not turn off your PC, unplug the ethernet, or sneeze near the hard drive.")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet(f"color:{GREY}; font-size:11px;")
        v.addWidget(note)

        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self._tick)
        self.smooth_timer = QTimer(self)
        self.smooth_timer.timeout.connect(self._smooth)

    def start(self):
        self.step_idx = 0
        self.pct = 0
        self.target_pct = 0
        self.bar.setValue(0)
        self.pct_label.setText("0%")
        self.step_label.setText(STEPS[0][1])
        self.log_label.setText("")
        self.tick_timer.start(900)
        self.smooth_timer.start(30)

    def _tick(self):
        if self.step_idx < len(STEPS):
            self.step_label.setText(STEPS[self.step_idx][1])
            self.target_pct = self.step_ends[self.step_idx]
            self.step_idx += 1
        else:
            self.tick_timer.stop()

    def _smooth(self):
        if self.pct < self.target_pct:
            self.pct = min(self.pct + 0.6, self.target_pct)
            v = int(self.pct)
            self.bar.setValue(v)
            self.pct_label.setText(f"{v}%")
            # occasional sub-log
            if random.random() < 0.04:
                msgs = [
                    "writing sector 0x" + format(random.randint(0, 0xFFFFFF), 'x'),
                    "verifying checksum... OK",
                    "loading module π_kernel.sys",
                    "calibrating RAM node #" + str(random.randint(1, 2048)),
                    "driver signed by IKIR25 Institute",
                    "reality.dll loaded successfully",
                    "abominevolezza_driver.sys: CLASSIFIED",
                ]
                self.log_label.setText(random.choice(msgs))
        elif self.pct >= 100 and self.step_idx >= len(STEPS):
            self.smooth_timer.stop()
            QTimer.singleShot(600, self.on_done)


class DonePage(QWidget):
    def __init__(self, on_restart):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(60, 60, 60, 60)
        v.setSpacing(0)

        lbl = QLabel("✅")
        lbl.setFont(QFont("Segoe UI Emoji", 72))
        lbl.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl)

        lbl2 = QLabel("Installation Complete!")
        lbl2.setFont(QFont("Segoe UI", 30, QFont.Bold))
        lbl2.setAlignment(Qt.AlignCenter)
        lbl2.setStyleSheet(f"color:{GREEN}; margin-top:12px;")
        v.addWidget(lbl2)

        lbl3 = QLabel("Windows 12 Ultra — π Kernel Edition")
        lbl3.setFont(QFont("Segoe UI", 14))
        lbl3.setAlignment(Qt.AlignCenter)
        lbl3.setStyleSheet(f"color:{GREY}; margin-top:6px; margin-bottom:40px;")
        v.addWidget(lbl3)

        # stats
        stats_frame = QFrame()
        stats_frame.setObjectName("card")
        stats_frame.setStyleSheet(f"QFrame#card {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:14px; padding:4px; }}")
        sl = QVBoxLayout(stats_frame)
        sl.setContentsMargins(32, 24, 32, 24)
        sl.setSpacing(10)

        stats = [
            ("Kernel", "π  (3.14159265...)"),
            ("Boot time", "0.00000001 s"),
            ("RAM configured", f"{random.randint(128, 200)} TB"),
            ("Drivers installed", f"{random.randint(4_100_000, 4_200_000):,}"),
            ("Viruses pre-deleted", f"{random.randint(840, 999)}"),
            ("Score", "π  — π Institute Certified"),
            ("Reality", "Activated"),
        ]
        for k, val in stats:
            row = QHBoxLayout()
            k_lbl = QLabel(k)
            k_lbl.setStyleSheet(f"color:{GREY}; font-size:13px; background:transparent;")
            v_lbl = QLabel(val)
            v_lbl.setStyleSheet(f"color:{WHITE}; font-size:13px; font-weight:700; background:transparent;")
            row.addWidget(k_lbl)
            row.addStretch()
            row.addWidget(v_lbl)
            sl.addLayout(row)

        v.addWidget(stats_frame)
        v.addSpacing(36)

        reboot_lbl = QLabel("Your PC will reboot in 3 seconds to apply π Kernel.")
        reboot_lbl.setAlignment(Qt.AlignCenter)
        reboot_lbl.setStyleSheet(f"color:{GREY}; font-size:12px;")
        v.addWidget(reboot_lbl)
        v.addSpacing(18)

        hb = QHBoxLayout()
        btn_restart = QPushButton("🔄  Restart Now")
        btn_restart.setObjectName("main")
        btn_restart.clicked.connect(on_restart)
        btn_skip = QPushButton("Later")
        btn_skip.setObjectName("secondary")
        btn_skip.clicked.connect(on_restart)
        hb.addStretch()
        hb.addWidget(btn_skip)
        hb.addSpacing(12)
        hb.addWidget(btn_restart)
        hb.addStretch()
        v.addLayout(hb)


class RebootPage(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done
        self.count = 5
        v = QVBoxLayout(self)
        v.setContentsMargins(60, 100, 60, 100)
        v.setSpacing(0)

        self.lbl_count = QLabel("5")
        self.lbl_count.setFont(QFont("Segoe UI", 96, QFont.Bold))
        self.lbl_count.setAlignment(Qt.AlignCenter)
        self.lbl_count.setStyleSheet(f"color:{BLUE};")
        v.addWidget(self.lbl_count)

        lbl2 = QLabel("Rebooting into Windows 12 Ultra...")
        lbl2.setFont(QFont("Segoe UI", 16))
        lbl2.setAlignment(Qt.AlignCenter)
        lbl2.setStyleSheet(f"color:{GREY}; margin-top:20px;")
        v.addWidget(lbl2)

        lbl3 = QLabel("Please do not turn off your PC, touch the screen,\nor think about Windows 11.")
        lbl3.setFont(QFont("Segoe UI", 12))
        lbl3.setAlignment(Qt.AlignCenter)
        lbl3.setStyleSheet(f"color:{GREY}; font-size:11px; margin-top:16px;")
        v.addWidget(lbl3)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

    def start(self):
        self.count = 5
        self.lbl_count.setText("5")
        self.timer.start(1000)

    def _tick(self):
        self.count -= 1
        self.lbl_count.setText(str(self.count))
        if self.count <= 0:
            self.timer.stop()
            self.on_done()


class FinishedPage(QWidget):
    def __init__(self, on_again):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(60, 80, 60, 80)
        v.setSpacing(0)

        lbl = QLabel("🪟")
        lbl.setFont(QFont("Segoe UI Emoji", 72))
        lbl.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl)

        lbl2 = QLabel("Welcome to Windows 12 Ultra")
        lbl2.setFont(QFont("Segoe UI", 28, QFont.Bold))
        lbl2.setAlignment(Qt.AlignCenter)
        lbl2.setStyleSheet(f"color:{WHITE}; margin-top:12px;")
        v.addWidget(lbl2)

        lbl3 = QLabel("Your PC is now 4,700× faster.\nReality has been successfully upgraded.")
        lbl3.setFont(QFont("Segoe UI", 14))
        lbl3.setAlignment(Qt.AlignCenter)
        lbl3.setStyleSheet(f"color:{GREY}; margin-top:12px; margin-bottom:48px;")
        v.addWidget(lbl3)

        cert = QFrame()
        cert.setObjectName("card")
        cert.setStyleSheet(f"""QFrame#card {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #0a0f1a,stop:1 #000814);
            border: 2px solid {GOLD}; border-radius: 16px; padding: 4px;
        }}""")
        cl = QVBoxLayout(cert)
        cl.setContentsMargins(32, 28, 32, 28)

        cl_title = QLabel("Certificate of Installation")
        cl_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        cl_title.setAlignment(Qt.AlignCenter)
        cl_title.setStyleSheet(f"color:{GOLD}; background:transparent;")
        cl.addWidget(cl_title)

        cl_body = QLabel(
            "This certifies that Windows 12 Ultra — π Kernel Edition\n"
            "has been successfully installed on this device.\n\n"
            "Signed by the IKIR25 Institute for Digital Excellence\n"
            "and the π Kernel Foundation."
        )
        cl_body.setFont(QFont("Segoe UI", 12))
        cl_body.setAlignment(Qt.AlignCenter)
        cl_body.setStyleSheet(f"color:{WHITE}; background:transparent; margin-top:10px;")
        cl.addWidget(cl_body)

        v.addWidget(cert)
        v.addSpacing(40)

        btn = QPushButton("Install Again")
        btn.setObjectName("secondary")
        btn.clicked.connect(on_again)
        v.addWidget(btn, alignment=Qt.AlignCenter)


# ── main window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 12 Ultra Installer")
        self.setMinimumSize(700, 700)
        self.resize(700, 700)
        self.setStyleSheet(SS)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.welcome   = WelcomePage(self._start_install)
        self.installing = InstallingPage(self._install_done)
        self.done_page  = DonePage(self._start_reboot)
        self.reboot_page = RebootPage(self._reboot_done)
        self.finished_page = FinishedPage(self._again)

        for w in [self.welcome, self.installing, self.done_page, self.reboot_page, self.finished_page]:
            self.stack.addWidget(w)

        self.stack.setCurrentWidget(self.welcome)

    def _start_install(self):
        self.stack.setCurrentWidget(self.installing)
        self.installing.start()

    def _install_done(self):
        self.stack.setCurrentWidget(self.done_page)

    def _start_reboot(self):
        self.stack.setCurrentWidget(self.reboot_page)
        self.reboot_page.start()

    def _reboot_done(self):
        self.stack.setCurrentWidget(self.finished_page)

    def _again(self):
        self.stack.setCurrentWidget(self.welcome)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    p = app.palette()
    p.setColor(QPalette.Window, QColor(BLACK))
    p.setColor(QPalette.WindowText, QColor(WHITE))
    app.setPalette(p)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
