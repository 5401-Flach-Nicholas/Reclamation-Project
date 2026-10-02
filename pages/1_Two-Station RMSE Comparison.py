import streamlit as st
import pandas as pd
import plotly.express as px

# font size increase

st.markdown("""
<style>
/* Increase normal text */
html, body, [class*="css"] {
    font-size: 21px;
}

/* Title */
h1 {
    font-size: 43px !important;
}

/* Subheaders */
h3 {
    font-size: 30px !important;
}
</style>
""", unsafe_allow_html=True)

combinations = [
    [5, 1], [5, 2], [5, 3], [5, 4], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10],
]

windsim_aug_rmse = [
    1.79, 1.27, 1.69, 1.29, 0.65, 0.97, 1.17, 1.02, 1.21,
]
windsim_feb_rmse = [
    2.11, 1.88, 1.92, 1.57, 0.90, 1.30, 2.17, 1.39, 1.35, 
]

# Meteodyn RMSE values, keyed by their source combination order.
meteodyn_aug_combinations = [
    [5, 1], [5, 2], [5, 3], [5, 4], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10],
]
meteodyn_aug_rmse = [
    0.91, 0.64, 0.75, 0.72, 0.32, 0.54, 0.77, 0.63, 0.60,
]

meteodyn_feb_combinations = [
    [5, 1], [5, 2], [5, 3], [5, 4], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10],
]
meteodyn_feb_rmse = [
    1.25, 1.18, 1.14, 1.16, 0.91, 0.95, 1.93, 1.25, 1.06,
]


def combination_key(combination):
    return tuple(sorted(combination))


def build_comparison_frame(meteodyn_combinations, meteodyn_values, windsim_values):
    if len(combinations) != 9 or len(windsim_values) != len(combinations):
        raise ValueError("Expected WindSim values for all 21 station combinations.")
    if len(meteodyn_combinations) != len(meteodyn_values):
        raise ValueError("Meteodyn combinations and RMSE values must have equal lengths.")

    meteodyn_by_combo = {
        combination_key(combo): rmse
        for combo, rmse in zip(meteodyn_combinations, meteodyn_values)
    }
    windsim_by_combo = {
        combination_key(combo): rmse
        for combo, rmse in zip(combinations, windsim_values)
    }
    missing = set(windsim_by_combo) - set(meteodyn_by_combo)
    if missing:
        raise ValueError(f"Missing Meteodyn RMSE values for: {sorted(missing)}")

    return pd.DataFrame(
        [
            {
                "Station Combination": str(combo),
                "Meteodyn": meteodyn_by_combo[combination_key(combo)],
                "WindSim": windsim_by_combo[combination_key(combo)],
            }
            for combo in combinations
        ]
    )


def show_comparison_chart(period, frame):
    chart_data = frame.melt(
        id_vars="Station Combination", var_name="Software", value_name="RMSE"
    )
    figure = px.bar(
        chart_data,
        x="Station Combination",
        y="RMSE",
        color="Software",
        color_discrete_map={"Meteodyn": "#91C5F7", "WindSim": "#2F69BF"},
        barmode="group",
        title=f"Meteodyn vs WindSim RMSE for {period}",
        category_orders={"Station Combination": frame["Station Combination"].tolist()},
    )
    figure.update_layout(xaxis_tickangle=-45, height=620)
    st.plotly_chart(figure, width="stretch")

# Enable wide mode for the whole page
st.set_page_config(layout="wide")
    
st.title("Two-Station RMSE Comparison")
st.caption("Meteodyn and WindSim errors by station combination, ordered by ascending WindSim error")


august_comparison = build_comparison_frame(
    meteodyn_aug_combinations, meteodyn_aug_rmse, windsim_aug_rmse
)
february_comparison = build_comparison_frame(
    meteodyn_feb_combinations, meteodyn_feb_rmse, windsim_feb_rmse
)

# Reorder the station combinations by WindSim RMSE values in ascending order
august_comparison = august_comparison.sort_values(by='WindSim')
february_comparison = february_comparison.sort_values(by='WindSim')

st.subheader("August 2022")
show_comparison_chart("August 2022", august_comparison)

st.subheader("February 2023")
show_comparison_chart("February 2023", february_comparison)