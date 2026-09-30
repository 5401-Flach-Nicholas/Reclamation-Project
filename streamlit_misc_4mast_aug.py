import streamlit as st
import pandas as pd
import plotly.express as px

combos = [
    "[5, 6, 10, 3]",
    "[5, 6, 10, 7]",
    "[5, 6, 10, 4]",
    "[5, 6, 9, 10]",
    "[5, 6, 9, 7]",
]

meteodyn_rmse = [0.3456692831787825, 0.40549538016275016, 0.4119625023389062, 0.44658479971146947, 0.5384970163953248]
windsim_rmse = [0.68, 0.55, 0.55, 0.48, 0.50]

meteodyn_misc_aug_ranking = pd.DataFrame(
    {
        "Station_Combination": combos,
        "RMSE": meteodyn_rmse,
        "Software": "Meteodyn",
    }
).sort_values("RMSE", ascending=True).reset_index(drop=True)

windsim_misc_aug_ranking = pd.DataFrame(
    {
        "Station_Combination": combos,
        "RMSE": windsim_rmse,
        "Software": "WindSim",
    }
).sort_values("RMSE", ascending=True).reset_index(drop=True)

comparison_df = pd.concat([meteodyn_misc_aug_ranking, windsim_misc_aug_ranking], ignore_index=True)

st.title("Misc August RMSE Comparison")
st.caption("Grouped bar chart comparing the 5 August misc station combinations")

fig = px.bar(
    comparison_df,
    x="Station_Combination",
    y="RMSE",
    color="Software",
    barmode="group",
    title="Meteodyn vs WindSim RMSE for the 5 Misc August Runs",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Ordered ranking (lowest to highest RMSE)")
st.dataframe(meteodyn_misc_aug_ranking, hide_index=True)