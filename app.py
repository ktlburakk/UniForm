import streamlit as st
import pandas as pd
import io
import numpy as np
from src.lm import clean_and_standardize

# --- Sayfa Yapılandırması ---
st.set_page_config(layout="wide", page_title="AI Data Refiner")

# --- Session State (Hafıza Yönetimi) ---
if "master_df" not in st.session_state:
    st.session_state["master_df"] = None
if "current_analysis" not in st.session_state:
    st.session_state["current_analysis"] = None

# --- Fonksiyonlar ---
def highlight_rows(row):
    """Değişen satırları çok hafif bir sarı/mavi tonuyla belirginleştirir (Okunabilirlik için)."""
    # Çok açık sarı/krem rengi metnin okunmasını engellemez
    color = 'background-color: #fff9c4; color: #000000;' if str(row['Original']) != str(row['AI_Refined']) else ''
    return [color] * len(row)

def to_excel(df):
    """Master dataframe'i Excel dosyasına dönüştürür."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Refined_Data')
    return output.getvalue()

# --- Sidebar (Sol Menü) ---
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Yeni dosya yüklendiğinde hafızayı temizle
    file_id = uploaded_file.name + str(uploaded_file.size)
    if "last_file_id" not in st.session_state or st.session_state["last_file_id"] != file_id:
        df_init = pd.read_excel(uploaded_file)
        df_init.columns = [str(col).strip() for col in df_init.columns]
        st.session_state["master_df"] = df_init
        st.session_state["current_analysis"] = None
        st.session_state["last_file_id"] = file_id

    tab_overview, tab_analysis = st.tabs(["📊 Overview & Export", "🧠 AI Refinement"])

    with tab_overview:
        st.subheader("Master Dataset")
        st.write("Bu tablo, yaptığınız tüm 'Apply & Save' işlemlerini içeren güncel ana dosyadır.")
        # Tabloyu her zaman en güncel master_df ile göster
        st.dataframe(st.session_state["master_df"], use_container_width=True, height=500)
        
        st.divider()
        st.subheader("💾 Export Full Dataset")
        if st.session_state["master_df"] is not None:
            full_excel = to_excel(st.session_state["master_df"])
            st.download_button(
                label="📥 Download Updated Excel File",
                data=full_excel,
                file_name="refined_master_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with tab_analysis:
        col_ctrl, col_edit = st.columns([1, 2])

        with col_ctrl:
            st.subheader("Control Panel")
            target_col = st.selectbox("Select Column to Analyze:", options=st.session_state["master_df"].columns)
            threshold = st.slider("Similarity Threshold", 0.5, 1.0, 0.75)
            
            if st.button("🚀 Run AI Analysis", use_container_width=True):
                with st.spinner("AI is analyzing variations..."):
                    refined = clean_and_standardize(st.session_state["master_df"][target_col], threshold)
                    orig = st.session_state["master_df"][target_col].astype(str)
                    
                    st.session_state["current_analysis"] = pd.DataFrame({
                        "Status": np.where(orig != refined, "🔄 Changed", "✅ Same"),
                        "Original": orig,
                        "AI_Refined": refined
                    })

        with col_edit:
            st.subheader("Interactive Editor")
            if st.session_state["current_analysis"] is not None:
                st.info("Edit the 'AI_Refined' column directly. When finished, click 'Save Changes to Master' below.")
                
                # Editor üzerinden yapılan değişiklikleri anlık yakala
                edited_df = st.data_editor(
                    st.session_state["current_analysis"],
                    column_config={
                        "Status": st.column_config.Column(width="small", disabled=True),
                        "Original": st.column_config.Column(disabled=True),
                        "AI_Refined": st.column_config.TextColumn("Refined Value (Editable)")
                    },
                    use_container_width=True,
                    height=400,
                    key="editor_v3"
                )
                
                # Durumu güncelle
                edited_df["Status"] = np.where(edited_df["Original"] != edited_df["AI_Refined"], "🔄 Modified", "✅ Same")

                # --- KRİTİK DÜZELTME: Kaydetme Butonu Editörün Altında ---
                if st.button("💾 Apply & Save to Master Dataset", type="primary", use_container_width=True):
                    final_col_name = f"Refined_{target_col}"
                    # Editördeki en son veriyi (edited_df) ana dataframe'e aktar
                    st.session_state["master_df"][final_col_name] = edited_df["AI_Refined"].values
                    # Güncel veriyi hafızaya al
                    st.session_state["current_analysis"] = edited_df
                    st.success(f"Changes saved! Column '{final_col_name}' added to Master Dataset. Go to 'Overview' to see it.")
                    st.balloons() # Görsel onay

                with st.expander("🔍 View Highlighted Preview (Read-only)"):
                    # Yazıların okunması için çok açık sarı arka plan kullanıldı
                    st.dataframe(edited_df.style.apply(highlight_rows, axis=1), use_container_width=True)
            else:
                st.warning("Please select a column and click 'Run Analysis'.")