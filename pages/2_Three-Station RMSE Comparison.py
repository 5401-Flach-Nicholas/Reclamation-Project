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
    [5, 6, 9], [5, 6, 8], [5, 6, 10], [5, 6, 4], [5, 6, 7], [5, 6, 2],
    [5, 7, 9], [5, 7, 8], [5, 7, 10], [5, 7, 4], [5, 7, 2], [5, 6, 1],
    [5, 6, 3], [5, 9, 8], [5, 9, 10], [5, 9, 2], [5, 9, 4], [5, 9, 1],
    [5, 9, 3], [5, 7, 1], [5, 7, 3],
]

windsim_aug_rmse = [
    0.43, 0.49, 0.51, 0.57, 0.58, 0.60, 0.64, 0.74, 0.77, 0.83, 0.85,
    0.86, 0.92, 0.96, 0.98, 0.98, 1.01, 1.11, 1.11, 1.17, 1.17,
]
windsim_feb_rmse = [
    0.92, 1.13, 0.82, 0.86, 0.93, 0.99, 1.06, 1.52, 1.00, 1.13, 1.37,
    1.04, 1.07, 1.40, 1.36, 1.37, 1.39, 1.44, 1.42, 1.48, 1.42,
]

# Meteodyn RMSE values, keyed by their source combination order.
meteodyn_aug_combinations = [
    [5, 6, 9], [5, 6, 8], [5, 6, 10], [5, 6, 4], [5, 6, 7], [5, 6, 2],
    [5, 7, 9], [5, 7, 8], [5, 7, 10], [5, 7, 4], [5, 7, 2], [5, 6, 1],
    [5, 6, 3], [5, 9, 8], [5, 10, 9], [5, 9, 2], [5, 9, 4], [5, 9, 1],
    [5, 9, 3], [5, 7, 1], [5, 7, 3],
]
meteodyn_aug_rmse = [
    0.4687448757815157, 0.41781640363065825, 0.3208378517925482,
    0.4352589163770391, 0.37026671853832993, 0.33231415644150425,
    0.5782282606623196, 0.5875499018320548, 0.5130794870193116,
    0.5893627175663072, 0.5160796810017395, 0.40747559786709053,
    0.4765929515095365, 0.6131525806378516, 0.6370826824562996,
    0.6145059583577224, 0.5612832720013767, 0.6273238603100361,
    0.5887411934433864, 0.6250371086126464, 0.633752470832039,
]

meteodyn_feb_combinations = [
    [5, 6, 9], [5, 6, 8], [5, 6, 10], [5, 6, 4], [5, 6, 7], [5, 6, 2],
    [5, 7, 9], [5, 7, 8], [5, 7, 10], [5, 7, 4], [5, 7, 2], [5, 6, 1],
    [5, 6, 3], [5, 9, 8], [5, 10, 9], [5, 9, 2], [5, 9, 4], [5, 9, 1],
    [5, 9, 3], [5, 7, 1], [5, 7, 3],
]
meteodyn_feb_rmse = [
    1.1851330787239525, 1.457108152667958, 1.0004716966082976,
    0.973044665690415, 0.9715452206224298, 0.8871456676974112,
    1.2057280479918702, 1.5848930793139149, 1.0115339666636438,
    1.0451251934577024, 1.0341750736007627, 0.9052259915149838,
    0.9791898291080087, 0.9884885980988493, 1.313417801550052,
    1.1119654015686433, 1.1886143871872707, 1.2618412323720782,
    1.2106225311207215, 1.0286202422940853, 1.0562402155083581,
]


def combination_key(combination):
    return tuple(sorted(combination))


def build_comparison_frame(meteodyn_combinations, meteodyn_values, windsim_values):
    if len(combinations) != 21 or len(windsim_values) != len(combinations):
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

st.title("Three-Station RMSE Comparison")
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