# FCD2627_G2

End-to-end data science project developed for the Foundations of Data Science (FCD) course at Ciências ULisboa[cite: 2].

---

## 🎯 Project Scope & Objectives

Based on the official project guidelines, this project covers an end-to-end data science pipeline[cite: 2], structured around the following key phases:
- **Research Question & Goal:** Define a clear analytical objective (Predictive, Descriptive/Exploratory, or Classification) using two or more structured tabular datasets[cite: 3].
- **Ethics & Regulation:** Address data privacy, consent, potential model biases, transparency, fairness, and accountability[cite: 3].
- **Data Understanding & Quality (M+A):** Analyze dataset size, attributes, types, missing values, quality issues, and attribute transformation needs[cite: 3].
- **Data Cleaning & Integration:** Implement missing data imputation, entity similarity/deduplication rules, define an integrated data model (ER/relational), and build automated scripts to extract and integrate data sources[cite: 4].
- **Machine Learning & Explainability:** Apply both interpretable and black-box models, perform feature selection and train/test splits, evaluate metrics, and extract explanations using SHAP or LIME[cite: 4].
- **Research Paper & Code:** Deliver a production-ready codebase, a Jupyter Notebook, and an 8-page research paper following the ACM primary article template[cite: 2, 4].

---

## 📁 Project Structure

```text
FCD2627_G2/
├── data/
│   ├── raw/          # Raw datasets fetched via automation scripts (ignored by Git)
│   └── processed/    # Lightweight, processed datasets (tracked by Git)
├── notebooks/        # Jupyter Notebooks for exploratory analysis and modeling
├── src/
│   ├── extract.py    # Extraction script (e.g., via curl/API)
│   └── process.py    # Cleaning, transformation, and integration script
├── .gitignore        # Git ignore rules (includes fcd_env/)
├── requirements.txt  # Project Python dependencies (pandas, scikit-learn, requests, shap, dice-ml)
└── README.md         # Documentation and setup instructions

📋 Prerequisites

Before running the project, ensure you have installed:

    Python 3.x

    VS Code

⚙️ Setup & Virtual Environment (fcd_env)
1. Clone the repository
Bash

git clone [https://github.com/your-username/FCD2627_G2.git](https://github.com/your-username/FCD2627_G2.git)
cd FCD2627_G2

2. Create and activate the custom virtual environment

    macOS / Linux:
    Bash

    python3 -m venv fcd_env
    source fcd_env/bin/activate

    Windows (PowerShell):
    Bash

    python -m venv fcd_env
    fcd_env\Scripts\Activate.ps1

    Windows (Command Prompt):
    Bash

    python -m venv fcd_env
    fcd_env\Scripts\activate.bat

3. Install dependencies
Bash

pip install -r requirements.txt

🚀 Data Pipeline Workflow

Due to size limits and .gitignore configurations, raw data in data/raw/ is not tracked by Git. Follow these steps to run the pipeline locally:
Step 1: Extract Data

Run the extraction script to download raw datasets into data/raw/:
Bash

python src/extract.py

Step 2: Process Data

Run the processing script to clean, transform, and output integrated datasets to data/processed/:
Bash

python src/process.py

Note: Only lightweight files saved under data/processed/ will be committed to GitHub.
