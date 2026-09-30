import streamlit as st
import pandas as pd
import plotly.express as px

combinations = [
    [5, 6, 9, 1],  [5, 6, 9, 2],  [5, 6, 9, 3], 
    [5, 6, 9, 4],  [5, 6, 9, 7],  [5, 6, 9, 8], 
    [5, 6, 9, 10], [5, 6, 10, 1], [5, 6, 10, 2], 
    [5, 6, 10, 3], [5, 6, 10, 4], [5, 6, 10, 7], 
    [5, 6, 10, 8],
]

windsim_aug_rmse = [
    0.43, 0.47, 0.40, 0.45, 0.50, 0.50, 0.48, 0.63, 0.56, 0.68, 0.55, 0.55, 0.50,
]
windsim_feb_rmse = [
    0.84, 0.73, 0.82, 0.96, 1.00, 0.57, 1.06, 0.75, 0.73, 0.76, 0.91, 0.92, 0.66,
]

# Meteodyn RMSE values, keyed by their source combination order.
meteodyn_aug_combinations = [
    [5, 6, 9, 1],  [5, 6, 9, 2],  [5, 6, 9, 3], 
    [5, 6, 9, 4],  [5, 6, 9, 7],  [5, 6, 9, 8], 
    [5, 6, 9, 10], [5, 6, 10, 1], [5, 6, 10, 2], 
    [5, 6, 10, 3], [5, 6, 10, 4], [5, 6, 10, 7], 
    [5, 6, 10, 8],
]
meteodyn_aug_rmse = [
    0.42, 0.42, 0.33, 0.29, 0.54, 0.39, 0.45, 0.33, 0.34, 0.35, 0.41, 0.41, 0.37,
]

meteodyn_feb_combinations = [
    [5, 6, 9, 1],  [5, 6, 9, 2],  [5, 6, 9, 3], 
    [5, 6, 9, 4],  [5, 6, 9, 7],  [5, 6, 9, 8], 
    [5, 6, 9, 10], [5, 6, 10, 1], [5, 6, 10, 2], 
    [5, 6, 10, 3], [5, 6, 10, 4], [5, 6, 10, 7], 
    [5, 6, 10, 8],
]
meteodyn_feb_rmse = [
    1.17, 0.95, 1.11, 1.09, 1.26, 0.60, 1.26, 0.97, 0.88, 0.97, 1.03, 1.08, 0.92, 
]


def combination_key(combination):
    return tuple(sorted(combination))


def build_comparison_frame(meteodyn_combinations, meteodyn_values, windsim_values):
    if len(combinations) != 13 or len(windsim_values) != len(combinations):
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

st.title("Four-Station RMSE Comparison")
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