import tkinter as tk
import time
import random

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing speed test is a fun way to improve your skills.",
    "Python is a powerful and popular programming language.",
    "Practice makes perfect, so keep typing every day.",
    "Artificial intelligence is changing the world rapidly."
]

class TypingSpeedTest:
    """
    A Tkinter GUI desktop application that tests your typing speed.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("700x350")
        self.start_time = None
        self.ended = False

        self.random_sentences = tk.StringVar()
        self.random_sentences.set(random.choice(sentences))
        tk.Label(root, text="請輸入以下句子：", font=("Arial", 14)).pack(pady=10)
        self.sentence_label = tk.Label(root, textvariable=self.random_sentences, wraplength=650, font=("Arial", 14))
        self.sentence_label.pack(pady=50)

        self.input_field = tk.Text(root, height=5, width=70, font=("Arial", 14))
        self.input_field.pack()
        self.input_field.bind("<KeyPress>", self.start_test)

        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="white")
        self.result_label.pack(pady=15)

        tk.Button(root, text="重置", font=("Arial", 14), command=self.reset_test).pack()


    def start_test(self, event):
        if self.start_time is None:  # 第一次按鍵
            self.start_time = time.time()

        # 如果按下 Enter 結束測試
        if event.keysym == "Return":
            self.end_test()

    def end_test(self):
        if self.ended:
            return
        self.ended = True

        end_time = time.time()
        elapsed = end_time - self.start_time

        typed_text = self.input_field.get("1.0", tk.END).strip()
        target_text = self.random_sentences.get()

        # 計算
        words = len(typed_text.split())
        chars = len(typed_text)

        wpm = words / (elapsed / 60)
        cpm = chars / (elapsed / 60)

        # 正確率
        correct_chars = sum(1 for a, b in zip(typed_text, target_text) if a == b)
        accuracy = correct_chars / len(target_text) * 100

        result = (
            f"⏱ 用時: {elapsed:.2f} 秒\n"
            f"💬 WPM（每分鐘單字）: {wpm:.2f}\n"
            f"🔡 CPM（每分鐘字元）: {cpm:.2f}\n"
            f"🎯 正確率: {accuracy:.2f}%"
        )

        self.result_label.config(text=result)

    def reset_test(self):
        self.start_time = None
        self.ended = False
        self.input_field.delete("1.0", tk.END)
        self.random_sentences.set(random.choice(sentences))
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
