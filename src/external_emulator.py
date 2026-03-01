#!/usr/bin/env python3
"""
external_emulator.py

    If the user does not wish to use the built-in mgba libretro core, they can opt to use their external emulator.
    This script handles the launch skeleton, while providers are collected from the providers folder. For example,
    the SBC handheld firmware ROCKNIX has its own launch control method, which is performed in providers/rocknix.py.
    
    More providers can be added in this way, simply by creating a new provider.py file.
"""

import os
import platform
import inspect
import subprocess
import threading
import time
import pygame
from abc import ABC, abstractmethod

from settings import load_sinew_settings

# --- Provider Interface ---

class EmulatorProvider(ABC):
    @property
    @abstractmethod
    def supported_os(self):
        pass

    @abstractmethod
    def get_command(self, rom_path, core="auto"):
        pass

    @abstractmethod
    def probe(self, distro_id) -> bool:
        """Return True if this provider is available and active on the current system."""
        pass
        
    @abstractmethod
    def terminate(self, process):
        pass

    @abstractmethod
    def on_exit(self):
        pass

# --- Import providers ---    
from providers import *

# --- Main ExternalEmulator Controller ---

class ExternalEmulator:
    def __init__(self):
        self.process = None
        self.active_provider = None
        self.is_running = False
        self.current_os = platform.system().lower()
        self.distro_id = self._get_linux_distro() if self.current_os == "linux" else None
        
        # Load settings
        current_settings = load_sinew_settings()
        
        # Register Providers
        import providers
        self.providers = [
            cls(current_settings) 
            for name, cls in inspect.getmembers(providers, inspect.isclass)
            if issubclass(cls, EmulatorProvider) 
            and cls is not EmulatorProvider
            and getattr(cls, 'active', False)
        ]
        
        self._detect_environment()
        
    def _get_linux_distro(self):
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                distro_id = None
                os_name = None
                for line in f:
                    if line.startswith('ID='):
                        distro_id = line.split('=')[1].strip().replace('"', '').lower()
                    elif line.startswith('OS_NAME='):
                        os_name = line.split('=')[1].strip().replace('"', '').lower()
                return distro_id or os_name or "generic"
        return "generic"

    def _detect_environment(self):
        if not self.providers:
            print("[ExternalEmu] No providers registered (all have active = False).")
            return

        for provider in self.providers:
            name = type(provider).__name__
            if self.current_os not in provider.supported_os:
                print(
                    f"[ExternalEmu] Skipping {name}:"
                    f" supports {provider.supported_os}, current OS is '{self.current_os}'"
                )
                continue
            if provider.probe(self.distro_id):
                self.active_provider = provider
                print(f"[ExternalEmu] Initialized {name}")
                return
            print(f"[ExternalEmu] {name} probe failed.")

        print("[ExternalEmu] No provider matched this environment.")

    def launch(self, rom_path, controller_manager, core="auto"):
        if not self.active_provider:
            print("[ExternalEmu] No provider found. Launch aborted.")
            return False

        cmd = self.active_provider.get_command(rom_path, core)
        if not cmd:
            return False

        # Release the hardware
        controller_manager.pause()
        pygame.display.iconify()

        # Revert LD_LIBRARY_PATH for the system tools
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = env.get("LD_LIBRARY_PATH_ORIG", "/usr/lib:/lib")

        try:
            # Launch the external emulator
            self.process = subprocess.Popen(
                cmd,
                env=env,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=True
            )
            self.is_running = True
            self._exit_handled = False

            # Automatically resume input when the process dies
            def wait_for_exit():
                self.process.wait()
                print("[ExternalEmu] Subprocess ended. Resuming Sinew controls...")
                self.is_running = False
                if not self._exit_handled:
                    self._exit_handled = True
                    self.active_provider.on_exit()
                    controller_manager.resume()
                    self._restore_window()

            threading.Thread(target=wait_for_exit, daemon=True).start()

            return True
        except Exception as e:
            print(f"[ExternalEmu] Launch Error: {e}")
            controller_manager.resume()
            return False

    def _restore_window(self):
        """Restore and focus the Sinew window after the external emulator closes."""
        # Give the OS a moment to fully clean up the emulator window.
        time.sleep(0.3)
        if platform.system().lower() == "windows":
            try:
                import ctypes
                hwnd = pygame.display.get_wm_info().get("window")
                if hwnd:
                    SW_RESTORE = 9
                    ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    print("[ExternalEmu] Window restored.")
            except Exception as e:
                print(f"[ExternalEmu] Window restore failed: {e}")
        else:
            # On Linux/macOS pygame.VIDEORESIZE or a display event will
            # bring the window back; posting VIDEOEXPOSE nudges a redraw.
            pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE))

    def check_status(self):
        if self.process is None:
            return False
        status = self.process.poll()
        if status is not None:
            print(f"[ExternalEmu] Process exited with code: {status}")
            self.process = None
            return False
        return True
        
    def terminate(self):
        if self.process and self.active_provider:
            print(f"[ExternalEmu] Delegating termination to {type(self.active_provider).__name__}")
            self._exit_handled = True
            self.active_provider.terminate(self.process)
            self.process = None
            self.is_running = False