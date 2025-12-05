import tkinter as tk
import threading
import time

class DisappearingTextApp:
    """
    An online writing app where if you stop typing, your work will disappear.
    """
    def __init__(self, root, timeout=5):
        """Initializes the Watermark Application GUI and state."""
        self.root = root
        self.root.title("Disappearing Text Write App")
        self.timeout = timeout
        self.last_edit_time = time.time()

        self.text = tk.Text(root, width=60, height=20, font=("Arial", 14))
        self.text.pack(padx=10, pady=10)

        # 倒數
        self.timer_label = tk.Label(root, text="", font=("Arial", 12))
        self.timer_label.pack()

        # 每次輸入重設計時器
        self.text.bind("<Key>", self.reset_timer)

        # 啟動監控執行緒
        self.running = True
        threading.Thread(target=self.watchdog, daemon=True).start()

    def reset_timer(self, event=None):
        self.last_edit_time = time.time()

    def watchdog(self):
        while self.running:
            elapsed = time.time() - self.last_edit_time
            remaining = max(0, int(self.timeout - elapsed))
            # 更新倒數
            self.timer_label.config(text=f"文字將在 {remaining} 秒後消失(若無輸入)")

            # 超過 timeout 就清空
            if elapsed >= self.timeout:
                self.text.delete("1.0", tk.END)
                self.last_edit_time = time.time()

            time.sleep(0.2)

if __name__ == "__main__":
    # 建立主視窗物件
    root = tk.Tk()
    app = DisappearingTextApp(root, timeout=10)
    root.mainloop()