import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="Hendrix SpectraLab",
    layout="wide"
)

# ============================================================
# Custom styling — Apple x Aritzia vibe
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: #0a0b0f;
        color: #f5f3ee;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: #12141a;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: #f5f3ee;
    }

    .hero-title {
        font-size: 2.45rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #f8f6f1;
        margin-bottom: 0.35rem;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: rgba(245,243,238,0.72);
        margin-bottom: 1.75rem;
        max-width: 980px;
        line-height: 1.5;
    }

    .section-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: rgba(245,243,238,0.55);
        margin-bottom: 0.8rem;
        font-weight: 600;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 650;
        color: #f8f6f1;
        margin-bottom: 0.85rem;
        letter-spacing: -0.02em;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 22px;
        padding: 1.1rem 1.2rem 1rem 1.2rem;
        min-height: 112px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.18);
    }

    .metric-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        color: rgba(245,243,238,0.58);
        margin-bottom: 0.8rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        line-height: 1;
        font-weight: 700;
        letter-spacing: -0.04em;
        color: #faf8f4;
        margin-bottom: 0.25rem;
        word-break: break-word;
    }

    .metric-subtext {
        font-size: 0.82rem;
        color: rgba(245,243,238,0.62);
    }

    .soft-panel {
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.018));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 24px;
        padding: 1.2rem 1.25rem;
        margin-bottom: 1rem;
    }

    .pill-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.35rem;
    }

    .sample-pill {
        display: inline-block;
        padding: 0.55rem 0.85rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.035);
        color: #f5f3ee;
        font-size: 0.9rem;
        line-height: 1;
        letter-spacing: -0.01em;
        white-space: nowrap;
    }

    .sample-pill-muted {
        color: rgba(245,243,238,0.68);
        border-style: dashed;
        background: rgba(255,255,255,0.02);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .stTabs [data-baseweb="tab"] {
        color: rgba(245,243,238,0.72);
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        overflow: hidden;
    }

    details {
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 0.15rem 0.3rem;
        background: rgba(255,255,255,0.02);
    }

    .tight-top {
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Helper UI functions
# ============================================================
def metric_card(label, value, subtext=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sample_pills(samples_list, max_show=None):
    if not samples_list:
        st.markdown(
            """
            <div class="pill-wrap">
                <span class="sample-pill sample-pill-muted">No samples selected</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    shown = samples_list if max_show is None else samples_list[:max_show]
    pills_html = "".join([f'<span class="sample-pill">{sample}</span>' for sample in shown])

    if max_show is not None and len(samples_list) > max_show:
        remaining = len(samples_list) - max_show
        pills_html += f'<span class="sample-pill sample-pill-muted">+{remaining} more</span>'

    st.markdown(f'<div class="pill-wrap">{pills_html}</div>', unsafe_allow_html=True)


# ============================================================
# Header
# ============================================================
st.markdown('<div class="hero-title">Hendrix SpectraLab</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero-subtitle">
        Portable UV-Vis absorbance analysis software for comparing sample spectra,
        identifying peak wavelengths, detecting review-worthy samples, and exporting research-ready metrics.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Upload CSV / demo data / live app link
# ============================================================
LIVE_APP_URL = "https://hendrix-spectralab-agoftmmlzwugjr9vmuv4yh.streamlit.app/"
DEMO_CSV_PATH = Path(__file__).resolve().parent / "sample_spectra_demo.csv"

if "use_demo_csv" not in st.session_state:
    st.session_state.use_demo_csv = False

st.markdown('<div class="section-label">Start an Analysis</div>', unsafe_allow_html=True)

upload_col, demo_col, live_col = st.columns([2.2, 1.05, 1.05])

with upload_col:
    uploaded_file = st.file_uploader(
        "Upload your UV-Vis CSV file",
        type=["csv"],
        help="Upload a CSV exported from your UV-Vis instrument."
    )

with demo_col:
    st.markdown("**Demo data**")

    load_demo = st.button(
        "Load Demo CSV",
        use_container_width=True,
        disabled=not DEMO_CSV_PATH.exists()
    )

    if load_demo:
        st.session_state.use_demo_csv = True

    if DEMO_CSV_PATH.exists():
        st.download_button(
            label="Download Demo CSV",
            data=DEMO_CSV_PATH.read_bytes(),
            file_name="sample_spectra_demo.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.caption("Add sample_spectra_demo.csv to the app folder to enable demo data.")

with live_col:
    st.markdown("**Live application**")
    st.link_button(
        "Open Live App ↗",
        LIVE_APP_URL,
        use_container_width=True
    )

if uploaded_file is not None:
    st.session_state.use_demo_csv = False
    df = pd.read_csv(uploaded_file, header=None)
    data_source_name = uploaded_file.name
elif st.session_state.use_demo_csv and DEMO_CSV_PATH.exists():
    df = pd.read_csv(DEMO_CSV_PATH, header=None)
    data_source_name = "sample_spectra_demo.csv"
    st.success("Demo CSV loaded. Use the controls in the sidebar to explore the sample spectra.")
else:
    st.info("Upload a CSV file or select **Load Demo CSV** to begin.")
    st.stop()

# ============================================================
# Detect samples
# ============================================================
samples = {}
step = 2

for col in range(0, df.shape[1], step):
    if col + 1 >= df.shape[1]:
        continue

    sample_name = str(df.iloc[0, col]).strip()

    if sample_name.lower() in ["nan", "", "none"]:
        continue

    wavelength = pd.to_numeric(df.iloc[2:, col], errors="coerce")
    absorbance = pd.to_numeric(df.iloc[2:, col + 1], errors="coerce")

    clean = pd.DataFrame({
        "Wavelength": wavelength,
        "Absorbance": absorbance
    }).dropna()

    clean = clean.sort_values("Wavelength")

    if not clean.empty:
        samples[sample_name] = clean

sample_names = sorted(list(samples.keys()))

if not sample_names:
    st.error("No samples detected. Check the CSV format.")
    st.stop()

# ============================================================
# Sidebar controls
# ============================================================
st.sidebar.markdown("## Controls")

smooth_curves = st.sidebar.checkbox("Smooth curves", value=True)

search_text = st.sidebar.text_input(
    "Search samples",
    placeholder="Example: 77, 81, 59"
)

def sample_name_matches(name, term):
    """Return True only for an exact sample name or exact numeric suffix."""
    normalized_name = str(name).strip().casefold()
    normalized_term = str(term).strip().casefold()

    if not normalized_term:
        return False

    # Full sample names must match exactly: sample.1 does not match sample.11.
    if normalized_name == normalized_term:
        return True

    # Preserve convenient shorthand: "1" matches sample.1, but not sample.11.
    if normalized_term.isdigit():
        suffix_pattern = rf"(?:^|[._\-\s]){re.escape(normalized_term)}$"
        return re.search(suffix_pattern, normalized_name) is not None

    return False


if search_text.strip():
    search_terms = [
        term.strip()
        for term in re.split(r"[,;\n]+", search_text)
        if term.strip()
    ]

    filtered_samples = [
        name for name in sample_names
        if any(sample_name_matches(name, term) for term in search_terms)
    ]
else:
    filtered_samples = sample_names

st.sidebar.caption(
    "Exact matching is enabled. Enter `sample.1` or `1` to select only sample.1. "
    "Separate multiple samples with commas."
)

auto_select_filtered = st.sidebar.checkbox(
    "Auto-select filtered samples",
    value=True
)

if auto_select_filtered:
    selected_samples = filtered_samples
else:
    selected_samples = st.sidebar.multiselect(
        "Choose samples",
        options=filtered_samples,
        default=[]
    )

normalize = st.sidebar.checkbox(
    "Normalize curves",
    value=False,
    help="Divide each spectrum by its own maximum absorbance to compare shape instead of magnitude."
)

show_peak_markers = st.sidebar.checkbox(
    "Show peak markers",
    value=True
)

all_wavelengths = pd.concat(
    [sample_df["Wavelength"] for sample_df in samples.values()],
    ignore_index=True
)

min_wavelength = int(np.floor(all_wavelengths.min()))
max_wavelength = int(np.ceil(all_wavelengths.max()))

default_min = min(max(min_wavelength, 260), max_wavelength)
default_max = max_wavelength

wavelength_min, wavelength_max = st.sidebar.slider(
    "Wavelength range",
    min_value=min_wavelength,
    max_value=max_wavelength,
    value=(default_min, default_max),
    step=1
)

st.sidebar.markdown("---")
st.sidebar.write(f"Total samples detected: **{len(sample_names)}**")
st.sidebar.write(f"Filtered samples: **{len(filtered_samples)}**")
st.sidebar.write(f"Selected samples: **{len(selected_samples)}**")

# ============================================================
# Data helper functions
# ============================================================
def clean_absorbance_curve(data, smooth=True):
    clean = data.copy()

    clean["Wavelength"] = pd.to_numeric(clean["Wavelength"], errors="coerce")
    clean["Absorbance"] = pd.to_numeric(clean["Absorbance"], errors="coerce")

    clean = clean.replace([np.inf, -np.inf], np.nan)
    clean = clean.dropna(subset=["Wavelength", "Absorbance"])

    clean = clean[
        (clean["Absorbance"] >= 0) &
        (clean["Absorbance"] <= 10)
    ].copy()

    clean = clean.sort_values("Wavelength").reset_index(drop=True)

    clean["Saturated"] = clean["Absorbance"] >= 9.9

    if smooth:
        clean["Absorbance_Clean"] = (
            clean["Absorbance"]
            .rolling(window=5, center=True, min_periods=1)
            .median()
            .rolling(window=5, center=True, min_periods=1)
            .mean()
        )
    else:
        clean["Absorbance_Clean"] = clean["Absorbance"]

    return clean


def filter_by_wavelength(data):
    return data[
        (data["Wavelength"] >= wavelength_min) &
        (data["Wavelength"] <= wavelength_max)
    ].copy()


def area_under_curve(y_values, x_values):
    if hasattr(np, "trapezoid"):
        return np.trapezoid(y_values, x_values)
    return np.trapz(y_values, x_values)


def calculate_sample_metrics(sample_name, data):
    raw_data = data.copy()
    raw_data["Wavelength"] = pd.to_numeric(raw_data["Wavelength"], errors="coerce")
    raw_data["Absorbance"] = pd.to_numeric(raw_data["Absorbance"], errors="coerce")
    raw_data = raw_data.replace([np.inf, -np.inf], np.nan)
    raw_data = raw_data.dropna(subset=["Wavelength", "Absorbance"])
    raw_data = filter_by_wavelength(raw_data)

    saturated_count = int((raw_data["Absorbance"] >= 9.9).sum()) if not raw_data.empty else 0
    saturated_status = "Flagged" if saturated_count > 0 else "Clear"

    data = clean_absorbance_curve(data, smooth=smooth_curves)
    data = filter_by_wavelength(data)

    if data.empty:
        return {
            "Sample": sample_name,
            "Peak Wavelength": np.nan,
            "Max Absorbance": np.nan,
            "Average Absorbance": np.nan,
            "Minimum Absorbance": np.nan,
            "Area Under Curve": np.nan,
            "Saturated Status": saturated_status,
            "Saturated Readings": saturated_count,
        }

    max_idx = data["Absorbance_Clean"].idxmax()
    max_absorbance = data.loc[max_idx, "Absorbance_Clean"]
    peak_wavelength = data.loc[max_idx, "Wavelength"]
    avg_absorbance = data["Absorbance_Clean"].mean()
    min_absorbance = data["Absorbance_Clean"].min()

    auc = area_under_curve(
        data["Absorbance_Clean"].to_numpy(),
        data["Wavelength"].to_numpy()
    )

    return {
        "Sample": sample_name,
        "Peak Wavelength": peak_wavelength,
        "Max Absorbance": max_absorbance,
        "Average Absorbance": avg_absorbance,
        "Minimum Absorbance": min_absorbance,
        "Area Under Curve": auc,
        "Saturated Status": saturated_status,
        "Saturated Readings": saturated_count,
    }


# ============================================================
# AI helper functions
# ============================================================
def ai_review_summary(summary_df):
    if summary_df.empty:
        return "No samples selected, so there is nothing to review yet."

    review = []

    flagged = summary_df[summary_df["Saturated Status"] == "Flagged"]

    if len(flagged) > 0:
        review.append(
            f"{len(flagged)} sample(s) contain saturated readings. These should be reviewed before using peak absorbance as a final result."
        )
    else:
        review.append(
            "No saturation issues were detected in the selected wavelength window."
        )

    valid_df = summary_df.dropna(
        subset=["Max Absorbance", "Peak Wavelength", "Area Under Curve"]
    )

    if valid_df.empty:
        return "The selected samples do not contain enough valid numeric data for automated review."

    strongest = valid_df.sort_values("Max Absorbance", ascending=False).iloc[0]
    weakest = valid_df.sort_values("Max Absorbance", ascending=True).iloc[0]

    review.append(
        f"The strongest absorbing sample is {strongest['Sample']} with a max absorbance of {strongest['Max Absorbance']:.4f}."
    )

    review.append(
        f"The weakest absorbing sample is {weakest['Sample']} with a max absorbance of {weakest['Max Absorbance']:.4f}."
    )

    peak_spread = valid_df["Peak Wavelength"].max() - valid_df["Peak Wavelength"].min()

    if peak_spread <= 5:
        review.append(
            "Peak wavelengths are tightly grouped, suggesting the selected samples likely share a similar spectral response."
        )
    elif peak_spread <= 25:
        review.append(
            "Peak wavelengths show moderate variation, which may indicate concentration differences, sample variation, or processing effects."
        )
    else:
        review.append(
            "Peak wavelengths vary substantially. This may suggest different sample behavior, contamination, instrument artifacts, or a meaningful material difference."
        )

    auc_spread = valid_df["Area Under Curve"].max() - valid_df["Area Under Curve"].min()

    review.append(
        f"The AUC spread across selected samples is {auc_spread:.4f}, which reflects total absorbance differences across the selected wavelength range."
    )

    return "\n\n".join(review)


def detect_outlier_samples(summary_df):
    if summary_df.empty or len(summary_df) < 3:
        return pd.DataFrame()

    df = summary_df.copy()

    metric_cols = [
        "Max Absorbance",
        "Area Under Curve",
        "Peak Wavelength"
    ]

    for col in metric_cols:
        mean = df[col].mean()
        std = df[col].std()

        if std == 0 or np.isnan(std):
            df[f"{col} Z-Score"] = 0
        else:
            df[f"{col} Z-Score"] = (df[col] - mean) / std

    df["AI Flag Score"] = (
        df["Max Absorbance Z-Score"].abs()
        + df["Area Under Curve Z-Score"].abs()
        + df["Peak Wavelength Z-Score"].abs()
    )

    df["AI Review Flag"] = np.where(
        df["AI Flag Score"] >= 3,
        "Review",
        "Normal"
    )

    return df.sort_values("AI Flag Score", ascending=False)


def generate_ai_next_steps(summary_df):
    if summary_df.empty:
        return []

    next_steps = []

    if (summary_df["Saturated Status"] == "Flagged").any():
        next_steps.append(
            "Re-run or dilute saturated samples before treating peak absorbance as final."
        )

    if len(summary_df) >= 3:
        ai_flags = detect_outlier_samples(summary_df)
        if not ai_flags.empty and (ai_flags["AI Review Flag"] == "Review").any():
            flagged_samples = ai_flags[ai_flags["AI Review Flag"] == "Review"]["Sample"].tolist()
            next_steps.append(
                f"Manually inspect flagged sample(s): {', '.join(flagged_samples)}."
            )

    peak_spread = summary_df["Peak Wavelength"].max() - summary_df["Peak Wavelength"].min()

    if peak_spread > 25:
        next_steps.append(
            "Check whether peak shifts match expected chemistry/material behavior or come from measurement artifacts."
        )

    if not next_steps:
        next_steps.append(
            "Export the summary table and use the current wavelength window for consistent reporting."
        )

    return next_steps


# ============================================================
# Calculations
# ============================================================
summary_rows = [
    calculate_sample_metrics(sample, samples[sample])
    for sample in selected_samples
]

summary_df = pd.DataFrame(summary_rows)

if not summary_df.empty:
    summary_df = summary_df.sort_values("Max Absorbance", ascending=False)

highest_sample = "None"

if not summary_df.empty and not summary_df["Max Absorbance"].isna().all():
    highest_sample = str(summary_df.iloc[0]["Sample"])

peak_range_value = "None"

if not summary_df.empty and not summary_df["Peak Wavelength"].isna().all():
    peak_min = summary_df["Peak Wavelength"].min()
    peak_max = summary_df["Peak Wavelength"].max()
    peak_range_value = f"{peak_min:.1f} – {peak_max:.1f} nm"

saturated_sample_count = 0

if not summary_df.empty and "Saturated Status" in summary_df.columns:
    saturated_sample_count = int((summary_df["Saturated Status"] == "Flagged").sum())

# ============================================================
# Metric cards
# ============================================================
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    metric_card("Total Samples", len(sample_names), "Detected in uploaded CSV")

with m2:
    metric_card("Selected Samples", len(selected_samples), "Currently active in the dashboard")

with m3:
    metric_card("Highest Absorbance Sample", highest_sample, "Within current wavelength window")

with m4:
    metric_card("Peak Wavelength Range", peak_range_value, "Across selected samples")

with m5:
    metric_card("Saturated Samples", saturated_sample_count, "Flagged at ≥ 9.9 absorbance")

# ============================================================
# Selected sample summary panel
# ============================================================
st.markdown('<div class="section-label">Current Selection</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Selected Samples</div>', unsafe_allow_html=True)
render_sample_pills(selected_samples, max_show=18)

# ============================================================
# Tabs
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Absorbance Plot",
    "Peak Summary Table",
    "Selected Data",
    "Two-Sample Comparison",
    "AI Review"
])

# ============================================================
# Tab 1 — Plot
# ============================================================
with tab1:
    st.markdown('<div class="tight-top"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interactive Absorbance Plot</div>', unsafe_allow_html=True)

    if not selected_samples:
        st.warning("No samples selected. Try searching for samples like 77, 59.")
    else:
        fig = go.Figure()

        for sample in selected_samples:
            data = clean_absorbance_curve(samples[sample], smooth=smooth_curves)
            data = filter_by_wavelength(data)

            if data.empty:
                continue

            x_values = data["Wavelength"]
            y_values = data["Absorbance_Clean"]
            max_raw = y_values.max()

            if normalize and max_raw != 0:
                y_plot = y_values / max_raw
            else:
                y_plot = y_values

            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_plot,
                    mode="lines",
                    name=sample,
                    line=dict(width=2),
                    hovertemplate=(
                        "<b>%{fullData.name}</b><br>"
                        "Wavelength: %{x}<br>"
                        "Absorbance: %{y:.5f}<br>"
                        "<extra></extra>"
                    )
                )
            )

            if show_peak_markers:
                max_idx = data["Absorbance_Clean"].idxmax()
                peak_x = data.loc[max_idx, "Wavelength"]
                peak_y_raw = data.loc[max_idx, "Absorbance_Clean"]

                if normalize and max_raw != 0:
                    peak_y_plot = peak_y_raw / max_raw
                else:
                    peak_y_plot = peak_y_raw

                fig.add_trace(
                    go.Scatter(
                        x=[peak_x],
                        y=[peak_y_plot],
                        mode="markers",
                        marker=dict(size=7),
                        name=f"{sample} Peak",
                        hovertemplate=(
                            f"<b>{sample} Peak</b><br>"
                            f"Peak Wavelength: {peak_x:.2f}<br>"
                            f"Max Absorbance: {peak_y_raw:.5f}<br>"
                            "<extra></extra>"
                        ),
                        showlegend=False
                    )
                )

        y_axis_title = "Normalized Absorbance" if normalize else "Absorbance"

        fig.update_layout(
            title=f"Absorbance Curves ({wavelength_min}–{wavelength_max} nm)",
            height=650,
            template="plotly_dark",
            paper_bgcolor="#0a0b0f",
            plot_bgcolor="#0a0b0f",
            font=dict(color="#f5f3ee"),
            xaxis=dict(
                title="Wavelength",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                zeroline=False
            ),
            yaxis=dict(
                title=y_axis_title,
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                zeroline=False
            ),
            hovermode="closest",
            legend=dict(
                title="Samples",
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(255,255,255,0.06)",
                borderwidth=0
            ),
            margin=dict(l=40, r=20, t=70, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Analysis Notes", expanded=True):
            st.write(
                f"- Wavelength window: **{wavelength_min}–{wavelength_max} nm**\n"
                f"- Smoothing: **{'On' if smooth_curves else 'Off'}**\n"
                f"- Peak markers: **{'On' if show_peak_markers else 'Off'}**\n"
                f"- Normalization: **{'On' if normalize else 'Off'}**\n"
                f"- Saturated samples: **{saturated_sample_count}** flagged at absorbance values ≥ 9.9.\n"
                "- Metrics are calculated within the selected wavelength range.\n"
                "- Cleaning removes non-numeric rows, blank rows, negative absorbance values, and extreme values above 10 before plotting."
            )

# ============================================================
# Tab 2 — Summary table
# ============================================================
with tab2:
    st.markdown('<div class="section-title">Peak Summary Table</div>', unsafe_allow_html=True)

    if summary_df.empty:
        st.warning("No samples selected.")
    else:
        display_summary = summary_df.copy()

        numeric_cols = [
            "Peak Wavelength",
            "Max Absorbance",
            "Average Absorbance",
            "Minimum Absorbance",
            "Area Under Curve",
            "Saturated Readings"
        ]

        for col in numeric_cols:
            display_summary[col] = display_summary[col].round(5)

        st.dataframe(display_summary, use_container_width=True)

        summary_csv = display_summary.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Summary Table as CSV",
            data=summary_csv,
            file_name="absorbance_peak_summary.csv",
            mime="text/csv"
        )

# ============================================================
# Tab 3 — Selected data
# ============================================================
with tab3:
    st.markdown('<div class="section-title">Selected Sample Data</div>', unsafe_allow_html=True)

    if not selected_samples:
        st.warning("No samples selected.")
    else:
        selected_dataframes = []

        for sample in selected_samples:
            temp = clean_absorbance_curve(samples[sample], smooth=smooth_curves)
            temp = filter_by_wavelength(temp)

            if not temp.empty:
                temp.insert(0, "Sample", sample)
                selected_dataframes.append(temp)

        if selected_dataframes:
            selected_data = pd.concat(selected_dataframes, ignore_index=True)
            st.dataframe(selected_data, use_container_width=True)

            selected_csv = selected_data.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Selected Data as CSV",
                data=selected_csv,
                file_name="selected_absorbance_data.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data in the selected wavelength range.")

# ============================================================
# Tab 4 — Two-sample comparison
# ============================================================
with tab4:
    st.markdown('<div class="section-title">Two-Sample Comparison</div>', unsafe_allow_html=True)

    if len(selected_samples) < 2:
        st.warning("Select at least two samples to compare.")
    else:
        comparison_samples = st.multiselect(
            "Choose exactly two samples for comparison",
            options=selected_samples,
            default=selected_samples[:2]
        )

        if len(comparison_samples) != 2:
            st.info("Choose exactly two samples.")
        else:
            sample_a, sample_b = comparison_samples

            metrics_a = calculate_sample_metrics(sample_a, samples[sample_a])
            metrics_b = calculate_sample_metrics(sample_b, samples[sample_b])

            max_abs_diff = metrics_a["Max Absorbance"] - metrics_b["Max Absorbance"]
            peak_wave_diff = metrics_a["Peak Wavelength"] - metrics_b["Peak Wavelength"]
            auc_diff = metrics_a["Area Under Curve"] - metrics_b["Area Under Curve"]

            if metrics_b["Max Absorbance"] != 0:
                percent_diff = (max_abs_diff / metrics_b["Max Absorbance"]) * 100
            else:
                percent_diff = np.nan

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                metric_card("Max Absorbance Difference", f"{max_abs_diff:.5f}", f"{sample_a} minus {sample_b}")

            with c2:
                metric_card("Peak Wavelength Difference", f"{peak_wave_diff:.5f}", f"{sample_a} minus {sample_b}")

            with c3:
                metric_card("AUC Difference", f"{auc_diff:.5f}", f"{sample_a} minus {sample_b}")

            with c4:
                percent_display = "N/A" if np.isnan(percent_diff) else f"{percent_diff:.2f}%"
                metric_card("Percent Difference", percent_display, f"Relative to {sample_b}")

            st.markdown(
                f"""
                <div class="soft-panel">
                    Comparison is calculated as <b>{sample_a}</b> minus <b>{sample_b}</b>.
                </div>
                """,
                unsafe_allow_html=True
            )

            comparison_df = pd.DataFrame([metrics_a, metrics_b]).round(5)
            st.dataframe(comparison_df, use_container_width=True)

            data_a = clean_absorbance_curve(samples[sample_a], smooth=smooth_curves)
            data_b = clean_absorbance_curve(samples[sample_b], smooth=smooth_curves)

            data_a = filter_by_wavelength(data_a)
            data_b = filter_by_wavelength(data_b)

            merged = pd.merge(
                data_a[["Wavelength", "Absorbance_Clean"]],
                data_b[["Wavelength", "Absorbance_Clean"]],
                on="Wavelength",
                how="inner",
                suffixes=(f"_{sample_a}", f"_{sample_b}")
            )

            if merged.empty:
                st.warning("Could not create a difference plot because the samples do not share exact wavelength values.")
            else:
                merged["Difference"] = (
                    merged[f"Absorbance_Clean_{sample_a}"] -
                    merged[f"Absorbance_Clean_{sample_b}"]
                )

                diff_fig = go.Figure()

                diff_fig.add_trace(
                    go.Scatter(
                        x=merged["Wavelength"],
                        y=merged["Difference"],
                        mode="lines",
                        name=f"{sample_a} - {sample_b}",
                        line=dict(width=2),
                        hovertemplate=(
                            "<b>Difference</b><br>"
                            "Wavelength: %{x}<br>"
                            "Absorbance Difference: %{y:.5f}<br>"
                            "<extra></extra>"
                        )
                    )
                )

                diff_fig.update_layout(
                    title=f"Difference Plot: {sample_a} – {sample_b}",
                    height=500,
                    template="plotly_dark",
                    paper_bgcolor="#0a0b0f",
                    plot_bgcolor="#0a0b0f",
                    font=dict(color="#f5f3ee"),
                    xaxis=dict(
                        title="Wavelength",
                        showgrid=True,
                        gridcolor="rgba(255,255,255,0.06)",
                        zeroline=False
                    ),
                    yaxis=dict(
                        title="Absorbance Difference",
                        showgrid=True,
                        gridcolor="rgba(255,255,255,0.06)",
                        zeroline=False
                    ),
                    margin=dict(l=40, r=20, t=70, b=40)
                )

                st.plotly_chart(diff_fig, use_container_width=True)

# ============================================================
# Tab 5 — AI Review
# ============================================================
with tab5:
    st.markdown('<div class="section-title">AI Review</div>', unsafe_allow_html=True)

    if summary_df.empty:
        st.warning("No samples selected.")
    else:
        st.markdown("### Automated Interpretation")
        st.info(ai_review_summary(summary_df))

        st.markdown("### Review-Worthy Sample Ranking")

        ai_flags = detect_outlier_samples(summary_df)

        if ai_flags.empty:
            st.write("Select at least three samples to enable group-based review ranking.")
        else:
            display_ai = ai_flags[
                [
                    "Sample",
                    "Max Absorbance",
                    "Peak Wavelength",
                    "Area Under Curve",
                    "Saturated Status",
                    "AI Flag Score",
                    "AI Review Flag"
                ]
            ].copy()

            display_ai = display_ai.round(5)
            st.dataframe(display_ai, use_container_width=True)

            review_count = int((display_ai["AI Review Flag"] == "Review").sum())

            if review_count > 0:
                st.warning(
                    f"{review_count} sample(s) were flagged for review based on unusual absorbance, AUC, or peak wavelength behavior."
                )
            else:
                st.success("No major unusual samples detected among the selected samples.")

        st.markdown("### Suggested Next Steps")

        next_steps = generate_ai_next_steps(summary_df)

        for step_text in next_steps:
            st.write(f"- {step_text}")

        st.markdown("### What This AI Layer Does")
        st.write(
            """
            This AI Review layer is built from the actual experimental metrics in the dashboard.
            It does not depend on an external chatbot or API key.

            It helps:
            - flag saturated samples
            - identify strongest and weakest absorbers
            - detect unusual peak wavelength shifts
            - rank samples that behave differently from the group
            - generate a plain-English review summary
            - suggest next steps for lab review
            """
        )
