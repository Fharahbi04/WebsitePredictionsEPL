# st.subheader("Catatan & Troubleshooting")
# st.markdown("""
# - Jika Anda mendapatkan error _The feature names should match those that were passed during fit_, berarti kolom pada data input **tidak sama** (nama atau urutan) dengan yang dipakai saat pelatihan. Jika model dibuat dengan scikit-learn, biasanya model memiliki `feature_names_in_` — periksa bagian sidebar untuk melihatnya.
# - Jika model tidak menyertakan fitur `feature_names_in_`, Anda harus memasukkan nama kolom yang sama seperti saat training.
# - Pastikan encoder untuk kolom kategorikal (mis. `team`, `status`) cocok dengan nilai pada input. Jika Anda melatih encoder di Colab, Anda bisa menyimpannya dengan `joblib.dump(encoder, 'team_encoder.pkl')` lalu unduh file tersebut ke server agar app dapat memuatnya.

# Contoh perintah untuk menyimpan encoder di Colab:
# ```python
# from sklearn.preprocessing import LabelEncoder
# import joblib
# enc = LabelEncoder()
# enc.fit(list_of_categories)
# joblib.dump(enc, 'team_encoder.pkl')
# ```
# Kemudian unduh `team_encoder.pkl` dan `status_encoder.pkl` ke environment yang menjalankan Streamlit (pada contoh ini file ditempatkan di `/mnt/data`).
# """)

# st.write("Selesai — aplikasi siap digunakan.")

# # app.py
# import streamlit as st
# import pandas as pd
# import joblib

# # --- Load model dan encoder ---
# model = joblib.load("model_randomforest.pkl")
# team_encoder = joblib.load("team_encoder.pkl")
# status_encoder = joblib.load("status_encoder.pkl")

# st.set_page_config(page_title="Prediksi EPL", page_icon="⚽", layout="centered")

# st.title("⚽ Prediksi Hasil Pertandingan EPL")
# st.write("Selamat Datang di Website Prediksi Pertandingan Liga Inggris, Berikut Adalah Panduan Referensi Data Pada Tahun 2023/2024")
# # Tampilan = pd.read_excel ("EPL.xlsx")
# # selected_columns = ["Team", "Team rating", "Status","Round"]
# # st.write(Tampilan[selected_columns])


# # --- Sidebar Input ---
# st.sidebar.header("Input Data Pertandingan")

# def user_input():
#     # Informasi umum
#     team_name = st.sidebar.text_input("Masukkan nama tim", "Chelsea")
#     status = st.sidebar.selectbox("Status tim", ["Home", "Guest"])
#     team_rating = st.sidebar.number_input("Masukkan rating tim", min_value=0.0, max_value=10.0, value=6.7)
#     opponent_rating = st.sidebar.number_input("Masukkan rating tim lawan", min_value=0.0, max_value=10.0, value=7.1)
#     round_match = st.sidebar.number_input("Masukkan putaran pertandingan", min_value=1, max_value=38, value=6)

#     st.sidebar.markdown("---")
#     st.sidebar.subheader("Formasi Tim Anda")
#     positions = ["CB", "LB", "RB", "ST", "CM", "AM", "LM", "DM", "LW", "RW", "RM"]
#     team_form = {}
#     for pos in positions:
#         team_form[pos] = st.sidebar.number_input(f"{pos}", min_value=0, max_value=11, value=0)

#     st.sidebar.markdown("---")
#     st.sidebar.subheader("Formasi Tim Lawan")
#     opp_positions = ["CBr", "LBr", "RBr", "STr", "CMr", "AMr", "LMr", "DMr", "LWr", "RWr", "RMr"]
#     opp_form = {}
#     for pos in opp_positions:
#         opp_form[pos] = st.sidebar.number_input(f"{pos}", min_value=0, max_value=11, value=0)

#     # Encode sesuai dengan encoder dari training
#     try:
#         team_val = team_encoder.transform([team_name])[0]
#     except:
#         team_val = 0  # fallback jika tim tidak dikenal
#     try:
#         status_val = status_encoder.transform([status])[0]
#     except:
#         status_val = 0

#     # Gabungkan semua data
#     data = {
#         "Team_encoded": team_val,
#         "Status_encoded": status_val,
#         "Team rating": team_rating,
#         "Rival team rating": opponent_rating,
#         "Round": round_match,
#     }

#     data.update(team_form)
#     data.update(opp_form)

#     return pd.DataFrame([data])

# # Ambil input user
# input_df = user_input()

# st.subheader("📊 Data Input")
# st.write("Harap Pastikan Inputan Benar dan Saran Untuk Pengujian Data Formasi Pemain Dapat Menggunakan Formasi Terakhir Pertandingan")
# st.write(input_df)

# # --- Prediksi ---
# if st.button("Prediksi Hasil"):
#     try:
#         # Pastikan urutan kolom sama dengan training
#         input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)

#         prediction = model.predict(input_df)

#         st.subheader("🔮 Hasil Prediksi")
#         if prediction[0] == "H":
#             st.success("🏠 Home Team Menang")
#         elif prediction[0] == "A":
#             st.success("🚩 Away Team Menang")
#         else:
#             st.success("🤝 Seri")
#     except Exception as e:
#         st.error(f"Terjadi error saat prediksi: {e}")
