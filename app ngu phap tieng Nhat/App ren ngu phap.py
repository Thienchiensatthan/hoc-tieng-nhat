import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME_GR = os.path.join(BASE_DIR, "ngu_phap.json")

class AppHocNguPhap:
    def __init__(self, root):
        self.root = root
        self.root.title("App Luyện Ngữ Pháp v8.1")
        self.root.geometry("700x650")
        self.data_grammar = self.load_data()
        self.current_sentence = None
        
        # --- GIAO DIỆN CHÍNH (Giữ nguyên như bản trước) ---
        tk.Label(root, text="LUYỆN CẤU TRÚC & NGỮ PHÁP", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.display_frame = tk.LabelFrame(root, text="Dịch câu sau sang Hiragana", padx=10, pady=20)
        self.display_frame.pack(padx=20, pady=10, fill="both")
        self.label_struct = tk.Label(self.display_frame, text="Cấu trúc: ...", font=("Arial", 10, "italic"), fg="blue")
        self.label_struct.pack()
        self.label_vietnamese = tk.Label(self.display_frame, text="Bấm 'Câu tiếp theo' để bắt đầu", font=("Arial", 14, "bold"), wraplength=600)
        self.label_vietnamese.pack(pady=10)

        self.entry_answer = tk.Entry(root, font=("Arial", 14), justify="center")
        self.entry_answer.pack(pady=10, padx=50, fill="x")
        self.entry_answer.bind('<Return>', lambda e: self.check_answer())

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Kiểm tra (Enter)", command=self.check_answer, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Câu tiếp theo", command=self.next_question, width=15).grid(row=0, column=1, padx=5)

        tk.Button(root, text="QUẢN LÝ KHO NGỮ PHÁP", command=self.open_manage_window, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

    def load_data(self):
        if os.path.exists(FILE_NAME_GR):
            with open(FILE_NAME_GR, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(FILE_NAME_GR, "w", encoding="utf-8") as f:
            json.dump(self.data_grammar, f, ensure_ascii=False, indent=4)

    def next_question(self):
        if not self.data_grammar:
            messagebox.showwarning("Trống", "Chưa có dữ liệu!")
            return
        # Chọn cấu trúc có ít nhất 1 câu
        valid_structs = [g for g in self.data_grammar if g['sentences']]
        struct = random.choice(valid_structs)
        self.current_sentence = random.choice(struct['sentences'])
        self.label_struct.config(text=f"Cấu trúc: {struct['grammar_name']}")
        self.label_vietnamese.config(text=self.current_sentence['vi'])
        self.entry_answer.delete(0, tk.END)

    def check_answer(self):
        if not self.current_sentence: return
        user_ans = self.entry_answer.get().strip().replace(" ", "")
        correct_ans = self.current_sentence['hira'].strip().replace(" ", "")
        if user_ans == correct_ans:
            messagebox.showinfo("Đúng", "Chuẩn!")
            self.next_question()
        else:
            messagebox.showerror("Sai", f"Đáp án: {self.current_sentence['hira']}")

    # --- CỬA SỔ QUẢN LÝ MỚI XỊN XÒ HƠN ---
    def open_manage_window(self):
        manage_win = tk.Toplevel(self.root)
        manage_win.title("Quản lý Ngữ pháp")
        manage_win.geometry("500x500")

        # Phần 1: Chọn hoặc thêm cấu trúc
        tk.Label(manage_win, text="1. Chọn Cấu trúc cũ hoặc Gõ tên Cấu trúc mới:", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Danh sách tên các cấu trúc đã có
        struct_names = [g['grammar_name'] for g in self.data_grammar]
        self.combo_struct = ttk.Combobox(manage_win, values=struct_names, width=40)
        self.combo_struct.pack(pady=5)
        self.combo_struct.set("Gõ hoặc chọn ở đây...")

        # Phần 2: Nhập thông tin câu ví dụ
        tk.Label(manage_win, text="2. Nhập thông tin câu ví dụ:", font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Label(manage_win, text="Câu tiếng Việt:").pack()
        e_vi = tk.Entry(manage_win, width=50); e_vi.pack()

        tk.Label(manage_win, text="Full Hiragana:").pack()
        e_hira = tk.Entry(manage_win, width=50); e_hira.pack()

        tk.Label(manage_win, text="Câu có Kanji (Tham khảo):").pack()
        e_kanji = tk.Entry(manage_win, width=50); e_kanji.pack()

        def save_logic():
            name = self.combo_struct.get().strip()
            vi = e_vi.get().strip()
            hira = e_hira.get().strip()
            kanji = e_kanji.get().strip()

            if not name or not vi or not hira:
                messagebox.showwarning("Lỗi", "Vui lòng nhập đủ Tên cấu trúc, Câu Việt và Hiragana!")
                return

            # Tìm xem cấu trúc đã tồn tại chưa
            target_struct = None
            for g in self.data_grammar:
                if g['grammar_name'] == name:
                    target_struct = g
                    break
            
            new_sentence = {"vi": vi, "hira": hira, "kanji": kanji}

            if target_struct:
                # Nếu có rồi, chỉ cần thêm câu vào danh sách sentences
                target_struct['sentences'].append(new_sentence)
                messagebox.showinfo("Thành công", f"Đã thêm 1 câu mới vào cấu trúc '{name}'!")
            else:
                # Nếu chưa có, tạo cấu trúc mới hoàn toàn
                self.data_grammar.append({
                    "grammar_name": name,
                    "sentences": [new_sentence]
                })
                messagebox.showinfo("Thành công", f"Đã tạo cấu trúc mới '{name}' và thêm câu ví dụ!")
                # Cập nhật lại danh sách trong Combobox
                self.combo_struct['values'] = [g['grammar_name'] for g in self.data_grammar]

            self.save_data()
            e_vi.delete(0, tk.END); e_hira.delete(0, tk.END); e_kanji.delete(0, tk.END)

        tk.Button(manage_win, text="LƯU DỮ LIỆU", command=save_logic, bg="#4CAF50", fg="white", pady=10, width=20).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppHocNguPhap(root)
    root.mainloop()