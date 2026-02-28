using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using Newtonsoft.Json.Linq;

namespace DBPFF_App
{
    public partial class MainWindow : Window
    {
        private readonly string _siteRoot;
        private bool _sidebarOpen = false;
        private readonly List<string> _logs = new();
        private readonly Dictionary<string, Process?> _running = new();
        private readonly string _home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);

        private static readonly string[] RgbPatterns =
            { "Rainbow Cycle", "Breathing", "Wave", "Solid Color", "Chaos", "π-Mode", "Epilepsy Speedrun %" };

        private readonly Dictionary<string, string> _appPaths = new()
        {
            ["win12"] = @"apps\Windows12Ultra\Windows12Ultra.exe",
            ["miner"] = @"apps\freeCrYptOMiner2\freeCrYptOMinerminor2paygood2.exe",
            ["bench"] = @"apps\BenchmarkUltra\BenchmarkUltra.exe",
            ["virus"] = @"apps\VirusDeleter\VirusDeleter.exe",
            ["rgb"]   = @"apps\RGBUltimate\RGBUltimate.exe",
            ["gpu1"]  = @"apps\Hardware\RTX5090.exe",
            ["gpu2"]  = @"apps\Hardware\2xRTX5090.exe",
            ["cpu1"]  = @"apps\Hardware\Ryzen9_92759X5D.exe",
            ["ssd1"]  = @"apps\Hardware\SSD_8TB.exe",
            ["ssd2"]  = @"apps\Hardware\SSD_50kPB.exe",
            ["fan"]   = @"apps\Cooling\FanspeederX200.exe",
        };

        public MainWindow()
        {
            InitializeComponent();
            _siteRoot = FindSiteRoot();
            InitWebView();
            AddLog("DBPFF Hub started");
        }

        private string FindSiteRoot()
        {
            var dir = AppDomain.CurrentDomain.BaseDirectory;
            while (dir != null)
            {
                if (File.Exists(Path.Combine(dir, "index.html")))
                    return dir;
                dir = Directory.GetParent(dir)?.FullName;
            }
            return @"C:\Users\ricca\DownloadBetterPerformanceForFree";
        }

        private async void InitWebView()
        {
            try
            {
                await webView.EnsureCoreWebView2Async();
                webView.CoreWebView2.Navigate(
                    new Uri(Path.Combine(_siteRoot, "index.html")).AbsoluteUri);
                AddLog("WebView2 loaded");
            }
            catch (Exception ex)
            {
                AddLog($"WebView2 error: {ex.Message}");
            }
        }

        // ═══════ SIDEBAR TOGGLE ═══════

        private void ToggleSidebar_Click(object sender, RoutedEventArgs e)
        {
            _sidebarOpen = !_sidebarOpen;
            if (_sidebarOpen)
            {
                sidebarCol.Width = new GridLength(200);
                sidebarContent.Visibility = Visibility.Visible;
                btnToggle.Content = "✕";
                btnToggle.HorizontalAlignment = HorizontalAlignment.Right;
                btnToggle.Margin = new Thickness(0, 6, 6, 0);
            }
            else
            {
                sidebarCol.Width = new GridLength(36);
                sidebarContent.Visibility = Visibility.Collapsed;
                btnToggle.Content = "☰";
                btnToggle.HorizontalAlignment = HorizontalAlignment.Center;
                btnToggle.Margin = new Thickness(0, 6, 0, 0);
            }
        }

        // ═══════ SITO NAVIGATION ═══════

        private async void NavSito_Click(object sender, RoutedEventArgs e)
        {
            ShowPanel("sito");
            var tag = (sender as Button)?.Tag?.ToString();
            if (webView.CoreWebView2 == null) return;

            switch (tag)
            {
                case "home":
                    webView.CoreWebView2.Navigate(
                        new Uri(Path.Combine(_siteRoot, "index.html")).AbsoluteUri);
                    break;
                case "about":
                    webView.CoreWebView2.Navigate(
                        new Uri(Path.Combine(_siteRoot, "about", "index.html")).AbsoluteUri);
                    break;
                default:
                    var indexUri = new Uri(Path.Combine(_siteRoot, "index.html")).AbsoluteUri;
                    var current = webView.CoreWebView2.Source?.Split('#')[0] ?? "";
                    if (current == indexUri)
                    {
                        await webView.CoreWebView2.ExecuteScriptAsync(
                            $"document.getElementById('{tag}')?.scrollIntoView({{behavior:'smooth'}})");
                    }
                    else
                    {
                        webView.CoreWebView2.Navigate(indexUri + "#" + tag);
                    }
                    break;
            }
        }

        // ═══════ APP / HUB NAVIGATION ═══════

        private void NavApp_Click(object sender, RoutedEventArgs e)
        {
            var tag = (sender as Button)?.Tag?.ToString();
            ShowPanel(tag);

            switch (tag)
            {
                case "kc":
                case "miner":    RefreshKC(); break;
                case "win12":    RefreshWin12(); break;
                case "bench":    RefreshBenchmark(); break;
                case "virus":    RefreshVirus(); break;
                case "rgb":      RefreshRgb(); break;
                case "gpu":      RefreshGPU(); break;
                case "cpu":      RefreshCPU(); break;
                case "storage":  RefreshStorage(); break;
                case "fan":      RefreshFan(); break;
                case "settings": RefreshSettings(); break;
            }
        }

        private void ShowPanel(string? p)
        {
            webView.Visibility       = p == "sito"     ? Visibility.Visible : Visibility.Collapsed;
            panelWin12.Visibility    = p == "win12"    ? Visibility.Visible : Visibility.Collapsed;
            panelMiner.Visibility    = p == "miner"    ? Visibility.Visible : Visibility.Collapsed;
            panelKC.Visibility       = p == "kc"       ? Visibility.Visible : Visibility.Collapsed;
            panelBench.Visibility    = p == "bench"    ? Visibility.Visible : Visibility.Collapsed;
            panelVirus.Visibility    = p == "virus"    ? Visibility.Visible : Visibility.Collapsed;
            panelRgb.Visibility      = p == "rgb"      ? Visibility.Visible : Visibility.Collapsed;
            panelZip.Visibility      = p == "zip"      ? Visibility.Visible : Visibility.Collapsed;
            panelGPU.Visibility      = p == "gpu"      ? Visibility.Visible : Visibility.Collapsed;
            panelCPU.Visibility      = p == "cpu"      ? Visibility.Visible : Visibility.Collapsed;
            panelStorage.Visibility  = p == "storage"  ? Visibility.Visible : Visibility.Collapsed;
            panelFan.Visibility      = p == "fan"      ? Visibility.Visible : Visibility.Collapsed;
            panelLog.Visibility      = p == "log"      ? Visibility.Visible : Visibility.Collapsed;
            panelSettings.Visibility = p == "settings" ? Visibility.Visible : Visibility.Collapsed;
        }

        // ═══════ APP LAUNCH / KILL ═══════

        private void LaunchApp_Click(object sender, RoutedEventArgs e)
        {
            var key = (sender as Button)?.Tag?.ToString();
            if (key == null || !_appPaths.ContainsKey(key)) return;

            if (_running.TryGetValue(key, out var existing) && existing != null && !existing.HasExited)
            {
                AddLog($"[{key}] Already running");
                return;
            }

            var fullPath = Path.Combine(_siteRoot, _appPaths[key]);
            if (!File.Exists(fullPath))
            {
                AddLog($"[{key}] Not found: {fullPath}");
                return;
            }

            try
            {
                var proc = Process.Start(new ProcessStartInfo(fullPath) { UseShellExecute = true });
                _running[key] = proc;
                AddLog($"[{key}] Launched");
            }
            catch (Exception ex)
            {
                AddLog($"[{key}] Error: {ex.Message}");
            }
        }

        private void KillApp_Click(object sender, RoutedEventArgs e)
        {
            var key = (sender as Button)?.Tag?.ToString();
            if (key == null) return;

            if (_running.TryGetValue(key, out var proc) && proc != null && !proc.HasExited)
            {
                proc.Kill();
                AddLog($"[{key}] Killed");
            }
            else
            {
                AddLog($"[{key}] Not running");
            }
        }

        private void OpenFolder_Click(object sender, RoutedEventArgs e)
        {
            var zipDir = Path.Combine(_siteRoot, "apps", "ZIPdInternet");
            if (Directory.Exists(zipDir))
            {
                Process.Start(new ProcessStartInfo("explorer.exe", zipDir));
                AddLog("[zip] Opened folder");
            }
            else
            {
                AddLog("[zip] Folder not found");
            }
        }

        // ═══════ REFRESH: WINDOWS 12 ULTRA ═══════

        private void RefreshWin12()
        {
            try
            {
                var path = Path.Combine(_home, ".windows12ultra_status.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var installed = j["installed"]?.Value<bool>() ?? false;

                    if (installed)
                    {
                        win12Status.Text = "Installed";
                        win12Status.Foreground = Brush("#00ff99");
                        win12Date.Text = $"Installed on: {j["date"]}";

                        var ram = j["ram_tb"]?.Value<int>() ?? 0;
                        var drv = j["drivers"]?.Value<int>() ?? 0;
                        var vir = j["viruses_deleted"]?.Value<int>() ?? 0;

                        win12Specs.Text =
                            $"RAM: {ram} TB (downloaded)\n" +
                            $"Kernel: π (3.14159265...)\n" +
                            $"Boot time: 0.00000001 s\n" +
                            $"Drivers installed: {drv:N0}\n" +
                            $"Viruses pre-deleted: {vir}\n" +
                            $"Reality: Activated";
                    }
                }
                else
                {
                    win12Status.Text = "Not installed";
                    win12Status.Foreground = Brush("#6a88a8");
                    win12Date.Text = "";
                    win12Specs.Text = "Run Windows 12 Ultra to install and see specs";
                }
            }
            catch (Exception ex) { AddLog($"win12 refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: KELIUSCOIN ═══════

        private void RefreshKC_Click(object sender, RoutedEventArgs e) => RefreshKC();

        private void RefreshKC()
        {
            try
            {
                var path = Path.Combine(_home, ".freecryptominer2_wallet.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var total = j["total_kc"]?.Value<double>() ?? 0;
                    var userKc = total * 0.01;
                    var sitoKc = total * 0.99;

                    kcBalanceText.Text = $"{userKc:F6} KC";
                    kcSitoText.Text = $"{sitoKc:F6} KC";
                    minerUserKC.Text = $"{userKc:F6} KC";
                    minerSitoKC.Text = $"{sitoKc:F6} KC";
                    AddLog($"KC refreshed: {total:F6} total");
                }
                else
                {
                    kcBalanceText.Text = "No wallet found";
                    kcSitoText.Text = "—";
                    minerUserKC.Text = "No wallet found";
                    minerSitoKC.Text = "—";
                }
            }
            catch (Exception ex)
            {
                kcBalanceText.Text = $"Error: {ex.Message}";
                AddLog($"KC error: {ex.Message}");
            }
        }

        // ═══════ REFRESH: BENCHMARK ═══════

        private void RefreshBenchmark()
        {
            try
            {
                var path = Path.Combine(_home, ".benchmarkultra_history.json");
                if (File.Exists(path))
                {
                    var arr = JArray.Parse(File.ReadAllText(path));
                    if (arr.Count > 0)
                    {
                        var last = arr.Last!;
                        var score = last["score"]?.Value<double>() ?? 0;
                        benchScore.Text = $"{score:F5} pts";
                        benchInfo.Text = $"PC: {last["pc"]}  |  {last["date"]}";

                        var lines = new List<string>();
                        for (int i = arr.Count - 1; i >= 0 && i >= arr.Count - 10; i--)
                        {
                            var e = arr[i];
                            lines.Add($"{e["date"]}  {e["score"]?.Value<double>():F5} pts  ({e["pc"]})");
                        }
                        benchHistory.Text = string.Join("\n", lines);
                        return;
                    }
                }
                benchScore.Text = "—";
                benchInfo.Text = "No benchmarks yet — run BenchmarkUltra";
                benchHistory.Text = "No history yet";
            }
            catch (Exception ex) { AddLog($"bench refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: VIRUSDELETER ═══════

        private void RefreshVirus()
        {
            try
            {
                var path = Path.Combine(_home, ".virusdeleter_history.json");
                if (File.Exists(path))
                {
                    var arr = JArray.Parse(File.ReadAllText(path));
                    if (arr.Count > 0)
                    {
                        var last = arr.Last!;
                        virusLastScan.Text =
                            $"Last scan: {last["type"]}  |  {last["threats"]} threats  |  {last["date"]}\n" +
                            $"Total scans: {arr.Count}";

                        var lines = new List<string>();
                        for (int i = arr.Count - 1; i >= 0 && i >= arr.Count - 10; i--)
                        {
                            var e = arr[i];
                            lines.Add($"{e["date"]}  {e["type"],-12}  {e["threats"]} threats");
                        }
                        virusHistory.Text = string.Join("\n", lines);
                        return;
                    }
                }
                virusLastScan.Text = "No scans yet — run VirusDeleter";
                virusHistory.Text = "No scans yet";
            }
            catch (Exception ex) { AddLog($"virus refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: RGBULTIMATE ═══════

        private void RefreshRgb()
        {
            try
            {
                var path = Path.Combine(_home, ".rgbultimate_settings.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var speed = j["speed"]?.Value<int>() ?? 3;
                    var brightness = j["brightness"]?.Value<int>() ?? 200;
                    var patIdx = j["pattern"]?.Value<int>() ?? 0;
                    var patName = patIdx >= 0 && patIdx < RgbPatterns.Length
                        ? RgbPatterns[patIdx] : "Unknown";

                    rgbInfo.Text =
                        $"Pattern: {patName}\n" +
                        $"Speed: {speed}/20\n" +
                        $"Brightness: {brightness}/255";
                }
                else
                {
                    rgbInfo.Text = "Default settings (no saves yet)";
                }
            }
            catch (Exception ex) { AddLog($"rgb refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: SETTINGS / RAM ═══════

        private void RefreshSettings()
        {
            try
            {
                var path = Path.Combine(_home, ".dbpff_ram.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var amount = j["amount"]?.Value<string>() ?? "none";
                    var spec   = j["spec"]?.Value<string>()   ?? "";
                    var date   = j["date"]?.Value<string>()   ?? "";
                    var tier   = j["tier"]?.Value<int>()      ?? 0;

                    if (tier > 0)
                    {
                        settingsRamInfo.Text =
                            $"Amount: {amount}\n" +
                            $"Spec:   {spec}\n" +
                            $"Installed: {date}";
                        settingsRamInfo.Foreground = Brush("#00ff88");
                    }
                    else
                    {
                        settingsRamInfo.Text = "No RAM downloaded yet";
                        settingsRamInfo.Foreground = Brush("#557755");
                    }
                }
                else
                {
                    settingsRamInfo.Text = "No RAM downloaded yet";
                    settingsRamInfo.Foreground = Brush("#557755");
                }
            }
            catch (Exception ex) { AddLog($"settings refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: FANSPEEDER ═══════

        private void RefreshFan_Click(object sender, RoutedEventArgs e) => RefreshFan();

        private void RefreshFan()
        {
            try
            {
                var path = Path.Combine(_home, ".dbpff_cooling.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var mode = j["fan_mode"]?.Value<string>() ?? "";
                    var date = j["fan_date"]?.Value<string>() ?? "";
                    if (!string.IsNullOrEmpty(mode))
                    {
                        fanMode.Text = mode switch
                        {
                            "Normal" => "Normal (Balanced)",
                            "Turbo"  => "Turbo (High Performance)",
                            "X200"   => "X200 — LEVITATION RISK",
                            _        => mode
                        };
                        fanMode.Foreground = mode switch
                        {
                            "Normal" => Brush("#44cc88"),
                            "Turbo"  => Brush("#ffaa00"),
                            "X200"   => Brush("#ff3333"),
                            _        => Brush("#00ccff")
                        };
                        fanDate.Text = $"Last set: {date}";
                        return;
                    }
                }
                fanMode.Text = "No mode set";
                fanMode.Foreground = Brush("#4499aa");
                fanDate.Text = "";
            }
            catch (Exception ex) { AddLog($"fan refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: GPU ═══════

        private void RefreshGPU_Click(object sender, RoutedEventArgs e) => RefreshGPU();

        private void RefreshGPU()
        {
            try
            {
                var path = Path.Combine(_home, ".dbpff_gpu.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var tier = j["tier"]?.Value<int>() ?? 0;
                    if (tier > 0)
                    {
                        gpuStatus.Text = j["name"]?.Value<string>() ?? "Unknown";
                        gpuStatus.Foreground = Brush("#00aaff");
                        gpuSpec.Text = j["spec"]?.Value<string>() ?? "";
                        gpuDate.Text = $"Installed: {j["date"]}";
                        return;
                    }
                }
                gpuStatus.Text = "No GPU downloaded yet";
                gpuStatus.Foreground = Brush("#4477aa");
                gpuSpec.Text = "";
                gpuDate.Text = "";
            }
            catch (Exception ex) { AddLog($"gpu refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: CPU ═══════

        private void RefreshCPU_Click(object sender, RoutedEventArgs e) => RefreshCPU();

        private void RefreshCPU()
        {
            try
            {
                var path = Path.Combine(_home, ".dbpff_cpu.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var tier = j["tier"]?.Value<int>() ?? 0;
                    if (tier > 0)
                    {
                        cpuStatus.Text = j["name"]?.Value<string>() ?? "Unknown";
                        cpuStatus.Foreground = Brush("#ff5533");
                        cpuSpec.Text = j["spec"]?.Value<string>() ?? "";
                        cpuDate.Text = $"Installed: {j["date"]}";
                        return;
                    }
                }
                cpuStatus.Text = "No CPU downloaded yet";
                cpuStatus.Foreground = Brush("#aa5533");
                cpuSpec.Text = "";
                cpuDate.Text = "";
            }
            catch (Exception ex) { AddLog($"cpu refresh error: {ex.Message}"); }
        }

        // ═══════ REFRESH: STORAGE ═══════

        private void RefreshStorage_Click(object sender, RoutedEventArgs e) => RefreshStorage();

        private void RefreshStorage()
        {
            try
            {
                var path = Path.Combine(_home, ".dbpff_storage.json");
                if (File.Exists(path))
                {
                    var j = JObject.Parse(File.ReadAllText(path));
                    var tier = j["tier"]?.Value<int>() ?? 0;
                    if (tier > 0)
                    {
                        storageStatus.Text = j["name"]?.Value<string>() ?? "Unknown";
                        storageStatus.Foreground = Brush("#aa44ff");
                        storageSpec.Text = j["spec"]?.Value<string>() ?? "";
                        storageDate.Text = $"Installed: {j["date"]}";
                        return;
                    }
                }
                storageStatus.Text = "No storage downloaded yet";
                storageStatus.Foreground = Brush("#7744aa");
                storageSpec.Text = "";
                storageDate.Text = "";
            }
            catch (Exception ex) { AddLog($"storage refresh error: {ex.Message}"); }
        }

        // ═══════ LOG ═══════

        private void AddLog(string msg)
        {
            var line = $"[{DateTime.Now:HH:mm:ss}] {msg}";
            _logs.Add(line);
            if (_logs.Count > 200) _logs.RemoveAt(0);
            logText.Text = string.Join("\n", _logs);
        }

        // ═══════ HELPERS ═══════

        private static System.Windows.Media.SolidColorBrush Brush(string hex) =>
            new((System.Windows.Media.Color)System.Windows.Media.ColorConverter.ConvertFromString(hex));

        // ═══════ CLEANUP ═══════

        protected override void OnClosed(EventArgs e)
        {
            foreach (var kv in _running)
            {
                try { if (kv.Value != null && !kv.Value.HasExited) kv.Value.Kill(); } catch { }
            }
            base.OnClosed(e);
        }
    }
}
