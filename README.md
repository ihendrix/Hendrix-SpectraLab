# Hendrix SpectraLab

**Hendrix SpectraLab** is a portable UV-Vis absorbance analysis dashboard for turning raw spectra CSV files into interactive plots, sample-level metrics, automated review flags, and exportable research summaries.

The app is designed for experimental workflows where researchers need to compare many spectra, identify unusual samples, flag data quality issues, and produce clean outputs without relying on hardcoded local files or private lab data.

## Live Demo

[[Open Hendrix SpectraLab
]([url](https://hendrix-spectralab-agoftmmlzwugjr9vmuv4yh.streamlit.app/))](https://hendrix-spectralab-agoftmmlzwugjr9vmuv4yh.streamlit.app/)
Citation

Hendrix, I. (2026).
Hendrix SpectraLab (Version 1.0.0) [Computer software].
Zenodo.
[https://doi.org/10.5281/zenodo.xxxxxxx](https://doi.org/10.5281/zenodo.21228048)

## Demo Data

A synthetic demo CSV is included for testing:

```text
sample_spectra_demo.csv
```

The demo file uses anonymized sample names such as `sample.1`, `sample.2`, and so on. The absorbance values are synthetic and are included only so users can test the app without exposing private lab data.

## What It Does

Hendrix SpectraLab converts raw UV-Vis CSV exports into an interactive scientific analysis workflow. Users can upload spectra files, automatically detect sample curves, filter wavelength ranges, compare absorbance behavior, calculate peak and area metrics, flag data quality concerns, and export processed results.

The app also includes a research review layer that identifies spectra that behave differently from the cohort, detects possible boundary-driven peak artifacts, and generates written review summaries to support lab inspection.

## Key Features

### Data Upload and Selection

* Upload UV-Vis CSV files directly in the browser
* Automatically detect sample spectra from uploaded files
* Search, filter, and select samples
* Adjust wavelength analysis range
* Compare two selected samples side by side

### Visualization

* Display interactive Plotly absorbance curves
* Smooth noisy spectra
* Normalize spectra to compare curve shape
* Show peak markers on selected curves

### Metrics

* Calculate peak wavelength
* Calculate maximum, average, and minimum absorbance
* Calculate area under the curve
* Count saturated readings
* Flag saturated samples when absorbance values are greater than or equal to 9.9

### Export

* Export summary metrics as CSV
* Export selected wavelength-filtered data as CSV
* Export review metrics and written summaries

## Research Review Layer

The review layer is designed to make the app more useful than a basic plotting dashboard.

It can:

* Flag saturated samples
* Identify strongest and weakest absorbers
* Detect unusual absorbance behavior
* Detect peak wavelengths that may be caused by analysis-boundary effects
* Compare samples against cohort-level trends
* Rank samples that may need review
* Distinguish review-worthy samples from confirmed experimental failures
* Generate suggested next steps for lab inspection

This layer does not use an external chatbot or API key. It is based on metrics calculated directly from the uploaded spectra.

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
* Cohort comparison metrics
* Review flags for unusual samples

Metrics are calculated only within the selected wavelength range. This allows users to exclude noisy, irrelevant, or instrument-limited wavelength regions from the analysis.

## Analysis Notes

Saturated readings are flagged when absorbance values are greater than or equal to 9.9.

Peak wavelength should be interpreted carefully when the peak occurs at the edge of the selected wavelength range. In those cases, the peak may reflect the selected analysis boundary rather than a true spectral maximum.

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
├── sample_spectra_demo.csv
└── .gitignore
```

## Data Privacy

This repository does not include private lab data or raw research files. Users upload their own CSV files through the app interface during runtime.

The included demo file is synthetic and anonymized.

## Use Case

This project was built as a portable scientific computing tool for experimental data analysis workflows. It supports quick review of UV-Vis absorbance spectra, sample comparison, peak behavior analysis, unusual-spectrum detection, and clean summary output generation.

## Project Goal

The goal of Hendrix SpectraLab is to move beyond static plots and manual spreadsheet review by providing an interactive, reusable, and research-ready workflow for UV-Vis absorbance analysis.
