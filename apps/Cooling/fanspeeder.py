"""
FanspeederX200 3.104
"Le ventole giravano a una velocità tale da generare portanza."
— L'Abominevolezza, Cap. 4
"""
import sys, ctypes, re, subprocess, json, math, time
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPainterPath

# ── Palette ─────────────────────────────────────────────────────────────────
BG     = "#070a0d"
CYAN   = "#00ccff"
ORANGE = "#ff8800"
RED    = "#ff3333"
GREEN  = "#00ff88"
WHITE  = "#ddeeff"
GREY   = "#445566"
PANEL  = "#0d1520"

COOLING_FILE = Path.home() / ".dbpff_cooling.json"

# ── Power plan GUIDs ─────────────────────────────────────────────────────────
PLAN_BALANCED  = "381b4222-f694-41f0-9685-ff5bb260df2e"
PLAN_HIGH      = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
PLAN_ULTIMATE  = "e9a42b02-d5df-448d-aa00-03f14749eb61"

MODES = {
    "Normal": {"plan": PLAN_BALANCED, "rpm": 2200,  "risk": 3,  "color": GREEN,  "acer": False},
    "Turbo":  {"plan": PLAN_HIGH,     "rpm": 5100,  "risk": 44, "color": ORANGE, "acer": False},
    "X200":   {"plan": PLAN_ULTIMATE, "rpm": 9400,  "risk": 99, "color": RED,    "acer": True},
}

# ── Admin ────────────────────────────────────────────────────────────────────
def is_admin() -> bool:
    try:    return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except: return False

def relaunch_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(f'"{a}"' for a in sys.argv), None, 1
    )
    sys.exit()

# ── Power plan helpers ────────────────────────────────────────────────────────
def get_active_plan() -> str:
    try:
        r = subprocess.run(["powercfg", "/getactivescheme"],
                           capture_output=True, text=True, shell=True)
        m = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
                      r.stdout, re.I)
        return m.group(1).lower() if m else PLAN_BALANCED
    except:
        return PLAN_BALANCED

def set_plan(guid: str) -> bool:
    try:
        # Create Ultimate Performance if missing
        if guid.lower() == PLAN_ULTIMATE:
            r = subprocess.run(["powercfg", "/list"], capture_output=True, text=True, shell=True)
            if PLAN_ULTIMATE not in r.stdout.lower():
                subprocess.run(["powercfg", "/duplicatescheme", PLAN_ULTIMATE],
                               capture_output=True, shell=True)
        result = subprocess.run(["powercfg", "/setactive", guid],
                                capture_output=True, shell=True)
        return result.returncode == 0
    except:
        return False

# ── Acer WMI turbo ───────────────────────────────────────────────────────────
def acer_set_turbo(enable: bool):
    """Try to activate Acer Nitro's Turbo fan mode via WMI."""
    val = 3 if enable else 1   # Acer: 0=Quiet 1=Normal 2=Perf 3=Turbo
    ps = f"""
$ErrorActionPreference = 'SilentlyContinue'
# Try known Acer Nitro WMI class names
$classes = @('WMID_OEM_POWER_MODE','WmiAcerFan','AcerThermalControl','WMID_GetSetFunc')
foreach ($cls in $classes) {{
    $obj = Get-WmiObject -Namespace 'root\\WMI' -Class $cls -ErrorAction SilentlyContinue
    if ($obj) {{
        # Try common method names
        foreach ($method in @('ChangePowerMode','SetPowerMode','SetThermalMode')) {{
            try {{ $obj.$method({val}) | Out-Null; break }} catch {{}}
        }}
        break
    }}
}}
# Also try NitroSense COM interface
try {{
    $nitro = New-Object -ComObject AcerNitroPowerMonitor -ErrorAction SilentlyContinue
    if ($nitro) {{ $nitro.SetFanMode({val}) | Out-Null }}
}} catch {{}}
"""
    subprocess.Popen(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                     creationflags=subprocess.CREATE_NO_WINDOW)

# ── Real fan speed reader (background thread) ─────────────────────────────────
class FanReader(QThread):
    result = Signal(list)   # list of int RPMs

    def run(self):
        ps = r"""
$ErrorActionPreference = 'SilentlyContinue'
$found = $false
foreach ($ns in @('root/LibreHardwareMonitor','root/OpenHardwareMonitor')) {
    $s = Get-WmiObject -Namespace $ns -Class Sensor 2>$null
    if ($s) {
        $fans = $s | Where-Object { $_.SensorType -eq 'Fan' }
        if ($fans) {
            $fans | ForEach-Object { [int]$_.Value }
            $found = $true
            break
        }
    }
}
"""
        try:
            r = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                capture_output=True, text=True, timeout=4,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            vals = []
            for line in r.stdout.strip().splitlines():
                line = line.strip()
                if line.isdigit():
                    v = int(line)
                    if 100 < v < 15000:
                        vals.append(v)
            self.result.emit(vals)
        except:
            self.result.emit([])

# ── Fan animation widget ──────────────────────────────────────────────────────
class FanWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle   = 0.0
        self.speed   = 2.0      # deg/frame
        self.target  = 2.0
        self.n_blades = 5
        self.setMinimumSize(220, 220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_target_rpm(self, rpm: int):
        # rpm → deg/frame @20fps
        self.target = rpm / 60.0 * 360.0 / 20.0

    def step(self):
        self.speed += (self.target - self.speed) * 0.05
        self.angle  = (self.angle + self.speed) % 360.0
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2 - 8

        speed_ratio = min(1.0, self.speed / 80.0)   # 0..1

        # Outer glow ring
        glow_col = QColor(0, 170, 255, int(30 + 80 * speed_ratio))
        p.setPen(QPen(glow_col, 3))
        p.setBrush(QBrush(QColor(0, 20, 40, 60)))
        p.drawEllipse(int(cx - r), int(cy - r), int(r * 2), int(r * 2))

        # Motion blur effect: draw ghost blades at lower opacity
        blur_frames = int(speed_ratio * 4)
        for bf in range(blur_frames, 0, -1):
            alpha = int(20 * (1 - bf / (blur_frames + 1)))
            self._draw_blades(p, cx, cy, r,
                              self.angle - bf * self.speed * 1.5,
                              alpha)

        # Main blades
        blade_alpha = int(180 + 75 * speed_ratio)
        self._draw_blades(p, cx, cy, r, self.angle, blade_alpha)

        # Center hub
        hub = r * 0.13
        p.setPen(QPen(QColor(CYAN), 2))
        p.setBrush(QBrush(QColor(0, 10, 25)))
        p.drawEllipse(int(cx - hub), int(cy - hub), int(hub * 2), int(hub * 2))
        p.setBrush(QBrush(QColor(CYAN)))
        p.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

    def _draw_blades(self, p, cx, cy, r, base_angle, alpha):
        speed_ratio = min(1.0, self.speed / 80.0)
        r_tip = r * 0.88
        r_mid = r * 0.5

        for i in range(self.n_blades):
            angle_deg = base_angle + i * 360.0 / self.n_blades
            angle_rad = math.radians(angle_deg)

            p.save()
            p.translate(cx, cy)
            p.rotate(angle_deg)

            r_color = int(0   + 60  * speed_ratio)
            g_color = int(160 + 40  * speed_ratio)
            b_color = int(220 + 35  * speed_ratio)
            blade_color = QColor(r_color, g_color, b_color, alpha)

            path = QPainterPath()
            path.moveTo(0, -6)
            path.cubicTo(r_mid * 0.6, -10, r_tip * 0.95, -r_tip * 0.18, r_tip, 0)
            path.cubicTo(r_tip * 0.95,  r_tip * 0.18, r_mid * 0.6, 6, 0, 6)
            path.closeSubpath()

            p.setBrush(QBrush(blade_color))
            p.setPen(Qt.NoPen)
            p.drawPath(path)
            p.restore()

# ── Main window ───────────────────────────────────────────────────────────────
class FanspeederApp(QMainWindow):
    def __init__(self, original_plan: str):
        super().__init__()
        self.original_plan = original_plan
        self.current_mode  = "Normal"
        self.display_rpm   = 2200.0
        self.real_rpms: list[int] = []

        self.setWindowTitle("FanspeederX200 3.104")
        self.setMinimumSize(560, 660)
        self.resize(560, 660)
        self.setStyleSheet(f"QWidget {{ background: {BG}; color: {WHITE}; font-family: 'Segoe UI'; }}")

        self._build_ui()

        # Animation timer (50ms = 20fps)
        self._anim = QTimer(); self._anim.timeout.connect(self._animate); self._anim.start(50)
        # RPM display timer (100ms)
        self._rpm_t = QTimer(); self._rpm_t.timeout.connect(self._tick_rpm); self._rpm_t.start(100)
        # Real fan reader (every 4s)
        self._read_t = QTimer(); self._read_t.timeout.connect(self._read_fans); self._read_t.start(4000)
        self._read_fans()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _lbl(self, txt, size=12, color=WHITE, bold=False, align=Qt.AlignCenter):
        l = QLabel(txt)
        f = QFont("Segoe UI", size); f.setBold(bold); l.setFont(f)
        l.setAlignment(align)
        l.setStyleSheet(f"color: {color}; background: transparent;")
        return l

    def _build_ui(self):
        root = QWidget()
        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(24, 18, 24, 18)
        vbox.setSpacing(10)

        # Header
        vbox.addWidget(self._lbl("FanspeederX200", 26, CYAN, bold=True))
        vbox.addWidget(self._lbl("3.104 — Levitation-Grade Fan Control  •  Sito Fidato", 10, GREY))

        # Mode label
        self.mode_lbl = self._lbl("● NORMAL", 13, GREEN, bold=True)
        vbox.addWidget(self.mode_lbl)

        # Fan widget
        self.fan = FanWidget()
        vbox.addWidget(self.fan, stretch=1)

        # RPM display
        self.rpm_lbl = self._lbl("2,200 RPM", 34, CYAN, bold=True)
        vbox.addWidget(self.rpm_lbl)

        self.source_lbl = self._lbl(
            "⚠ No hardware monitor detected — install LibreHardwareMonitor for real RPM", 9, GREY
        )
        vbox.addWidget(self.source_lbl)

        # Levitation risk bar
        lev_row = QHBoxLayout()
        lev_row.addWidget(self._lbl("LEVITATION RISK", 9, GREY, align=Qt.AlignLeft))
        self.lev_bar = QProgressBar()
        self.lev_bar.setRange(0, 100); self.lev_bar.setValue(3)
        self.lev_bar.setTextVisible(False); self.lev_bar.setFixedHeight(8)
        self._style_lev(GREEN)
        lev_row.addWidget(self.lev_bar, stretch=1)
        self.lev_pct = self._lbl("3%", 9, GREEN)
        self.lev_pct.setFixedWidth(36)
        lev_row.addWidget(self.lev_pct)
        vbox.addLayout(lev_row)

        # Altitude joke label
        self.alt_lbl = self._lbl("Altitude gained: 0.00 cm", 10, GREY)
        vbox.addWidget(self.alt_lbl)

        # Mode buttons
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        specs = [("Normal", GREEN, "#0d2010"), ("Turbo", ORANGE, "#201000"), ("X200", RED, "#200000")]
        self.btns = {}
        for name, fg, bg in specs:
            b = QPushButton(name)
            b.setFixedHeight(46)
            b.setFont(QFont("Segoe UI", 14, QFont.Bold))
            b.clicked.connect(lambda _, m=name: self._set_mode(m))
            self.btns[name] = (b, fg, bg)
            btn_row.addWidget(b)
        vbox.addLayout(btn_row)

        # Status
        self.status_lbl = self._lbl("Power plan: Balanced  •  Admin: ✓", 9, GREY)
        vbox.addWidget(self.status_lbl)

        self.setCentralWidget(root)
        self._refresh_buttons("Normal")

    def _style_lev(self, color):
        self.lev_bar.setStyleSheet(
            f"QProgressBar {{ background: #0d1a0d; border-radius: 4px; }}"
            f"QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}"
        )

    def _refresh_buttons(self, active):
        specs = [("Normal", GREEN, "#0d2010"), ("Turbo", ORANGE, "#201000"), ("X200", RED, "#200000")]
        for name, fg, bg in specs:
            b, _, _ = self.btns[name]
            if name == active:
                b.setStyleSheet(
                    f"QPushButton {{ background: {fg}20; color: {fg}; border: 1px solid {fg}; "
                    f"border-radius: 6px; }}"
                )
            else:
                b.setStyleSheet(
                    f"QPushButton {{ background: {bg}; color: {fg}; border: 1px solid {fg}33; "
                    f"border-radius: 6px; }}"
                    f"QPushButton:hover {{ border-color: {fg}; }}"
                )

    # ── Mode switching ────────────────────────────────────────────────────────
    def _set_mode(self, mode: str):
        cfg = MODES[mode]
        self.current_mode = mode
        self.fan.set_target_rpm(cfg["rpm"])
        risk  = cfg["risk"]
        color = cfg["color"]

        # Levitation bar
        self._style_lev(color)
        self.lev_bar.setValue(risk)
        self.lev_pct.setText(f"{risk}%")
        self.lev_pct.setStyleSheet(f"color: {color}; font-size: 9px; background: transparent;")

        # Mode label
        icons = {"Normal": "●", "Turbo": "⚡", "X200": "☠"}
        self.mode_lbl.setText(f"{icons[mode]} {mode.upper()}")
        self.mode_lbl.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: bold; background: transparent;")

        self._refresh_buttons(mode)

        # Apply power plan
        ok = set_plan(cfg["plan"])
        plan_names = {PLAN_BALANCED: "Balanced", PLAN_HIGH: "High Performance",
                      PLAN_ULTIMATE: "Ultimate Performance"}
        pname = plan_names.get(cfg["plan"].lower(), cfg["plan"][:8])
        self.status_lbl.setText(f"Power plan: {pname} {'✓' if ok else '✗'}  •  Admin: ✓")

        # Acer WMI
        acer_set_turbo(cfg["acer"])

        # Save
        try:
            d = json.loads(COOLING_FILE.read_text()) if COOLING_FILE.exists() else {}
            d["fan_mode"] = mode
            d["fan_date"] = time.strftime("%Y-%m-%d %H:%M")
            COOLING_FILE.write_text(json.dumps(d))
        except Exception:
            pass

    # ── Timers ────────────────────────────────────────────────────────────────
    def _animate(self):
        self.fan.step()

    def _tick_rpm(self):
        cfg = MODES[self.current_mode]
        self.display_rpm += (cfg["rpm"] - self.display_rpm) * 0.04

        if self.real_rpms:
            avg = sum(self.real_rpms) // len(self.real_rpms)
            self.rpm_lbl.setText(f"{avg:,} RPM")
            self.rpm_lbl.setStyleSheet(f"color: {GREEN}; font-size: 34px; font-weight: bold; background: transparent;")
        else:
            self.rpm_lbl.setText(f"{int(self.display_rpm):,} RPM")
            self.rpm_lbl.setStyleSheet(f"color: {CYAN}; font-size: 34px; font-weight: bold; background: transparent;")

        # Altitude joke — proportional to RPM over 3000
        over = max(0, int(self.display_rpm) - 3000)
        alt = over * 0.0015
        self.alt_lbl.setText(f"Altitude gained: {alt:.2f} cm  {'🛸 LEVITATION IMMINENT' if alt > 2 else ''}")
        self.alt_lbl.setStyleSheet(
            f"color: {'#ff3333' if alt > 2 else GREY}; font-size: 10px; background: transparent; text-align: center;"
        )

    def _read_fans(self):
        r = FanReader()
        r.result.connect(self._on_fans)
        r.start()

    def _on_fans(self, rpms: list):
        self.real_rpms = rpms
        if rpms:
            fans_str = "  /  ".join(f"{v} RPM" for v in rpms)
            self.source_lbl.setText(f"⚡ Real fans: {fans_str}")
            self.source_lbl.setStyleSheet(f"color: {GREEN}; font-size: 9px; background: transparent;")
        else:
            self.source_lbl.setText(
                "Simulated — install LibreHardwareMonitor and run it as admin for real RPM"
            )
            self.source_lbl.setStyleSheet(f"color: {GREY}; font-size: 9px; background: transparent;")

    # ── Close: restore ────────────────────────────────────────────────────────
    def closeEvent(self, event):
        set_plan(self.original_plan)
        acer_set_turbo(False)
        super().closeEvent(event)


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    if not is_admin():
        app = QApplication(sys.argv)
        w = QMainWindow()
        w.setWindowTitle("FanspeederX200"); w.resize(400, 120)
        c = QWidget(); v = QVBoxLayout(c)
        l = QLabel("Requesting Administrator privileges…")
        l.setAlignment(Qt.AlignCenter)
        l.setStyleSheet(f"color: {WHITE}; font-size: 13px;")
        v.addWidget(l)
        w.setCentralWidget(c)
        w.setStyleSheet(f"QWidget {{ background: {BG}; }}")
        w.show()
        QTimer.singleShot(1200, relaunch_as_admin)
        sys.exit(app.exec())

    original = get_active_plan()
    app = QApplication(sys.argv)
    win = FanspeederApp(original)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
