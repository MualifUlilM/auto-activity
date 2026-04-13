# mouse.py

from .activity import Activity
import pyautogui
import platform
import random
import time


class Mouse(Activity):
    """Mouse class"""

    def __init__(self, handler):
        """init for Mouse"""
        super().__init__()
        self.handler = handler
        self._platform = platform.system()
        self.use_modifiers = True
        self.key_delay = 0.5
        self.close_emoji_popup = True
        self.tracker_app_name = None

    def _release_modifiers(self):
        # Prevent stuck modifier keys from triggering system shortcuts.
        for key in ("ctrl", "shift", "alt", "command", "option"):
            try:
                pyautogui.keyUp(key)
            except Exception:
                pass

    def _after_keypress(self):
        self._release_modifiers()
        self.__safeSleep(self.key_delay)
        if self._platform == "Darwin" and self.close_emoji_popup:
            # Close Emoji/Dictation panel if it was opened by a shortcut.
            pyautogui.press('esc')
            self.__safeSleep(self.key_delay)

    def _before_keypress(self):
        self._release_modifiers()
        self.__safeSleep(self.key_delay)

    def __smoothMove(self, x1, y1, x2, y2, duration=1) -> None:
        steps = 50  # lebih banyak step
        for i in range(steps):
            if not self.is_active: return
            t = i / steps
            # Interpolasi halus dengan easing (linear → bisa diganti)
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            pyautogui.moveTo(x, y)
            time.sleep(duration / steps)

    def __randomMouseMove(self) -> None:
        if not self.is_active: return
        screen_width, screen_height = pyautogui.size()
        margin = 10
        random_x = random.randint(margin, max(margin, screen_width - margin))
        random_y = random.randint(margin, max(margin, screen_height - margin))
        current_x, current_y = pyautogui.position()
        self.handler.handler(f"Mouse Move to ({random_x}, {random_y})")
        self.__smoothMove(current_x, current_y, random_x, random_y, duration=random.uniform(0.01, 0.3))

    def __randomScroll(self) -> None:
        if not self.is_active: return
        scroll_amount = random.randint(-500, 500)
        self.handler.handler(f"Mouse Scroll {scroll_amount}")
        pyautogui.scroll(scroll_amount)

    def __safeSleep(self, duration):
        """Sleep pendek yang bisa dibatalkan dengan stop()"""
        end_time = time.time() + duration
        while time.time() < end_time:
            if not self.is_active:
                break
            time.sleep(0.1)

    def startTimer(self, sleep_time) -> None:
        self.handler.handler(f"Random Mouse Event {sleep_time} seconds")
        start_time = time.time()
        while time.time() - start_time < sleep_time and self.is_active:
            action = random.choice(['move', 'scroll'])

            if action == 'move':
                self.__randomMouseMove()
            elif action == 'scroll':
                self.__randomScroll()

            self.__safeSleep(random.uniform(0.5, 2))

    def clickCenterScreen(self) -> None:
        if not self.is_active: return
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width / 2
        center_y = screen_height / 2
        self.handler.handler(f"Click Center Screen")
        pyautogui.click(center_x, center_y)

    def switchTab(self, app=None):
        if not self.is_active: return

        count = random.randint(1, 5)
        label = app if app else "app"
        self.handler.handler(f"Key Press ctrl+tab x{count} ({label})")

        # Ctrl+Tab aman di semua platform (tidak memicu system shortcut macOS).
        # Gunakan pola hold-press-release agar Ctrl tetap tertahan antar iterasi.
        self._release_modifiers()
        pyautogui.keyDown('ctrl')
        for _ in range(count):
            if not self.is_active: break
            pyautogui.press('tab')
            self.__safeSleep(0.1)
        pyautogui.keyUp('ctrl')
        self._release_modifiers()

    def typeDeleteText(self, sentences) -> None:
        if not self.is_active: return
        self.clickCenterScreen()
        self.handler.handler("Start Typing on VS Code")
        sentence = random.choice(sentences)
        comment = f"// {sentence}"
        self.handler.handler(f"Typing Text {comment}")

        self.__safeSleep(0.5)
        if self.use_modifiers:
            self.handler.handler("Key Press enter")
            self._before_keypress()
            pyautogui.hotkey('enter')
            self._after_keypress()
            self.__safeSleep(0.5)
            if self._platform == "Darwin":
                self.handler.handler("Key Press ctrl+/")
                self._before_keypress()
                pyautogui.hotkey('ctrl', '/')
                self._after_keypress()
            else:
                self.handler.handler("Key Press ctrl+/")
                pyautogui.hotkey('ctrl', '/')
            self.__safeSleep(0.5)
        else:
            self.handler.handler("Key Modifiers Disabled: simple typing mode")
            self.handler.handler("Key Press enter")
            pyautogui.hotkey('enter')
            self.__safeSleep(0.5)

        if not self.is_active: return
        self._before_keypress()
        pyautogui.write(comment, interval=0.1)
        self.startTimer(5)

        if not self.is_active: return
        self.handler.handler(f"Deleting Text {sentence}")
        self.__safeSleep(0.5)
        self._before_keypress()
        self.handler.handler(f"Key Press backspace x{len(comment)}")
        pyautogui.press('backspace', presses=len(comment), interval=0.1)
        self.__safeSleep(0.5)
        if self.use_modifiers:
            if self._platform == "Darwin":
                self.handler.handler("Key Press ctrl+/")
                self._before_keypress()
                pyautogui.hotkey('ctrl', '/')
                self._after_keypress()
            else:
                self.handler.handler("Key Press ctrl+/")
                pyautogui.hotkey('ctrl', '/')
            self.__safeSleep(0.5)
            self.handler.handler("Key Press backspace")
            self._before_keypress()
            pyautogui.hotkey('backspace')
            self._after_keypress()
            self.__safeSleep(0.5)
            if self._platform == "Darwin":
                self.handler.handler("Skip ctrl+up (Mission Control)")
            else:
                self.handler.handler("Key Press ctrl+home")
                pyautogui.hotkey('ctrl', 'home')
    
    def stopUpworkTimeTracker(self):
        if self.tracker_app_name:
            self.handler.handler(f"Focus tracker app: {self.tracker_app_name}")
            self.bringWindowToFront(self.tracker_app_name)
            self.__safeSleep(0.5)
        if self._platform == "Darwin":
            self.handler.handler("Key Press ctrl+opt+[")
            self._before_keypress()
            pyautogui.hotkey('ctrl', 'option', '[')
            self._after_keypress()
        else:
            self.handler.handler("Key Press ctrl+alt+[")
            pyautogui.hotkey('ctrl', 'alt', '[')
