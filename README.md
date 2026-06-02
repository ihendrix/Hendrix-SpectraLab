# Hendrix SpectraLab

Portable UV-Vis absorbance analysis software for experimental research workflows.

## What it does
Hendrix SpectraLab converts raw UV-Vis CSV exports into interactive spectra comparisons, peak wavelength metrics, QC flags, and downloadable research-ready summaries.

## Features
- Upload UV-Vis CSV exports
- Automatically detect sample spectra
- Search and select samples
- Filter wavelength range
- Compare absorbance curves interactively
- Calculate peak wavelength and absorbance metrics
- Flag potentially saturated readings
- Export metrics as CSV or Excel

## Tech Stack
Python, Streamlit, pandas, NumPy, Plotly, openpyxl

## Run Locally
pip install -r requirements.txt
streamlit run app.py
