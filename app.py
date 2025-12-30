import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Semantic Data Refinement")

# --- Session State ---

if "processed_data" not in st.session_state:
    st.session_state["processed_data"] = None
if "last_target_row" not in st.session_state:
    st.session_state["last_target_row"] = ""


# --- UI: File Upload ---

st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

@st.cache_data
def load_data(file):
    try:
        df = pd.read_excel(file)
        # Converting column headers to string to prevent data type mismatch
        df.columns = [str(col).strip() for col in df.columns]
        # The line below solves the "Expected bytes" error
        df.fillna("")
        return df
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None


# --- UI Logic ---

if uploaded_file is not None:
    df = load_data(uploaded_file)

    if df is not None:
        col_pick, col_original, col_processed = st.columns([1, 2, 3])

        with col_pick:
            st.subheader("⚙️ Settings")
            target_row = st.selectbox("Select Column to Process:", options=df.columns)

            threshold = st.slider("Similarity Threshold", 0.5, 1.0, 0.75, 
                                 help="Lower values group more items together.")

            st.divider()

            if st.button("🚀 Run Analysis", width="stretch"):
                with st.spinner("AI is analyzing the data, please wait..."):
                    # Logic and AI
                    st.success("Analysis completed!")

        with col_original:
            st.subheader("📄 Original Data")
            if target_row in df.columns:
                # df[[target_row]]
                display_df = df[target_row].astype(str) 
                st.dataframe(display_df, width="stretch", height=600)

        with col_processed:
            st.subheader("🤖 Processed Data")
            if st.session_state["processed_data"] is not None and st.session_state["last_target_row"] == target_row:
                processed_df = pd.DataFrame(
                    st.session_state["processed_data"].values,
                    columns=[f"Processed: {target_row}"]
                )

                st.dataframe(processed_df, width="stretch", height=600)

                old_num = len(df[target_row].unique())
                new_num = len(st.session_state["processed_data"].unique())
                st.info(f"Uniqueness: {old_num} unique values → {new_num} unique values")

                csv = processed_df.astype(str).to_csv(index=False).encode("utf-8-sig")
                st.download_button(label="📥 Download (CSV)", data=csv, file_name="output.csv", mime="text/csv")
            
            else:
                st.warning("Click '🚀 Run Analysis' to see the results.")
    else:
        st.error("Failed to process the uploaded file.")
else:
    st.info("👋 Please upload an Excel file to start the semantic transformation.")