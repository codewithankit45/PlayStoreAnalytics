# ============================================================
# GOOGLE PLAY STORE DATA ANALYTICS
# FINAL STREAMLIT DASHBOARD - TASK 1 TO TASK 6
# ============================================================

import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
import streamlit as st

warnings.filterwarnings("ignore")

# ============================================================
# CONFIGURATION
# ============================================================

APP_DATA_FILE = "Play Store Data.csv"
REVIEWS_DATA_FILE = "User Reviews.csv"

# FINAL SUBMISSION:
# False = actual time restrictions are applied.
# True = only for temporary testing outside the time window.
DEBUG_MODE = False

IST = pytz.timezone("Asia/Kolkata")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


# ============================================================
# TIME FUNCTIONS
# ============================================================

def current_ist():
    return datetime.now(IST)


def is_time_between(start_hour, end_hour):
    """
    Start inclusive, end exclusive.
    Example:
    17,19 => 5 PM <= time < 7 PM
    """
    hour = current_ist().hour
    return start_hour <= hour < end_hour


def chart_not_available(start_hour, end_hour):
    current_time = current_ist().strftime("%I:%M %p")

    st.warning(
        "🔒 This chart is currently hidden because the current "
        "time is outside its allowed time window."
    )

    st.info(
        f"⏰ Available time: {start_hour}:00 PM IST to "
        f"{end_hour}:00 PM IST\n\n"
        f"🕐 Current IST time: {current_time}"
    )

    st.caption(
        "Please open this task during its assigned time window "
        "to view the chart."
    )


# ============================================================
# COMMON PLOTLY STYLE
# ============================================================

def apply_chart_theme(fig):
    """
    Keep dashboard Plotly charts visually close to the
    Jupyter Plotly charts while improving Streamlit visibility.
    """

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            size=13,
            color="#111111"
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#444444",
            font=dict(
                family="Arial, sans-serif",
                size=13,
                color="#111111"
            ),
            align="left"
        )
    )

    fig.update_xaxes(
        color="#111111",
        title_font=dict(
            color="#111111",
            size=14
        ),
        tickfont=dict(
            color="#111111",
            size=12
        ),
        showgrid=True,
        gridcolor="lightgray"
    )

    fig.update_yaxes(
        color="#111111",
        title_font=dict(
            color="#111111",
            size=14
        ),
        tickfont=dict(
            color="#111111",
            size=12
        ),
        showgrid=True,
        gridcolor="lightgray"
    )

    return fig


def show_chart(fig):
    """
    Render chart with enough height so Plotly remains readable
    inside Streamlit.
    """
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True
        }
    )


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_and_prepare_data():

    apps_df = pd.read_csv(APP_DATA_FILE)
    reviews_df = pd.read_csv(REVIEWS_DATA_FILE)

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    apps_df = apps_df.drop_duplicates(
        subset="App"
    )

    reviews_df = reviews_df.drop_duplicates()

    # --------------------------------------------------------
    # Installs
    # --------------------------------------------------------

    apps_df["Installs"] = (
        apps_df["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    apps_df["Installs"] = pd.to_numeric(
        apps_df["Installs"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Reviews
    # --------------------------------------------------------

    apps_df["Reviews"] = pd.to_numeric(
        apps_df["Reviews"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Rating
    # --------------------------------------------------------

    apps_df["Rating"] = pd.to_numeric(
        apps_df["Rating"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Size
    # --------------------------------------------------------

    def clean_size(size):

        if pd.isna(size):
            return np.nan

        size = str(size)

        if "M" in size:
            return float(
                size.replace("M", "")
            )

        if "k" in size:
            return float(
                size.replace("k", "")
            ) / 1024

        return np.nan

    apps_df["Size_MB"] = (
        apps_df["Size"]
        .apply(clean_size)
    )

    # --------------------------------------------------------
    # Price
    # --------------------------------------------------------

    apps_df["Price"] = (
        apps_df["Price"]
        .astype(str)
        .str.replace("$", "", regex=False)
    )

    apps_df["Price"] = pd.to_numeric(
        apps_df["Price"],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    apps_df["Last Updated"] = pd.to_datetime(
        apps_df["Last Updated"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Android Version
    # --------------------------------------------------------

    apps_df["Android Version"] = (
        apps_df["Android Ver"]
        .astype(str)
        .str.extract(
            r"(\d+\.\d+)",
            expand=False
        )
    )

    apps_df["Android Version"] = pd.to_numeric(
        apps_df["Android Version"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Month
    # --------------------------------------------------------

    apps_df["Month"] = (
        apps_df["Last Updated"]
        .dt.month_name()
    )

    # --------------------------------------------------------
    # Merge
    # --------------------------------------------------------

    merged_df = pd.merge(
        apps_df,
        reviews_df,
        on="App",
        how="left"
    )

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    merged_df["Revenue"] = (
        merged_df["Price"] *
        merged_df["Installs"]
    )

    return merged_df


# ============================================================
# TASK 1
# BUBBLE CHART
# 5 PM - 7 PM IST
# ============================================================

def task1(merged_df):

    st.header("🫧 Task 1 — Bubble Chart")

    st.caption(
        "Required time window: 5 PM – 7 PM IST"
    )

    if not (
        DEBUG_MODE or
        is_time_between(17, 19)
    ):
        chart_not_available(17, 19)
        return

    task1_categories = [
        "GAME",
        "BEAUTY",
        "BUSINESS",
        "COMICS",
        "COMMUNICATION",
        "DATING",
        "ENTERTAINMENT",
        "SOCIAL",
        "EVENTS"
    ]

    task1_df = merged_df.copy()

    task1_df["Category"] = (
        task1_df["Category"]
        .astype(str)
        .str.upper()
    )

    # --------------------------------------------------------
    # EXACT NOTEBOOK FILTERS
    # --------------------------------------------------------

    task1_df = task1_df[
        (task1_df["Rating"] > 3.5) &
        (task1_df["Reviews"] > 500) &
        (task1_df["Installs"] > 50000) &
        (task1_df["Sentiment_Subjectivity"] > 0.5) &
        (
            ~task1_df["App"]
            .astype(str)
            .str.contains(
                "S",
                case=False,
                na=False
            )
        ) &
        (
            task1_df["Category"]
            .isin(task1_categories)
        )
    ].copy()

    task1_df = task1_df.dropna(
        subset=[
            "Size_MB",
            "Rating",
            "Installs"
        ]
    )

    # --------------------------------------------------------
    # TRANSLATION
    # --------------------------------------------------------

    display_df = task1_df.copy()

    display_df["Category_Display"] = (
        display_df["Category"]
        .replace({
            "BEAUTY": "सौंदर्य",
            "BUSINESS": "வணிகம்",
            "DATING": "Partnersuche"
        })
    )

    # --------------------------------------------------------
    # BUBBLE CHART
    # --------------------------------------------------------

    fig1 = px.scatter(
        display_df,
        x="Size_MB",
        y="Rating",
        size="Installs",
        color="Category_Display",
        hover_name="App",

        hover_data={
            "Size_MB": ":.1f",
            "Rating": ":.1f",
            "Installs": ":,",
            "Reviews": ":,",
            "Category_Display": True
        },

        size_max=40,

        color_discrete_map={
            "GAME": "pink"
        }
    )

    fig1.update_traces(
        marker=dict(
            opacity=0.72,
            line=dict(
                width=0.7,
                color="white"
            )
        )
    )

    fig1.update_layout(
        title={
            "text":
            "Task 1: Relationship Between App Size and Average Rating",
            "x": 0.5,
            "xanchor": "center"
        },

        xaxis_title="App Size (MB)",
        yaxis_title="Average Rating",

        legend_title="App Category",

        height=700,

        margin=dict(
            l=80,
            r=180,
            t=100,
            b=90
        )
    )

    apply_chart_theme(fig1)

    show_chart(fig1)


# ============================================================
# TASK 2
# CHOROPLETH MAP
# 6 PM - 8 PM IST
# ============================================================

def task2(merged_df):

    st.header("🌍 Task 2 — Choropleth Map")

    st.caption(
        "Required time window: 6 PM – 8 PM IST"
    )

    if not (
        DEBUG_MODE or
        is_time_between(18, 20)
    ):
        chart_not_available(18, 20)
        return

    task2_df = merged_df.copy()

    # --------------------------------------------------------
    # EXACT NOTEBOOK FILTER
    # --------------------------------------------------------

    task2_df = task2_df[
        ~task2_df["Category"]
        .astype(str)
        .str.upper()
        .str.startswith(
            ("A", "C", "G", "S"),
            na=False
        )
    ].copy()

    task2_df = (
        task2_df
        .groupby(
            "Category",
            as_index=False
        )["Installs"]
        .sum()
        .sort_values(
            "Installs",
            ascending=False
        )
        .head(5)
    )

    task2_df["Highlight"] = (
        task2_df["Installs"] > 1_000_000
    )

    # --------------------------------------------------------
    # NOTEBOOK-IDENTICAL CHOROPLETH
    #
    # IMPORTANT:
    # Category is NOT geographic country data.
    # Therefore Plotly will show a blank world map.
    # This is expected and matches the notebook.
    # --------------------------------------------------------

    fig2 = px.choropleth(
        task2_df,
        locations="Category",
        locationmode="country names",
        color="Installs",
        hover_name="Category",
        hover_data={
            "Installs": ":,"
        }
    )

    for trace in fig2.data:
        trace.marker.line.width = 1

    fig2.update_layout(
        title={
            "text":
            "Task 2: Global Installs by Category",
            "x": 0.5,
            "xanchor": "center"
        },

        height=700,

        margin=dict(
            t=100,
            l=80,
            r=80,
            b=80
        )
    )

    apply_chart_theme(fig2)

    show_chart(fig2)

    st.info(
        "Note: The Play Store dataset contains app categories, "
        "not geographic country data. Therefore category names "
        "cannot shade real countries. The blank world map "
        "matches the notebook implementation."
    )


# ============================================================
# TASK 3
# TIME SERIES
# 6 PM - 9 PM IST
# ============================================================

def task3(merged_df):

    st.header("📈 Task 3 — Monthly Install Trend by Category")

    st.caption(
        "Required time window: 6 PM – 9 PM IST"
    )

    if not (
        DEBUG_MODE or
        is_time_between(18, 21)
    ):
        chart_not_available(18, 21)
        return

    # ========================================================
    # DATA COPY
    # ========================================================

    task3_df = merged_df.copy()

    # ========================================================
    # EXACT NOTEBOOK FILTERS
    # ========================================================

    task3_df = task3_df[
        (task3_df["Reviews"] > 500) &
        (
            ~task3_df["App"]
            .astype(str)
            .str.upper()
            .str.startswith(
                ("X", "Y", "Z"),
                na=False
            )
        ) &
        (
            ~task3_df["App"]
            .astype(str)
            .str.contains(
                "S",
                case=False,
                na=False
            )
        ) &
        (
            task3_df["Category"]
            .astype(str)
            .str.upper()
            .str.startswith(
                ("E", "C", "B"),
                na=False
            )
        )
    ].copy()

    # ========================================================
    # CATEGORY TRANSLATION
    # ========================================================

    translation = {
        "BEAUTY": "सौंदर्य",
        "BUSINESS": "வணிகம்",
        "DATING": "Partnersuche"
    }

    task3_df["Category_Display"] = (
        task3_df["Category"]
        .astype(str)
        .str.upper()
        .replace(translation)
    )

    # ========================================================
    # MONTH
    # ========================================================

    task3_df["Month"] = (
        pd.to_datetime(
            task3_df["Last Updated"],
            errors="coerce"
        )
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # ========================================================
    # MONTHLY TOTAL INSTALLS
    # ========================================================

    monthly_df = (
        task3_df
        .groupby(
            [
                "Month",
                "Category_Display"
            ],
            as_index=False
        )["Installs"]
        .sum()
        .sort_values(
            [
                "Category_Display",
                "Month"
            ]
        )
        .reset_index(drop=True)
    )

    # ========================================================
    # MOM GROWTH
    # ========================================================

    monthly_df["Growth"] = (
        monthly_df
        .groupby("Category_Display")[
            "Installs"
        ]
        .pct_change()
    )

    # ========================================================
    # HIGH GROWTH > 20%
    # ========================================================

    monthly_df["High_Growth"] = (
        monthly_df["Growth"] > 0.20
    )

    # ========================================================
    # CREATE FIGURE
    # ========================================================

    fig3 = go.Figure()

    # EXACT NOTEBOOK COLORS
    colors = {
        "COMMUNICATION": "royalblue",
        "COMICS": "orange",
        "EDUCATION": "green",
        "ENTERTAINMENT": "red",
        "EVENTS": "purple",
        "BOOKS_AND_REFERENCE": "brown",
        "வணிகம்": "black",
        "सौंदर्य": "deeppink"
    }

    # ========================================================
    # CATEGORY-WISE LINE
    # ========================================================

    for cat in monthly_df[
        "Category_Display"
    ].unique():

        temp = (
            monthly_df[
                monthly_df["Category_Display"] == cat
            ]
            .sort_values("Month")
            .reset_index(drop=True)
        )

        # Main category line
        fig3.add_trace(
            go.Scatter(
                x=temp["Month"],
                y=temp["Installs"],

                mode="lines+markers",

                name=cat,

                line=dict(
                    width=2,
                    color=colors.get(
                        cat,
                        "gray"
                    )
                ),

                marker=dict(
                    size=6
                ),

                hovertemplate=
                    "<b>Category:</b> %{fullData.name}<br>" +
                    "<b>Month:</b> %{x|%b %Y}<br>" +
                    "<b>Total Installs:</b> %{y:,.0f}<br>" +
                    "<extra></extra>"
            )
        )

        # ====================================================
        # HIGH GROWTH DIAMOND
        # ====================================================

        growth_points = temp[
            temp["High_Growth"] == True
        ]

        if not growth_points.empty:

            fig3.add_trace(
                go.Scatter(
                    x=growth_points["Month"],
                    y=growth_points["Installs"],

                    mode="markers",

                    marker=dict(
                        size=14,
                        color="limegreen",
                        symbol="diamond"
                    ),

                    name=f"{cat} >20% Growth",

                    showlegend=False,

                    hovertemplate=
                        "<b>High Growth</b><br>" +
                        "Category: " + str(cat) + "<br>" +
                        "Month: %{x|%b %Y}<br>" +
                        "Installs: %{y:,.0f}<br>" +
                        "Growth: >20%<br>" +
                        "<extra></extra>"
                )
            )

    # ========================================================
    # HIGHLIGHT MONTHS
    # ========================================================

    high_growth_months = (
        monthly_df.loc[
            monthly_df["High_Growth"] == True,
            "Month"
        ]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    for month in high_growth_months:

        fig3.add_vrect(
            x0=month - pd.Timedelta(days=10),
            x1=month + pd.Timedelta(days=10),

            fillcolor="lightgreen",
            opacity=0.20,

            layer="below",
            line_width=0
        )

    # ========================================================
    # FINAL LAYOUT — NOTEBOOK MATCH
    # ========================================================

    fig3.update_layout(

        title=dict(
            text="Task 3 : Monthly Install Trend by Category",
            x=0.5,
            xanchor="center"
        ),

        xaxis=dict(
            title="Month",
            type="date",
            showgrid=True,
            gridcolor="lightgray"
        ),

        yaxis=dict(
            title="Total Installs",
            type="log",
            showgrid=True,
            gridcolor="lightgray"
        ),

        template="plotly_white",

        hovermode="x unified",

        height=700,

        legend=dict(
            title="Category",
            orientation="v",

            x=1.1,
            xanchor="center",

            y=1,
            yanchor="top",

            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1,

            font=dict(
                size=10
            )
        ),

        margin=dict(
            l=90,
            r=40,
            t=90,
            b=150
        )
    )

    fig3.update_xaxes(
        showgrid=True,
        gridcolor="lightgray"
    )

    fig3.update_yaxes(
        showgrid=True,
        gridcolor="lightgray"
    )

    apply_chart_theme(fig3)

    show_chart(fig3)


# ============================================================
# TASK 4
# STACKED AREA CHART
# 4 PM - 6 PM IST
# ============================================================

def task4(merged_df):

    st.header("📊 Task 4 — Stacked Area Chart")

    st.caption(
        "Required time window: 4 PM – 6 PM IST"
    )

    if not (
        DEBUG_MODE or
        is_time_between(16, 18)
    ):
        chart_not_available(16, 18)
        return

    task4_df = merged_df.copy()

    # --------------------------------------------------------
    # EXACT NOTEBOOK FILTERS
    # --------------------------------------------------------

    task4_df = task4_df[
        (task4_df["Rating"] >= 4.2) &
        (task4_df["Reviews"] > 1000) &
        (
            task4_df["Size_MB"]
            .between(20, 80)
        )
    ].copy()

    task4_df = task4_df[
        ~task4_df["App"]
        .astype(str)
        .str.contains(
            r"\d",
            regex=True,
            na=False
        )
    ].copy()

    task4_df = task4_df[
        task4_df["Category"]
        .astype(str)
        .str.upper()
        .str.startswith(
            ("T", "P"),
            na=False
        )
    ].copy()

    # --------------------------------------------------------
    # CATEGORY TRANSLATION
    # --------------------------------------------------------

    translation = {
        "TRAVEL_AND_LOCAL": "Voyage et Local",
        "PRODUCTIVITY": "Productividad",
        "PHOTOGRAPHY": "写真"
    }

    task4_df["Category_Display"] = (
        task4_df["Category"]
        .astype(str)
        .str.upper()
        .replace(translation)
    )

    # --------------------------------------------------------
    # MONTH
    # --------------------------------------------------------

    task4_df["Month"] = (
        pd.to_datetime(
            task4_df["Last Updated"]
        )
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    task4_df = task4_df.dropna(
        subset=[
            "App",
            "Category",
            "Rating",
            "Reviews",
            "Size_MB",
            "Installs",
            "Month"
        ]
    )

    # --------------------------------------------------------
    # MONTHLY DATA
    # --------------------------------------------------------

    monthly4_df = (
        task4_df
        .groupby(
            [
                "Month",
                "Category_Display"
            ],
            as_index=False
        )
        .agg(
            Monthly_Installs=(
                "Installs",
                "sum"
            )
        )
        .sort_values(
            [
                "Category_Display",
                "Month"
            ]
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # CUMULATIVE INSTALLS
    # --------------------------------------------------------

    monthly4_df[
        "Cumulative_Installs"
    ] = (
        monthly4_df
        .groupby("Category_Display")[
            "Monthly_Installs"
        ]
        .cumsum()
    )

    # --------------------------------------------------------
    # MOM GROWTH
    # --------------------------------------------------------

    monthly4_df["Growth"] = (
        monthly4_df
        .groupby("Category_Display")[
            "Monthly_Installs"
        ]
        .pct_change()
    )

    monthly4_df["High_Growth"] = (
        monthly4_df["Growth"] > 0.25
    )

    # --------------------------------------------------------
    # STACKED AREA
    # --------------------------------------------------------

    fig4 = go.Figure()

    for cat in monthly4_df[
        "Category_Display"
    ].unique():

        temp = (
            monthly4_df[
                monthly4_df["Category_Display"] == cat
            ]
            .sort_values("Month")
        )

        fig4.add_trace(
            go.Scatter(
                x=temp["Month"],
                y=temp["Cumulative_Installs"],

                mode="lines",

                stackgroup="one",

                name=cat,

                line=dict(
                    width=2
                ),

                hovertemplate=
                "<b>Category:</b> %{fullData.name}<br>" +
                "<b>Month:</b> %{x|%b %Y}<br>" +
                "<b>Cumulative Installs:</b> %{y:,.0f}" +
                "<extra></extra>"
            )
        )

    # --------------------------------------------------------
    # HIGHLIGHT >25% MOM GROWTH
    # --------------------------------------------------------

    high_growth_months = (
        monthly4_df.loc[
            monthly4_df["High_Growth"],
            "Month"
        ]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    for month in high_growth_months:

        fig4.add_vrect(
            x0=month,
            x1=month + pd.DateOffset(
                months=1
            ),

            fillcolor="red",
            opacity=0.12,

            layer="below",

            line_width=0
        )

    fig4.update_layout(
        title={
            "text":
            "Task 4 : Stacked Area Chart - Cumulative Installs",
            "x": 0.5,
            "xanchor": "center"
        },

        xaxis=dict(
            title="Month",
            showgrid=True,
            gridcolor="lightgray"
        ),

        yaxis=dict(
            title="Cumulative Installs",
            showgrid=True,
            gridcolor="lightgray"
        ),

        hovermode="x unified",

        height=700,

        legend=dict(
            title="Category",
            orientation="v",
            x=1.02,
            xanchor="left",
            y=1,
            yanchor="top",
            font=dict(size=10),
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        ),

        margin=dict(
            l=90,
            r=190,
            t=100,
            b=120
        )
    )

    apply_chart_theme(fig4)

    show_chart(fig4)


# ============================================================
# TASK 5
# GROUPED BAR CHART
# 3 PM - 5 PM IST
# ============================================================

def task5(merged_df):

    st.header("📊 Task 5 — Grouped Bar Chart")

    st.caption(
        "Required time window: 3 PM – 5 PM IST"
    )

    if not (
        DEBUG_MODE or
        is_time_between(15, 17)
    ):
        chart_not_available(15, 17)
        return

    task5_df = merged_df.copy()

    # --------------------------------------------------------
    # EXACT NOTEBOOK FILTERS
    # --------------------------------------------------------

    task5_df = task5_df[
        (task5_df["Rating"] >= 4.0) &
        (task5_df["Size_MB"] >= 10) &
        (task5_df["Month"] == "January")
    ].copy()

    task5_df = task5_df.dropna(
        subset=[
            "Category",
            "Rating",
            "Reviews",
            "Installs"
        ]
    )

    # --------------------------------------------------------
    # GROUP
    # --------------------------------------------------------

    task5_df = (
        task5_df
        .groupby("Category")
        .agg(
            Avg_Rating=(
                "Rating",
                "mean"
            ),

            Total_Reviews=(
                "Reviews",
                "sum"
            ),

            Total_Installs=(
                "Installs",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "Total_Installs",
            ascending=False
        )
        .head(10)
    )

    task5_df[
        "Total_Reviews_M"
    ] = (
        task5_df[
            "Total_Reviews"
        ] / 1_000_000
    )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig5 = go.Figure()

    fig5.add_trace(
        go.Bar(
            x=task5_df["Category"],
            y=task5_df["Avg_Rating"],

            name="Average Rating",

            text=(
                task5_df["Avg_Rating"]
                .round(2)
            ),

            textposition="outside",

            hovertemplate=
            "<b>%{x}</b><br>" +
            "Average Rating : %{y:.2f}" +
            "<extra></extra>"
        )
    )

    fig5.add_trace(
        go.Bar(
            x=task5_df["Category"],
            y=task5_df[
                "Total_Reviews_M"
            ],

            name="Total Reviews (Million)",

            text=(
                task5_df[
                    "Total_Reviews_M"
                ]
                .round(2)
            ),

            textposition="outside",

            hovertemplate=
            "<b>%{x}</b><br>" +
            "Total Reviews : %{y:,.2f} Million" +
            "<extra></extra>"
        )
    )

    fig5.update_layout(
        title={
            "text":
            "Task 5 : Average Rating vs Total Reviews",

            "x": 0.5,

            "y": 0.98,

            "xanchor": "center",

            "yanchor": "top"
        },

        barmode="group",

        xaxis_title="Category",

        yaxis_title=(
            "Average Rating / "
            "Reviews (Million)"
        ),

        height=700,

        hovermode="x unified",

        legend=dict(
            title="Metrics",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.12
        ),

        margin=dict(
            l=80,
            r=60,
            t=130,
            b=160
        )
    )

    fig5.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        tickangle=-35,
        automargin=True
    )

    fig5.update_yaxes(
        showgrid=True,
        gridcolor="lightgray"
    )

    apply_chart_theme(fig5)

    show_chart(fig5)


# ============================================================
# TASK 6
# DUAL AXIS CHART
# 1 PM - 2 PM IST
# ============================================================

def task6(merged_df):

    st.header(
        "📉 Task 6 — Average Installs vs Average Revenue"
    )

    st.caption(
        "Required time window: 1 PM – 2 PM IST"
    )

    if not (
        DEBUG_MODE or
        is_time_between(13, 14)
    ):
        chart_not_available(13, 14)
        return

    task6_df = merged_df.copy()

    # --------------------------------------------------------
    # APP NAME LENGTH
    # --------------------------------------------------------

    task6_df[
        "App_Name_Length"
    ] = (
        task6_df["App"]
        .astype(str)
        .str.len()
    )

    # --------------------------------------------------------
    # FREE / PAID
    # --------------------------------------------------------

    task6_df["App_Type"] = np.where(
        task6_df["Price"] > 0,
        "Paid",
        "Free"
    )

    # --------------------------------------------------------
    # EXACT NOTEBOOK FILTERS
    # --------------------------------------------------------

    task6_df = task6_df[
        (task6_df["Installs"] >= 10000) &
        (task6_df["Android Version"] > 4.0) &
        (task6_df["Size_MB"] > 15) &
        (
            task6_df["Content Rating"]
            == "Everyone"
        ) &
        (
            task6_df["App_Name_Length"]
            <= 30
        )
    ].copy()

    # --------------------------------------------------------
    # PAID REVENUE FILTER
    # --------------------------------------------------------

    task6_df = task6_df[
        (
            task6_df["App_Type"]
            == "Free"
        )
        |
        (
            (
                task6_df["App_Type"]
                == "Paid"
            )
            &
            (
                task6_df["Revenue"]
                >= 10000
            )
        )
    ].copy()

    # --------------------------------------------------------
    # TOP 3 CATEGORIES
    # --------------------------------------------------------

    top_3_categories = (
        task6_df
        .groupby("Category")[
            "Installs"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(3)
        .index
        .tolist()
    )

    task6_top3_df = task6_df[
        task6_df["Category"]
        .isin(top_3_categories)
    ].copy()

    # --------------------------------------------------------
    # AGGREGATION
    # --------------------------------------------------------

    task6_chart_df = (
        task6_top3_df
        .groupby(
            [
                "Category",
                "App_Type"
            ]
        )
        .agg(
            Average_Installs=(
                "Installs",
                "mean"
            ),

            Average_Revenue=(
                "Revenue",
                "mean"
            )
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # KEEP TOP 3 ORDER
    # --------------------------------------------------------

    task6_chart_df[
        "Category"
    ] = pd.Categorical(
        task6_chart_df["Category"],
        categories=top_3_categories,
        ordered=True
    )

    task6_chart_df = (
        task6_chart_df
        .sort_values(
            [
                "Category",
                "App_Type"
            ]
        )
    )

    # --------------------------------------------------------
    # SPLIT FREE / PAID
    # --------------------------------------------------------

    free_df = task6_chart_df[
        task6_chart_df["App_Type"]
        == "Free"
    ].copy()

    paid_df = task6_chart_df[
        task6_chart_df["App_Type"]
        == "Paid"
    ].copy()

    # --------------------------------------------------------
    # FIGURE
    # --------------------------------------------------------

        # ========================================================
    # CREATE FIGURE
    # ========================================================

    fig6 = go.Figure()

    # ========================================================
    # FREE : AVERAGE INSTALLS
    # ========================================================

    fig6.add_trace(
        go.Bar(
            x=free_df["Category"],
            y=free_df["Average_Installs"],

            name="Free - Avg Installs",

            offsetgroup="Free",

            hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Type:</b> Free<br>" +
                "<b>Average Installs:</b> %{y:,.0f}" +
                "<extra></extra>"
        )
    )

    # ========================================================
    # PAID : AVERAGE INSTALLS
    # ========================================================

    fig6.add_trace(
        go.Bar(
            x=paid_df["Category"],
            y=paid_df["Average_Installs"],

            name="Paid - Avg Installs",

            offsetgroup="Paid",

            hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Type:</b> Paid<br>" +
                "<b>Average Installs:</b> %{y:,.0f}" +
                "<extra></extra>"
        )
    )

    # ========================================================
    # FREE : AVERAGE REVENUE
    # ========================================================

    fig6.add_trace(
        go.Scatter(
            x=free_df["Category"],
            y=free_df["Average_Revenue"],

            name="Free - Avg Revenue",

            mode="lines+markers",

            yaxis="y2",

            hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Type:</b> Free<br>" +
                "<b>Average Revenue:</b> $%{y:,.2f}" +
                "<extra></extra>"
        )
    )

    # ========================================================
    # PAID : AVERAGE REVENUE
    # ========================================================

    fig6.add_trace(
        go.Scatter(
            x=paid_df["Category"],
            y=paid_df["Average_Revenue"],

            name="Paid - Avg Revenue",

            mode="lines+markers",

            yaxis="y2",

            hovertemplate=
                "<b>Category:</b> %{x}<br>" +
                "<b>Type:</b> Paid<br>" +
                "<b>Average Revenue:</b> $%{y:,.2f}" +
                "<extra></extra>"
        )
    )

    # ========================================================
    # FINAL LAYOUT — NOTEBOOK MATCH
    # ========================================================

    fig6.update_layout(

        title=dict(
            text="Task 6 : Average Installs vs Average Revenue - Free vs Paid",
            x=0.5,
            xanchor="center"
        ),

        xaxis=dict(
            title="Top 3 App Categories",

            categoryorder="array",

            categoryarray=top_3_categories,

            tickangle=0,

            automargin=True
        ),

        yaxis=dict(
            title="Average Installs",

            showgrid=True,
            gridcolor="lightgray",

            automargin=True
        ),

        yaxis2=dict(
            title="Average Revenue ($)",

            overlaying="y",
            side="right",

            showgrid=False,

            automargin=True
        ),

        barmode="group",

        template="plotly_white",

        width=1200,
        height=700,

        hovermode="x unified",

        legend=dict(
            title="Metrics",

            orientation="h",

            x=0.5,
            xanchor="center",

            y=1.10
        ),

        margin=dict(
            t=140,
            r=180,
            l=120,
            b=120
        )
    )

    fig6.update_xaxes(
        showgrid=True,
        gridcolor="lightgray"
    )

    fig6.update_yaxes(
        showgrid=True,
        gridcolor="lightgray"
    )

    apply_chart_theme(fig6)

    show_chart(fig6)


# ============================================================
# MAIN
# ============================================================

def main():

    load_css()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="dashboard-header">
            <h1>📊 Google Play Store Data Analytics</h1>
            <p>
                Interactive Internship Dashboard —
                Task 1 to Task 6
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.markdown(
        "## 📌 Dashboard Navigation"
    )

    st.sidebar.markdown(
        f"**Current IST:** "
        f"{current_ist().strftime('%I:%M %p')}"
    )

    st.sidebar.markdown(
        f"**Debug Mode:** "
        f"{'ON' if DEBUG_MODE else 'OFF'}"
    )

    st.sidebar.markdown("---")

    task = st.sidebar.selectbox(
        "Select Task",

        [
            "Task 1 - Bubble Chart",
            "Task 2 - Choropleth Map",
            "Task 3 - Time Series",
            "Task 4 - Stacked Area Chart",
            "Task 5 - Grouped Bar Chart",
            "Task 6 - Dual Axis Chart"
        ]
    )

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    try:

        merged_df = load_and_prepare_data()

    except Exception as e:

        st.error(
            "❌ Data loading failed."
        )

        st.exception(e)

        st.stop()

    st.success(
        f"Dataset loaded successfully — "
        f"{len(merged_df):,} rows"
    )

    # --------------------------------------------------------
    # TASK DESCRIPTION
    # --------------------------------------------------------

    task_info = {

        "Task 1 - Bubble Chart": (
            "Task 1: App Size vs Average Rating",
            "Explore the relationship between app size, "
            "average rating, and installs."
        ),

        "Task 2 - Choropleth Map": (
            "Task 2: Global Installs by Category",
            "Visualize global app installs across the "
            "top application categories."
        ),

        "Task 3 - Time Series": (
            "Task 3: Monthly Install Trend",
            "Analyze the trend of total installs over time "
            "by app category."
        ),

        "Task 4 - Stacked Area Chart": (
            "Task 4: Cumulative Installs by Category",
            "Visualize cumulative installs over time "
            "for each category."
        ),

        "Task 5 - Grouped Bar Chart": (
            "Task 5: Top 10 Categories Analysis",
            "Compare average rating and total reviews "
            "across the top categories."
        ),

        "Task 6 - Dual Axis Chart": (
            "Task 6: Average Installs vs Average Revenue",
            "Compare average installs and average revenue "
            "between free and paid apps."
        )
    }

    title, description = task_info[task]

    st.markdown(
        f"""
        <div class="task-header">
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # RUN ONLY SELECTED TASK
    # --------------------------------------------------------

    if task == "Task 1 - Bubble Chart":
        task1(merged_df)

    elif task == "Task 2 - Choropleth Map":
        task2(merged_df)

    elif task == "Task 3 - Time Series":
        task3(merged_df)

    elif task == "Task 4 - Stacked Area Chart":
        task4(merged_df)

    elif task == "Task 5 - Grouped Bar Chart":
        task5(merged_df)

    elif task == "Task 6 - Dual Axis Chart":
        task6(merged_df)


if __name__ == "__main__":
    main()