import streamlit as st
import pandas as pd
import joblib
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Streamlit - Model Predictor", layout="wide")
st.image("EPL.png")
st.title("⚽ Website Prediksi Pertandingan Liga Inggris")

# --- Paths to the uploaded files ---
MODEL_PATH = "model_randomforest.pkl"
ENC_STATUS_PATH = "status_encoder.pkl"
ENC_TEAM_PATH = "team_encoder.pkl"

@st.cache_resource
def load_model_and_encoders():
    model = joblib.load(MODEL_PATH)
    encoders = {}
    try:
        encoders['status'] = joblib.load(ENC_STATUS_PATH)
    except Exception:
        encoders['status'] = None
    try:
        encoders['team'] = joblib.load(ENC_TEAM_PATH)
    except Exception:
        encoders['team'] = None
    return model, encoders

model, encoders = load_model_and_encoders()

EXPECTED_FEATURES = None
if hasattr(model, 'feature_names_in_'):
    EXPECTED_FEATURES = list(model.feature_names_in_)

# Helper

def transform_category_column(enc, series):
    if enc is None:
        return series
    if hasattr(enc, 'transform') and not hasattr(enc, 'get_feature_names_out'):
        try:
            return enc.transform(series)
        except Exception:
            return enc.transform(series.astype(str).values)
    if hasattr(enc, 'transform') and hasattr(enc, 'get_feature_names_out'):
        arr = enc.transform(series.values.reshape(-1, 1))
        try:
            arr = arr.toarray()
        except Exception:
            pass
        df_ohe = pd.DataFrame(arr, columns=enc.get_feature_names_out([series.name]))
        return df_ohe
    return series

st.sidebar.image("pl.png")
st.sidebar.title("Panduan Data Encoded")
st.sidebar.write("Harap tulis pada form team_encoded berpedoman pada panduan data dibawah")
contoh=pd.read_csv("dataepl.csv")
ambil=["Team","Team_encoded","Team rating","Round"]
st.sidebar.write(contoh[ambil])
st.sidebar.title("Tentang file model")
st.sidebar.write(f"Model: `{MODEL_PATH}`")
st.sidebar.write(f"Status encoder: `{ENC_STATUS_PATH}` {'(found)' if encoders.get('status') is not None else '(tidak ditemukan)'}")
st.sidebar.write(f"Team encoder: `{ENC_TEAM_PATH}` {'(found)' if encoders.get('team') is not None else '(tidak ditemukan)'}")

st.markdown("---")

st.subheader("1) Prediksi manual (satu baris)")

manual_input = {}

# --- Tambahkan pilihan nama tim di paling atas ---
team_choice = None
if encoders.get('team') is not None and hasattr(encoders['team'], 'classes_'):
    team_classes = list(encoders['team'].classes_)
    team_choice = st.selectbox("Pilih Nama Tim", team_classes)
    manual_input['team'] = team_choice

with st.form(key='manual_form'):
    if EXPECTED_FEATURES is not None:
        st.write("Aplikasi mendeteksi feature yang dipakai model:")
        st.caption(", ".join(EXPECTED_FEATURES))
        for feat in EXPECTED_FEATURES:
            if feat.lower() == 'team':
                continue  # sudah ditangani di atas
            elif 'status' in feat.lower() and encoders.get('status') is not None:
                enc = encoders['status']
                choices = None
                if hasattr(enc, 'classes_'):
                    choices = list(enc.classes_)
                if choices is None:
                    manual_input[feat] = st.text_input(feat, value="")
                else:
                    manual_input[feat] = st.selectbox(feat, choices)
            else:
                try:
                    val = st.number_input(feat, value=0.0, format="%f")
                    manual_input[feat] = val
                except Exception:
                    manual_input[feat] = st.text_input(feat, value="")
    else:
        st.write("Model tidak menyediakan daftar feature secara otomatis.")
        st.caption("Silakan masukkan nama kolom dan nilainya.")
        cols_text = st.text_input('Masukkan nama kolom (dipisah koma)', value='')
        cols = [c.strip() for c in cols_text.split(',') if c.strip()]
        for c in cols:
            manual_input[c] = st.text_input(c, value='')

    submit_manual = st.form_submit_button('Prediksi')

if submit_manual:
    df_row = pd.DataFrame([manual_input])
    for col in df_row.columns:
        try:
            df_row[col] = pd.to_numeric(df_row[col])
        except Exception:
            pass

    expanded = []
    for col in df_row.columns:
        if col.lower() == 'team' and encoders.get('team') is not None:
            transformed = transform_category_column(encoders['team'], df_row[col])
            if isinstance(transformed, pd.DataFrame):
                expanded.append(transformed)
            else:
                df_row[col] = transformed
        elif 'status' in col.lower() and encoders.get('status') is not None:
            transformed = transform_category_column(encoders['status'], df_row[col])
            if isinstance(transformed, pd.DataFrame):
                expanded.append(transformed)
            else:
                df_row[col] = transformed

    if expanded:
        df_row = pd.concat([df_row.drop(columns=[c for c in df_row.columns if c.lower() in ['team', 'status']]), *expanded], axis=1)

    if EXPECTED_FEATURES is not None:
        available = [c for c in EXPECTED_FEATURES if c in df_row.columns]
        missing = [c for c in EXPECTED_FEATURES if c not in df_row.columns]
        if missing:
            st.warning(f"Kolom yang diharapkan oleh model tidak lengkap: {missing}.")
        X = df_row.reindex(columns=available)
    else:
        X = df_row

    try:
        preds = model.predict(X)
        st.success(f"Prediksi: {preds[0]}")
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(X)
            st.write('Probabilitas:', probs[0])
    except Exception as e:
        st.error(f"Terjadi error saat prediksi: {e}")



st.markdown("---")
st.subheader("2) Prediksi batch (unggah CSV)")

uploaded = st.file_uploader("Pilih CSV", type=['csv'])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.write("Preview data:")
    st.dataframe(df.head())

    df_transformed = df.copy()
    if 'team' in df_transformed.columns and encoders.get('team') is not None:
        enc = encoders['team']
        try:
            df_transformed['team'] = enc.transform(df_transformed['team'])
        except Exception:
            st.warning('Gagal mentransform kolom team.')
    if 'status' in df_transformed.columns and encoders.get('status') is not None:
        enc = encoders['status']
        try:
            df_transformed['status'] = enc.transform(df_transformed['status'])
        except Exception:
            st.warning('Gagal mentransform kolom status.')

    if EXPECTED_FEATURES is not None:
        missing = [c for c in EXPECTED_FEATURES if c not in df_transformed.columns]
        if missing:
            st.warning(f"CSV tidak memiliki kolom: {missing}")
        X = df_transformed.reindex(columns=[c for c in EXPECTED_FEATURES if c in df_transformed.columns])
    else:
        X = df_transformed

    try:
        preds = model.predict(X)
        out = df.copy()
        out['prediction'] = preds
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(X)
            out['prob_pred'] = probs.max(axis=1)
        st.write("Hasil prediksi:")
        st.dataframe(out.head())

        towrite = BytesIO()
        out.to_csv(towrite, index=False)
        towrite.seek(0)
        st.download_button(label='Download hasil prediksi CSV', data=towrite, file_name='predictions.csv', mime='text/csv')
    except Exception as e:
        st.error(f"Gagal prediksi batch: {e}")

st.markdown("---")