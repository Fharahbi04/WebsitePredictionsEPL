# ⚽ WebsitePredictionsEPL

Aplikasi web berbasis **Streamlit** untuk melakukan prediksi hasil pertandingan **English Premier League (EPL)** menggunakan **Random Forest Classifier**.

---

## 🚀 Features
- Prediksi hasil pertandingan EPL berdasarkan data input.
- Mendukung encoding tim dan status pertandingan.
- Upload data dalam format CSV untuk diprediksi.
- Tampilan interaktif berbasis Streamlit.

---

## 📂 Project Structure

├── app.py # Main Streamlit app
├── model_randomforest.pkl # Trained Random Forest model
├── status_encoder.pkl # Encoder untuk status pertandingan
├── team_encoder.pkl # Encoder untuk tim
├── requirements.txt # Daftar dependencies
└── data/ # (opsional) dataset EPL
---

## 🛠 Installation
### Clone
1. Clone repository:
   ```bash
   git clone https://github.com/USERNAME/WebsitePredictionsEPL.git
   cd WebsitePredictionsEPL
### Requirements
pip install -r requirements.txt
### Run Streamlit
streamlit run epl.py
