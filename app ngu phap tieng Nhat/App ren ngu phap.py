
import streamlit as st
import json
import os
import random

# --- ĐOẠN FIX LỖI ĐƯỜNG DẪN ---
# Lấy thư mục hiện tại của chính cái file Python này
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nối nó với tên file JSON của ông (Đảm bảo tên file này giống hệt trên GitHub)
FILE_NAME_GR = os.path.join(BASE_DIR, "ngu_phap.json")

def load_data():
    if os.path.exists(FILE_NAME_GR):
        try:
            with open(FILE_NAME_GR, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")
    return []
# ------------------------------

# Tự động xác định file dữ liệu
FILE_NAME_GR = "ngu_phap.json"

def load_data():
    if os.path.exists(FILE_NAME_GR):
        with open(FILE_NAME_GR, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_NAME_GR, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- GIAO DIỆN WEB STREAMLIT ---
st.set_page_config(page_title="Luyện Ngữ Pháp N3/N4", layout="centered")

st.title("🏯 Luyện Ngữ Pháp Tiếng Nhật")

# Khởi tạo dữ liệu
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Tab chức năng
tab1, tab2 = st.tabs(["🚀 Luyện tập", "➕ Thêm cấu trúc"])

with tab1:
    if not st.session_state.data:
        st.info("Kho ngữ pháp trống. Qua tab 'Thêm cấu trúc' để nạp đạn nhé bro!")
    else:
        # Chọn câu hỏi mới nếu chưa có
        if 'current_q' not in st.session_state:
            valid_structs = [g for g in st.session_state.data if g['sentences']]
            if valid_structs:
                struct = random.choice(valid_structs)
                st.session_state.current_q = random.choice(struct['sentences'])
                st.session_state.current_struct = struct['grammar_name']
                st.session_state.show_ans = False

        if 'current_q' in st.session_state:
            st.info(f"Cấu trúc: {st.session_state.current_struct}")
            st.subheader(f"Dịch sang Hiragana: \n {st.session_state.current_q['vi']}")
            
            user_ans = st.text_input("Nhập câu trả lời (Hiragana):", key="input_ans").strip().replace(" ", "")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Kiểm tra"):
                    correct_ans = st.session_state.current_q['hira'].strip().replace(" ", "")
                    if user_ans == correct_ans:
                        st.success("Chuẩn đét! Đỉnh vcl bro! 🌸")
                        st.balloons()
                    else:
                        st.error("Sai rồi, thử lại xem!")
            
            with col2:
                if st.button("Xem đáp án"):
                    st.session_state.show_ans = True
            
            if st.session_state.show_ans:
                st.warning(f"Đáp án: {st.session_state.current_q['hira']}")
                st.write(f"Kanji tham khảo: {st.session_state.current_q.get('kanji', '')}")

            if st.button("Câu tiếp theo ➡️"):
                if 'current_q' in st.session_state:
                    del st.session_state.current_q
                st.rerun()

with tab2:
    st.header("Thêm dữ liệu mới")
    all_struct_names = [g['grammar_name'] for g in st.session_state.data]
    
    selected_struct = st.selectbox("Chọn cấu trúc cũ hoặc 'Tạo mới'", ["-- Tạo mới --"] + all_struct_names)
    
    if selected_struct == "-- Tạo mới --":
        new_struct_name = st.text_input("Tên cấu trúc mới (VD: ~te kudasai)")
    else:
        new_struct_name = selected_struct

    vi = st.text_input("Câu tiếng Việt")
    hira = st.text_input("Câu Hiragana (Đáp án)")
    kanji = st.text_input("Câu Kanji (Tham khảo)")

    if st.button("Lưu câu ví dụ"):
        if new_struct_name and vi and hira:
            new_entry = {"vi": vi, "hira": hira, "kanji": kanji}
            
            found = False
            for g in st.session_state.data:
                if g['grammar_name'] == new_struct_name:
                    g['sentences'].append(new_entry)
                    found = True
                    break
            
            if not found:
                st.session_state.data.append({
                    "grammar_name": new_struct_name,
                    "sentences": [new_entry]
                })
            
            save_data(st.session_state.data)
            st.success("Đã lưu thành công! Quất tiếp đi bro.")
            st.rerun()