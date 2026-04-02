# activity.py

import platform
import subprocess
import psutil

try:
    import pygetwindow as gw
except Exception:
    gw = None

class Activity:
    """Activity class"""
    is_active = False
    process = None

    def __init__(self):
        """init for Activity"""
        self._platform = platform.system()

    def _mac_app_name(self, name: str) -> str:
        mapping = {
            "chrome": "Google Chrome",
            "code": "Visual Studio Code",
            "vscode": "Visual Studio Code",
        }
        return mapping.get(name.lower(), name)

    def _mac_activate_app(self, name: str) -> None:
        app_name = self._mac_app_name(name)
        script = f'tell application "{app_name}" to activate'
        subprocess.run(["osascript", "-e", script], check=False)

    def _mac_frontmost_app(self) -> str:
        script = 'tell application "System Events" to get name of first application process whose frontmost is true'
        result = subprocess.run(["osascript", "-e", script], check=False, capture_output=True, text=True)
        return result.stdout.strip()

    def isProcessRunning(self, process_name) -> bool:
        """Cek apakah proses berjalan berdasarkan nama"""
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in process.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def bringWindowToFront(self, window_title) -> None:
        """Membawa jendela ke depan berdasarkan judulnya"""
        if self._platform == "Darwin":
            self._mac_activate_app(window_title)
            return

        if gw is None:
            return

        windows = [w for w in gw.getWindowsWithTitle(window_title) if window_title.lower() in w.title.lower()]
        if windows:
            window = windows[0]
            window.activate()
            window.maximize()

    def isProcessOnFront(self, window_title) -> bool:
        """Cek apakah jendela dengan judul tertentu sedang berada di depan (aktif)"""
        if self._platform == "Darwin":
            frontmost = self._mac_frontmost_app()
            target = self._mac_app_name(window_title)
            return target.lower() in frontmost.lower()

        if gw is None:
            return False

        active_window = gw.getActiveWindow()
        if active_window and window_title.lower() in active_window.title.lower():
            return True
        return False
