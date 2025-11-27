
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core.models import Loan
from core.pipeline import run_qio_single, run_greedy_single, run_variance_experiment

st.set_page_config(page_title="Mortgage QIO Optimizer", layout="wide")

st.title("Quantum-Inspired Mortgage Pool Optimizer")
st.markdown(
    "Upload an Excel file of loans, then compare a **quantum-inspired optimizer** "
    "with a simple **greedy baseline** for secondary-market pool construction."
)

uploaded = st.file_uploader("Upload Excel file with loan data", type=["xlsx"])

if uploaded is None:
    st.info("You can also try the built-in sample dataset from the `data/` folder when running locally.")
else:
    df = pd.read_excel(uploaded)
    st.subheader("Raw Loan Data")
    st.dataframe(df.head(20), use_container_width=True)

    loans = []
    for _, row in df.iterrows():
        loans.append(
            Loan(
                id=str(row["loan_id"]),
                rate=float(row["rate"]),
                fico=int(row["fico"]),
                ltv=float(row["ltv"]),
                dti=float(row["dti"]),
                state=str(row["state"]),
                balance=float(row["balance"]),
            )
        )

    if st.button("Run Optimization", type="primary"):
        with st.spinner("Running QIO and greedy baseline..."):
            q_pool, q_metrics, q_score = run_qio_single(loans)
            g_pool, g_metrics, g_score = run_greedy_single(loans)
            variance_summary = run_variance_experiment(loans)

        st.success("Optimization complete.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### QIO Optimized Pool")
            st.write(f"Selected loans: {len(q_pool)}")
            st.dataframe(pd.DataFrame([vars(l) for l in q_pool]), use_container_width=True)

        with col2:
            st.markdown("### Greedy Baseline(heuristic) Pool")
            st.write(f"Selected loans: {len(g_pool)}")
            st.dataframe(pd.DataFrame([vars(l) for l in g_pool]), use_container_width=True)

        st.markdown("### Pool Metrics Comparison")
        metrics_df = pd.DataFrame(
            {
                "metric": list(q_metrics.keys()),
                "QIO": list(q_metrics.values()),
                "Greedy": [g_metrics[m] for m in q_metrics.keys()],
            }
        )
        st.dataframe(metrics_df, use_container_width=True)

        st.markdown("#### Composite Score")
        st.write(f"QIO: **{q_score:.4f}** | Greedy: **{g_score:.4f}**")

        fig, ax = plt.subplots()
        indices = range(3)
        q_vals = [q_metrics["WAC"], q_metrics["WA_FICO"], q_metrics["WA_LTV"]]
        g_vals = [g_metrics["WAC"], g_metrics["WA_FICO"], g_metrics["WA_LTV"]]
        width = 0.35

        ax.bar([i - width/2 for i in indices], q_vals, width, label="QIO")
        ax.bar([i + width/2 for i in indices], g_vals, width, label="Greedy")

        ax.set_xticks(list(indices))
        ax.set_xticklabels(["WAC", "WA_FICO", "WA_LTV"])
        ax.set_ylabel("Value")
        ax.set_title("Core Pool Quality Metrics")
        ax.legend()
        st.pyplot(fig)

        st.markdown("### Variance Across Multiple Runs")
        var_df = pd.DataFrame(
            {
                "method": ["QIO", "Greedy"],
                "mean_composite_score": [variance_summary["qio"]["mean"], variance_summary["greedy"]["mean"]],
                "std_composite_score": [variance_summary["qio"]["std"], variance_summary["greedy"]["std"]],
            }
        )
        st.dataframe(var_df, use_container_width=True)

        qio_df = pd.DataFrame([vars(l) for l in q_pool])
        greedy_df = pd.DataFrame([vars(l) for l in g_pool])

        st.markdown("### Download Results")
        qio_csv = qio_df.to_csv(index=False).encode("utf-8")
        greedy_csv = greedy_df.to_csv(index=False).encode("utf-8")

        st.download_button("Download QIO Pool as CSV", qio_csv, "qio_pool.csv", "text/csv")
        st.download_button("Download Greedy Pool as CSV", greedy_csv, "greedy_pool.csv", "text/csv")
