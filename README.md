<div align="center">

# 🦄 UniForm-mini
### AI-Powered Data Standardization Tool

**Messy Excel files? Typos? Inconsistent casing?**
<br>
*UniForm-mini uses semantic AI to clean, group, and standardize your datasets in seconds.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/Model-MiniLM-yellow?logo=huggingface&logoColor=white)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[View Demo](#) • [Report Bug](issues) • [Request Feature](issues)

</div>

---

## 📖 Overview

**UniForm-mini** is a lightweight, local web application designed to fix inconsistent text data in Excel files. Instead of writing complex RegEx, it uses a **Sentence Transformers** model to understand the semantic similarity of your text.

It detects that `"Apple Inc."`, `"apple inc"`, and `"Apple Incorporated"` are the same entity and standardizes them to a single canonical format automatically.

## ✨ Key Features

* **🧠 Semantic Matching:** Uses `paraphrase-multilingual-MiniLM-L12-v2` to group similar texts.
* **⚡ Interactive Editor:** Review AI suggestions and edit values manually in real-time.
* **📊 Excel Integration:** Seamlessly upload `.xlsx` files and download the cleaned version.
* **🛡️ Data Privacy:** Runs entirely locally; no data is sent to the cloud.
* **🎨 Smart Formatting:** Automatically capitalizes and trims whitespace.

## 📸 Screenshots

| **Dashboard & Upload** | **AI Analysis & Editing** |
|:----------------------:|:-------------------------:|
| ![Dashboard](https://via.placeholder.com/400x200?text=Dashboard+View) | ![Analysis](https://via.placeholder.com/400x200?text=AI+Refinement+View) |

## 🛠️ Installation

To keep the installation "mini" and fast, we install the **CPU version** of Torch, avoiding heavy GPU (CUDA) dependencies (~2GB vs ~150MB).

### Step-by-Step

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/yourusername/uniform-mini.git
    cd uniform-mini
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Torch (CPU Version)**
    ```bash
    pip install sentence-transformers --extra-index-url https://download.pytorch.org/whl/cpu
    ```

4.  **Install Other Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📦 Dependencies

```text
streamlit
pandas
sentence-transformers
openpyxl
xlsxwriter
numpy
sentence-transformers
```

## 🚀 Usage Guide

1.  **Upload Data:** Drag & drop your Excel file (`.xlsx` or `.xls`) into the sidebar. The app will automatically load the **Overview** tab.
2.  **Analyze Column:**
    * Navigate to the **"🧠 AI Refinement"** tab.
    * Select the target column you want to clean (e.g., *Customer Name*, *City*).
    * Set the **Similarity Threshold** (Default: 0.75). Higher values mean stricter matching.
    * Click **🚀 Run AI Analysis**.
3.  **Review & Edit:**
    * The app compares **Original** vs **AI Refined** values.
    * Rows that will be changed are visually highlighted for easy tracking.
    * Use the interactive table to make manual corrections to the `AI_Refined` column if necessary.
4.  **Save Changes:**
    * Select your saving preference:
        * **Update Original Column:** Overwrites the raw data (Recommended for direct cleaning).
        * **Create New Column:** Adds a `Refined_ColumnName` to the dataset.
    * Click **💾 Apply & Save to Master Dataset**.
5.  **Export:** Go back to the **Overview** tab and click **📥 Download Updated Excel File** to get your cleaned data.

## 🧠 How It Works



1.  **Vectorization:** The app converts every unique text entry into a 384-dimensional vector using the `paraphrase-multilingual-MiniLM-L12-v2` model.
2.  **Cosine Similarity:** It calculates the mathematical "angle" between these vectors to determine semantic similarity.
3.  **Clustering:** Values that have a similarity score above your defined threshold are grouped together.
4.  **Canonical Selection:** The shortest and clearest representation in each group is automatically chosen as the "Standard" (canonical) value.

## 📂 Project Structure

```bash
uniform-mini/
├── src/
│   ├── __init__.py
│   └── lm.py          # AI Logic, Semantic Mapping & Model Loader
├── app.py             # Main Streamlit Application (UI & State Management)
├── requirements.txt   # Python Dependencies
├── LICENSE            # MIT License File
├── README.md          # Project Documentation
└── .gitignore         # Ignored files (venv, __pycache__, etc.)
```

## 🤝 Contributing

Contributions make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.



1. **Fork** the Project.
2. **Create** your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the Branch (`git push origin feature/AmazingFeature`).
5. **Open** a Pull Request.

## 📄 License

Distributed under the Apache-2.0 License. See `LICENSE` file for more information.

---

<div align="center">
  <p>Made with ❤️ by Burak Kutlu</p>
</div>