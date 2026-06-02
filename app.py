import re
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
    /* App background */
    .stApp {
        background: #0a0b0f;
        color: #f5f3ee;
    }
    /* Main content width feel */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #12141a;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] * {
        color: #f5f3ee;
    }
    /* Typography */
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
    /* Metric cards */
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
    /* Panels */
    .soft-panel {
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.018));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 24px;
        padding: 1.2rem 1.25rem;
        margin-bottom: 1rem;
    }
    /* Sample pills */
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
    /* Streamlit tab polish */
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
    /* DataFrame / expander vibe */
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
    /* Reduce top gap after tabs sometimes */
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
        identifying peak wavelengths, and exporting research-ready metrics.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Upload CSV
# ============================================================
uploaded_file = st.file_uploader(
    "Upload your UV-Vis CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Upload a CSV file to begin.")
    st.stop()

df = pd.read_csv(uploaded_file, header=None)

# ============================================================
# Detect samples
# ============================================================
samples = {}
step = 2  # Change to 3 if your CSV has blank spacer columns
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
if search_text.strip():
    search_terms = [
        term.strip().lower()
        for term in re.split(r"[,\s]+", search_text)
        if term.strip()
    ]
    filtered_samples = [
        name for name in sample_names
        if any(term in name.lower() for term in search_terms)
    ]
else:
    filtered_samples = sample_names
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
# Wavelength slider
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
# Helper functions
# ============================================================
def clean_absorbance_curve(data, smooth=True):
    """
    Cleans each spectrum before plotting/metrics:
    - forces numeric wavelength + absorbance
    - removes NaN/infinite values
    - removes impossible absorbance values
    - smooths small instrument noise using rolling median + rolling mean
    """
    clean = data.copy()

    clean["Wavelength"] = pd.to_numeric(clean["Wavelength"], errors="coerce")
    clean["Absorbance"] = pd.to_numeric(clean["Absorbance"], errors="coerce")

    clean = clean.replace([np.inf, -np.inf], np.nan)
    clean = clean.dropna(subset=["Wavelength", "Absorbance"])

    # Keep physically reasonable absorbance values.
    # This removes extreme upload/export artifacts without changing normal UV-Vis curves.
    clean = clean[
        (clean["Absorbance"] >= 0) &
        (clean["Absorbance"] <= 10)
    ].copy()

    clean = clean.sort_values("Wavelength").reset_index(drop=True)

    # Flag saturated / near-saturated instrument readings.
    # These are kept in the data, but clearly marked for review.
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
    # Saturation is checked on the raw numeric values within the selected wavelength range.
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
st.markdown('<div class="soft-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Current Selection</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Selected Samples</div>', unsafe_allow_html=True)
render_sample_pills(selected_samples, max_show=18)
st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# Tabs
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Absorbance Plot",
    "Peak Summary Table",
    "Selected Data",
    "Two-Sample Comparison"
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
                "- Metrics are calculated within the selected wavelength range. "
                "Saturated readings are flagged when absorbance values are ≥ 9.9. "
                "Wavelength filtering can exclude noisy or instrument-limited regions from peak calculations.\n"
                "- Cleaning: non-numeric rows, blank rows, negative absorbance, and extreme values above 10 are removed before plotting."
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
