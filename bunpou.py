import streamlit as st
import json
import os
import random

# Định vị file data.json nằm ngay cạnh file main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data.json")

def load_data():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

# --- GIAO DIỆN ---
st.set_page_config(page_title="N4 Thần Tốc", layout="centered")
st.title("🏯 Học Ngữ Pháp N4/N3")

data = load_data()

if not data:
    st.error(f"⚠️ Không tìm thấy dữ liệu trong file: {file_path}")
    st.info("Bro kiểm tra xem file data.json đã được upload lên cùng chỗ với main.py chưa nhé!")
else:
    st.success(f"✅ Đã kết nối kho tri thức! (Đang có {len(data)} cấu trúc)")
    
    # Logic luyện tập (Rút gọn cho nhẹ máy)
    if 'q' not in st.session_state:
        struct = random.choice(data)
        st.session_state.q = random.choice(struct['sentences'])
        st.session_state.s_name = struct['grammar_name']

    st.info(f"Cấu trúc: {st.session_state.s_name}")
    st.subheader(st.session_state.q['vi'])
    
    ans = st.text_input("Nhập Hiragana:")
    if st.button("Kiểm tra"):
        if ans.strip().replace(" ","") == st.session_state.q['hira'].strip().replace(" ",""):
            st.balloons()
            st.success("Quá giỏi bro ơi!")
        else:
            st.error(f"Đáp án đúng: {st.session_state.q['hira']}")
            
    if st.button("Câu tiếp theo ➡️"):
        if 'q' in st.session_state: del st.session_state.q
        st.rerun()