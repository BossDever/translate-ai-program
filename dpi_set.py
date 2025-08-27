# --- DPI-friendly Tkinter bootstrap (drop-in) -------------------------------
import platform, ctypes, tkinter as tk
import tkinter.font as tkFont


class DpiManager:
    """จัดการ DPI awareness (Windows) + ปรับ tk scaling ตาม DPI จริงของหน้าต่าง
       อัปเดตอัตโนมัติเมื่อหน้าต่างถูกย้าย/รีไซส์ (debounce)
    """
    def __init__(self):
        self._last_dpi = None
        self._debounce_id = None

    def enable_win_dpi_awareness(self, mode="system"):
        """mode: 'system' = เสถียรสุดกับ Tk; 'permonitor' = ย้ายข้ามจอแล้วยังคม (อาจต่างกันตาม build ของ Tk)"""
        if platform.system() != "Windows":
            return
        if mode == "permonitor":
            # ลอง per-monitor v1 (ปลอดภัยกว่า v2 กับ Tk หลายรุ่น)
            try:
                PER_MONITOR_AWARE = ctypes.c_void_p(-3)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE
                ctypes.windll.user32.SetProcessDpiAwarenessContext(PER_MONITOR_AWARE)
                return
            except Exception:
                pass
        # system-DPI aware (เสถียรสุด)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
            return
        except Exception:
            pass
        try:
            ctypes.windll.user32.SetProcessDPIAware()       # fallback เก่า
        except Exception:
            pass

    def _get_window_dpi(self, root: tk.Tk) -> float:
        """คืนค่า DPI ปัจจุบันของหน้าต่าง root (float)"""
        # Windows: ใช้ GetDpiForWindow หากมี (แม่นสุด)
        if platform.system() == "Windows":
            try:
                hwnd = root.winfo_id()
                dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
                if dpi: return float(dpi)
            except Exception:
                pass
            return 96.0  # default

        # macOS / Linux: ใช้ Tk เองคำนวณ px ต่อ 1 นิ้ว
        try:
            # '1i' = 1 inch; ได้ px จริงของระบบ
            dpi = float(root.winfo_fpixels('1i'))
            return dpi
        except Exception:
            return 96.0

    def apply_tk_scaling(self, root: tk.Tk):
        """เซ็ต tk scaling จาก DPI ปัจจุบัน (72 pt = 96 px ที่ 100%)"""
        dpi = self._get_window_dpi(root)
        if dpi != self._last_dpi:
            root.tk.call('tk', 'scaling', dpi / 72.0)
            self._last_dpi = dpi
            # อัปเดตฟอนต์ชื่อมาตรฐานให้ sync (ถ้าคุณใช้ named fonts)
            for name in ("TkDefaultFont","TkTextFont","TkMenuFont","TkHeadingFont","TkCaptionFont","TkSmallCaptionFont","TkIconFont","TkTooltipFont"):
                try:
                    f = tkFont.nametofont(name)
                    # ไม่บังคับ size ใหม่ ถ้าคุณตั้งแบบจงใจไว้เอง; แค่ "touch" ให้ Tk reflow
                    f.configure(size=f['size'])
                except Exception:
                    pass

    def bind_auto_update(self, root: tk.Tk):
        """อัปเดต scaling อัตโนมัติเมื่อย้าย/รีไซส์ ด้วย debounce"""
        def _debounced_update(*_):
            if self._debounce_id:
                root.after_cancel(self._debounce_id)
            self._debounce_id = root.after(100, lambda: self.apply_tk_scaling(root))
        root.bind('<Configure>', _debounced_update)

