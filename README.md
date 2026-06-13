# Hendrix SpectraLab

**Hendrix SpectraLab** is a portable UV-Vis absorbance analysis dashboard for uploading raw spectra CSV files, inspecting sample behavior, calculating research-ready metrics, and running automated review checks on spectral data.

The app is designed for experimental workflows where researchers need to quickly compare many UV-Vis spectra, identify unusual samples, flag data quality issues, and export clean summaries without relying on hardcoded local files or private lab data.

## Live Demo

[Open Hendrix SpectraLab](https://hendrix-spectralab-agoftmmlzwugjr9vmuv4yh.streamlit.app/)

## Demo Data

A synthetic demo CSV is included for testing:

```text
examples/sample_spectra_demo.csv
```

The demo file uses anonymized sample names such as `sample.1`, `sample.2`, and so on. The absorbance values are synthetic and are included only so users can test the app without using private lab data.

## What It Does

Hendrix SpectraLab turns raw UV-Vis CSV exports into an interactive scientific analysis dashboard. Users can upload spectra files, automatically detect sample curves, filter wavelength ranges, compare absorbance behavior, calculate peak and area metrics, flag data quality concerns, and export processed results.

The upgraded review layer adds a more research-oriented workflow by identifying samples that behave differently from the cohort, detecting boundary-driven peak artifacts, comparing spectra to cohort trends, and generating written review summaries.

## Key Features

* Upload UV-Vis CSV files directly in the browser
* Automatically detect sample spectra from uploaded files
* Search, filter, and select samples
* Adjust wavelength analysis range
* Smooth noisy curves
* Normalize spectra to compare curve shape
* Display interactive Plotly absorbance curves
* Show peak markers on selected spectra
* Calculate peak wavelength and max absorbance
* Calculate average absorbance, minimum absorbance, and area under the curve
* Flag saturated readings when absorbance values are ≥ 9.9
* Compare two selected samples side by side
* Export summary metrics as CSV
* Export selected wavelength-filtered data as CSV

## Research Review Layer

The app includes an automated review layer designed to make the analysis more useful than a basic visualization dashboard.

The review layer can:

* Flag saturated samples
* Identify strongest and weakest absorbers
* Detect unusual absorbance behavior
* Detect boundary-driven peak wavelength artifacts
* Compare samples against cohort-level trends
* Rank review-worthy samples
* Distinguish statistical review candidates from confirmed experimental failures
* Generate suggested next steps for lab review
* Export review metrics and written summaries

This layer does not depend on an external chatbot or API key. It uses the experimental metrics calculated inside the app.

## Analysis Metrics

Depending on the uploaded data and selected wavelength range, the app calculates:

* Peak wavelength
* Maximum absorbance
* Average absorbance
* Minimum absorbance
* Area under the curve
* Saturated reading count
* Saturation status
* Absorbance-based review score
* Cohort-level comparison metrics
* Review flags for unusual samples

Metrics are calculated only within the selected wavelength range. This allows users to exclude noisy, irrelevant, or instrument-limited wavelength regions from the analysis.

## Analysis Notes

Saturated readings are flagged when absorbance values are greater than or equal to `9.9`.

Peak wavelength should be interpreted carefully when the peak occurs at the edge of the selected wavelength range. In those cases, the peak may reflect the analysis boundary rather than a true spectral maximum.

Automated review flags are intended to support inspection, not replace scientific judgment. A flagged sample should be treated as review-worthy, not automatically invalid.

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

## Requirements

```text
streamlit
pandas
numpy
plotly
```

## Project Structure

```text
Hendrix-SpectraLab/
├── app.py
├── requirements.txt
├── README.md
├── examples/
│   └── sample_spectra_demo.csv
└── .gitignore
```

## Data Privacy

This repository does not include private lab data or raw research files. Users upload their own CSV files through the app interface during runtime.

The included demo file is synthetic and anonymized.

## Use Case

This project was built as a portable scientific computing tool for experimental data analysis workflows. It is intended for quickly reviewing UV-Vis absorbance spectra, comparing samples, identifying peak behavior, detecting unusual spectra, and producing clean summary outputs for research review.

## Project Goal

The goal of Hendrix SpectraLab is to move beyond static plots and manual spreadsheet review by providing an interactive, reusable, and research-ready workflow for UV-Vis absorbance analysis.

