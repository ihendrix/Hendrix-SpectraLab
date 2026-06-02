# Hendrix SpectraLab

**Hendrix SpectraLab** is a portable UV-Vis absorbance analysis app for uploading raw spectra CSV files, comparing sample curves, calculating peak metrics, flagging saturated readings, and exporting research-ready results.

## Live Demo

[Open Hendrix SpectraLab](https://hendrix-spectralab-agoftmmlzwugjr9vmuv4yh.streamlit.app/)

## What It Does

Hendrix SpectraLab turns raw UV-Vis CSV exports into an interactive analysis dashboard. Users can upload a spectra file, automatically detect sample curves, filter wavelength ranges, compare absorbance curves, calculate peak absorbance metrics, and download processed results.

The app is designed to make experimental data easier to inspect, compare, and summarize without relying on hardcoded local files.

## Features

* Upload UV-Vis CSV files directly in the browser
* Automatically detect sample spectra from uploaded data
* Search and select specific samples
* Filter by wavelength range
* Smooth noisy curves for cleaner visualization
* Normalize spectra to compare curve shape
* Display interactive Plotly absorbance curves
* Show peak markers on selected spectra
* Calculate peak wavelength and max absorbance
* Calculate average absorbance, minimum absorbance, and area under the curve
* Flag saturated readings when absorbance values are ≥ 9.9
* Export summary metrics as CSV
* Export selected wavelength-filtered data as CSV
* Compare two selected samples side by side

## Analysis Notes

Metrics are calculated within the selected wavelength range. Saturated readings are flagged when absorbance values are ≥ 9.9. Wavelength filtering can exclude noisy or instrument-limited regions from peak calculations.

## Tech Stack

* Python
* Streamlit
* pandas
* NumPy
* Plotly

## Run Locally

Clone the repository:

```bash
git clone https://github.com/ihendrix/Hendrix-SpectraLab.git
cd Hendrix-SpectraLab
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Project Structure

```text
Hendrix-SpectraLab/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Privacy

This repository does not include private lab data or raw research files. Users upload their own CSV files through the app interface during runtime.

## Use Case

This project was built as a portable scientific computing tool for experimental data analysis workflows. It is intended for quickly reviewing UV-Vis absorbance spectra, comparing samples, identifying peak behavior, and producing clean summary outputs.
