import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math

st.set_page_config(page_title="Animal Slaughter Scale Dashboard", layout="wide")

st.title("Animal Slaughter Scale Dashboard")
st.markdown(
    "Scale of animal killing — land and aquatic — backed by USDA NASS/ERS and "
    "peer-reviewed research (Animal Welfare journal, fishcount.org.uk)."
)

tab_land, tab_aquatic, tab_compare, tab_rate = st.tabs(
    ["Land Animals (US)", "Aquatic Animals (Global)", "Scale Comparison", "Kill Rate"]
)

# -- LAND ANIMALS (US, 2023) --------------------------------------------------
# Source: USDA NASS Livestock Slaughter Annual Summary (2025)
# https://www.nass.usda.gov/Publications/Todays_Reports/reports/lstk0325.pdf
land_df = pd.DataFrame({
    "Species": [
        "Broiler Chickens",
        "Turkeys",
        "Cattle & Calves",
        "Hogs",
        "Sheep & Lambs",
        "Ducks & Other Poultry",
    ],
    "Annual Count (2023)": [
        9200000000,
         220000000,
          33000000,
         130000000,
           2000000,
          35000000,
    ],
    "Welfare Coverage": [
        "Excluded from Humane Methods Act",
        "Excluded from Humane Methods Act",
        "Covered by Humane Methods of Slaughter Act",
        "Covered by Humane Methods of Slaughter Act",
        "Covered by Humane Methods of Slaughter Act",
        "Excluded from Humane Methods Act",
    ],
})

total_land = int(land_df["Annual Count (2023)"].sum())
excluded_land = int(land_df[land_df["Welfare Coverage"].str.startswith("Excluded")]["Annual Count (2023)"].sum())
poultry_pct = excluded_land / total_land * 100

with tab_land:
    st.subheader("US Annual Land Animal Slaughter (2023, USDA NASS)")

    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            land_df,
            values="Annual Count (2023)",
            names="Species",
            title="US Land Animal Slaughter by Species (2023)",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Key Stats")
        st.metric("Total Land Animals (US, 2023)", "{:,}".format(total_land))
        st.metric("Poultry share", "{:.1f}%".format(poultry_pct))
        st.metric(
            "Excluded from federal welfare law",
            "{:.1f}% (all birds)".format(poultry_pct),
            help="The Humane Methods of Slaughter Act exempts poultry.",
        )
        st.markdown("---")
        st.dataframe(
            land_df[["Species", "Annual Count (2023)", "Welfare Coverage"]],
            hide_index=True,
        )

    st.caption(
        "Source: USDA NASS Livestock Slaughter Annual Summary "
        "(https://www.nass.usda.gov/Publications/Todays_Reports/reports/lstk0325.pdf). "
        "Poultry counts from USDA NASS Poultry Production reports."
    )

# -- AQUATIC ANIMALS (GLOBAL) -------------------------------------------------
# Wild fish: Mood et al. (2024), Animal Welfare, doi:10.1017/awf.2024.7
# Farmed fish: Mood et al. (2023), Animal Welfare, doi:10.1017/awf.2023.4
# Farmed crustaceans: fishcount.org.uk
# Bycatch: FAO SOFIA 2022 doi:10.4060/cc0461en; individual count est.
# US landings: NOAA Fisheries of the United States 2023

aquatic_df = pd.DataFrame({
    "Category": [
        "Wild-caught fish (global, mid-est.)",
        "Farmed fish (global, 2019)",
        "Farmed crustaceans (global, 2017 mid-est.)",
        "Bycatch / discards (global, est.)",
    ],
    "Annual Count (individuals)": [
        1650000000000,
         124000000000,
         425000000000,
         100000000000,
    ],
    "Low Estimate": [
        1100000000000,
          78000000000,
         250000000000,
          50000000000,
    ],
    "High Estimate": [
        2200000000000,
         171000000000,
         600000000000,
         200000000000,
    ],
    "Source": [
        "Mood et al. 2024, Animal Welfare (doi:10.1017/awf.2024.7)",
        "Mood et al. 2023, Animal Welfare (doi:10.1017/awf.2023.4)",
        "fishcount.org.uk (2017 est.)",
        "FAO SOFIA 2022 (doi:10.4060/cc0461en); individual count est.",
    ],
})

with tab_aquatic:
    st.subheader("Global Aquatic Animal Slaughter (Peer-Reviewed Estimates)")

    st.info(
        "These are individual animal counts, not weight-based tonnage. "
        "Aquatic animals are the most numerically significant victims of industrial food systems "
        "yet receive almost no welfare protections globally."
    )

    col1, col2 = st.columns(2)
    with col1:
        fig_aq = go.Figure()
        fig_aq.add_trace(go.Bar(
            name="Low Estimate",
            x=aquatic_df["Category"],
            y=aquatic_df["Low Estimate"] / 1e9,
            marker_color="#4e9af1",
        ))
        fig_aq.add_trace(go.Bar(
            name="Central Estimate",
            x=aquatic_df["Category"],
            y=aquatic_df["Annual Count (individuals)"] / 1e9,
            marker_color="#f1854e",
        ))
        fig_aq.add_trace(go.Bar(
            name="High Estimate",
            x=aquatic_df["Category"],
            y=aquatic_df["High Estimate"] / 1e9,
            marker_color="#a0d468",
        ))
        fig_aq.update_layout(
            title="Global Aquatic Animal Slaughter (billions/year)",
            yaxis_title="Billions of individuals",
            barmode="group",
        )
        st.plotly_chart(fig_aq, use_container_width=True)

    with col2:
        st.subheader("Key Stats")
        st.metric(
            "Wild fish caught annually (global)",
            "1.1-2.2 trillion",
            help="Mood et al. 2024, Animal Welfare journal",
        )
        st.metric(
            "Farmed fish killed annually (global)",
            "~124 billion",
            help="Mood et al. 2023, Animal Welfare journal (2019 data)",
        )
        st.metric(
            "Farmed crustaceans killed (global)",
            "250-600 billion",
            help="fishcount.org.uk estimates",
        )
        st.metric(
            "Bycatch / discards (global est.)",
            "~100 billion",
            help="FAO SOFIA 2022; individual count estimated from discard weight data",
        )
        st.metric(
            "US commercial landings (weight, 2023)",
            "8.4 billion lbs",
            help="NOAA Fisheries of the United States 2023 report",
        )
        st.markdown("---")
        st.dataframe(
            aquatic_df[["Category", "Low Estimate", "Annual Count (individuals)", "High Estimate"]],
            hide_index=True,
        )

    st.caption(
        "Sources: Mood et al. (2024) https://doi.org/10.1017/awf.2024.7 | "
        "Mood et al. (2023) https://doi.org/10.1017/awf.2023.4 | "
        "fishcount.org.uk | "
        "FAO SOFIA 2022: https://doi.org/10.4060/cc0461en | "
        "NOAA Fisheries of the United States 2023: "
        "https://www.fisheries.noaa.gov/national/sustainable-fisheries/fisheries-united-states"
    )

# -- SCALE COMPARISON ---------------------------------------------------------
with tab_compare:
    st.subheader("Scale Comparison: Land vs. Aquatic")

    st.markdown(
        "Land animal statistics dominate public discourse, yet aquatic animals "
        "are killed in numbers 100-200x greater. They receive almost no legal protection."
    )

    compare_df = pd.DataFrame({
        "Category": [
            "US land animals (2023)",
            "Global farmed fish (2019)",
            "Global farmed crustaceans (2017)",
            "Global bycatch / discards (est.)",
            "Global wild-caught fish (2000-2019 avg)",
        ],
        "Central Estimate (billions)": [9.62, 124, 425, 100, 1650],
        "Welfare Law Coverage": [
            "Partial (mammals only; ~98% birds excluded)",
            "Minimal - no global standard",
            "None",
            "None",
            "None",
        ],
    })

    fig_compare = px.bar(
        compare_df,
        x="Category",
        y="Central Estimate (billions)",
        color="Category",
        title="Annual Animal Slaughter: Land vs. Aquatic (billions of individuals)",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text="Central Estimate (billions)",
    )
    fig_compare.update_traces(texttemplate="%{text:.0f}B", textposition="outside")
    fig_compare.update_layout(showlegend=False, yaxis_title="Billions of individuals")
    st.plotly_chart(fig_compare, use_container_width=True)

    st.dataframe(compare_df, hide_index=True)

    st.markdown(
        "**Why this matters:** The Humane Methods of Slaughter Act covers US cattle, "
        "hogs, and sheep (~165M animals) but explicitly excludes poultry (~9.5B animals). "
        "No comparable federal law exists for aquatic animals. The numbers above represent "
        "the largest unaddressed animal welfare crisis on the planet."
    )

# -- KILL RATE (per second) ---------------------------------------------------
SECONDS_PER_YEAR = 365.25 * 24 * 3600

LAND_US_ANNUAL       =    9620000000
WILD_FISH_ANNUAL     = 1650000000000
FARMED_FISH_ANNUAL   =  124000000000
FARMED_CRUST_ANNUAL  =  425000000000
BYCATCH_ANNUAL       =  100000000000
AQUATIC_TOTAL_ANNUAL = WILD_FISH_ANNUAL + FARMED_FISH_ANNUAL + FARMED_CRUST_ANNUAL + BYCATCH_ANNUAL
ALL_TOTAL_ANNUAL     = LAND_US_ANNUAL + AQUATIC_TOTAL_ANNUAL

rate_df = pd.DataFrame({
    "Category": [
        "US land animals",
        "Global wild-caught fish",
        "Global farmed fish",
        "Global farmed crustaceans",
        "Global bycatch / discards",
    ],
    "Per second": [
        LAND_US_ANNUAL / SECONDS_PER_YEAR,
        WILD_FISH_ANNUAL / SECONDS_PER_YEAR,
        FARMED_FISH_ANNUAL / SECONDS_PER_YEAR,
        FARMED_CRUST_ANNUAL / SECONDS_PER_YEAR,
        BYCATCH_ANNUAL / SECONDS_PER_YEAR,
    ],
    "Per minute": [
        LAND_US_ANNUAL / SECONDS_PER_YEAR * 60,
        WILD_FISH_ANNUAL / SECONDS_PER_YEAR * 60,
        FARMED_FISH_ANNUAL / SECONDS_PER_YEAR * 60,
        FARMED_CRUST_ANNUAL / SECONDS_PER_YEAR * 60,
        BYCATCH_ANNUAL / SECONDS_PER_YEAR * 60,
    ],
    "Per hour": [
        LAND_US_ANNUAL / SECONDS_PER_YEAR * 3600,
        WILD_FISH_ANNUAL / SECONDS_PER_YEAR * 3600,
        FARMED_FISH_ANNUAL / SECONDS_PER_YEAR * 3600,
        FARMED_CRUST_ANNUAL / SECONDS_PER_YEAR * 3600,
        BYCATCH_ANNUAL / SECONDS_PER_YEAR * 3600,
    ],
})

with tab_rate:
    st.subheader("Kill Rate: Animals Killed Per Unit Time")

    st.markdown(
        "Abstract annual totals are hard to grasp. "
        "Breaking them into per-second rates makes the scale visceral."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "US land animals / second",
            "{:,.0f}".format(LAND_US_ANNUAL / SECONDS_PER_YEAR),
        )
        st.metric(
            "Global wild-caught fish / second",
            "{:,.0f}".format(WILD_FISH_ANNUAL / SECONDS_PER_YEAR),
        )
    with col2:
        st.metric(
            "Global farmed fish / second",
            "{:,.0f}".format(FARMED_FISH_ANNUAL / SECONDS_PER_YEAR),
        )
        st.metric(
            "Global farmed crustaceans / second",
            "{:,.0f}".format(FARMED_CRUST_ANNUAL / SECONDS_PER_YEAR),
        )
    with col3:
        st.metric(
            "All aquatic (global) / second",
            "{:,.0f}".format(AQUATIC_TOTAL_ANNUAL / SECONDS_PER_YEAR),
            help="Wild-caught fish + farmed fish + farmed crustaceans + bycatch",
        )
        st.metric(
            "Combined (US land + global aquatic) / second",
            "{:,.0f}".format(ALL_TOTAL_ANNUAL / SECONDS_PER_YEAR),
        )

    st.markdown("---")

    fig_rate = px.bar(
        rate_df,
        x="Category",
        y="Per second",
        color="Category",
        title="Animals Killed Per Second (central estimates)",
        color_discrete_sequence=px.colors.qualitative.Bold,
        text="Per second",
    )
    fig_rate.update_traces(texttemplate="%{text:,.0f}/s", textposition="outside")
    fig_rate.update_layout(showlegend=False, yaxis_title="Individuals per second")
    st.plotly_chart(fig_rate, use_container_width=True)

    rate_display = rate_df.copy()
    rate_display["Per second"] = rate_display["Per second"].map("{:,.0f}".format)
    rate_display["Per minute"] = rate_display["Per minute"].map("{:,.0f}".format)
    rate_display["Per hour"]   = rate_display["Per hour"].map("{:,.0f}".format)
    st.dataframe(rate_display, hide_index=True)

    st.caption(
        "Rates derived from annual totals / 31,557,600 seconds per year. "
        "Sources: USDA NASS lstk0325.pdf | Mood et al. 2024 doi:10.1017/awf.2024.7 | "
        "Mood et al. 2023 doi:10.1017/awf.2023.4 | fishcount.org.uk | FAO SOFIA 2022 doi:10.4060/cc0461en"
    )

st.markdown("---")
st.markdown(
    "Dashboard by [garytheveganbot](https://github.com/garytheveganbot) | "
    "Data: USDA NASS, NOAA Fisheries, Animal Welfare journal (Cambridge), fishcount.org.uk, FAO"
)
