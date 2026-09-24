import re
import requests
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SAI University | Research Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "https://sai-publications-dashboard.vercel.app/api/publications"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main {
        background-color: #f7f8fa;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .dashboard-title {
        font-size: 2.2rem;
        font-weight: 750;
        color: #172033;
        margin-bottom: 0.1rem;
    }

    .dashboard-subtitle {
        color: #697386;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #172033;
        margin-top: 1.2rem;
        margin-bottom: 0.7rem;
    }

    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        border: 1px solid #e8ebf0;
        min-height: 115px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .kpi-label {
        color: #697386;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .kpi-value {
        color: #172033;
        font-size: 1.8rem;
        font-weight: 750;
        margin-top: 0.35rem;
    }

    .insight-card {
        background: white;
        border-left: 4px solid #4f46e5;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        color: #303746;
    }

    .source-tag {
        display: inline-block;
        padding: 0.25rem 0.55rem;
        background: #eef2ff;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #4338ca;
        margin-right: 0.3rem;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# API
# ============================================================

@st.cache_data(ttl=3600)
def fetch_data():

    response = requests.get(
        API_URL,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if isinstance(result, dict):
        records = result.get("data", [])
    elif isinstance(result, list):
        records = result
    else:
        records = []

    return pd.DataFrame(records)


# ============================================================
# HELPERS
# ============================================================

def find_column(df, possible_names):

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in possible_names:

        key = name.strip().lower()

        if key in normalized:
            return normalized[key]

    # Partial matching
    for col in df.columns:

        col_lower = str(col).lower()

        for name in possible_names:

            if name.lower() in col_lower:
                return col

    return None


def clean_value(value):

    if pd.isna(value):
        return "Not Available"

    value = str(value).strip()

    if not value:
        return "Not Available"

    return value


def split_people(value):

    """
    Converts an author field containing multiple names
    into individual names.
    """

    if pd.isna(value):
        return []

    value = str(value).strip()

    if not value:
        return []

    # Common separators
    people = re.split(
        r"\s*(?:;|\||\n)\s*",
        value
    )

    return [
        p.strip()
        for p in people
        if p.strip()
    ]


def extract_sdg(value):

    if pd.isna(value):
        return []

    value = str(value)

    # Match SDG 1, SDG 2, etc.
    matches = re.findall(
        r"(?:SDG\s*)?([1-9]|1[0-7])",
        value,
        flags=re.IGNORECASE
    )

    return sorted(
        set(f"SDG {x}" for x in matches),
        key=lambda x: int(x.split()[-1])
    )


def normalize_indexing(value):

    if pd.isna(value):
        return "Not Available"

    text = str(value).strip().lower()

    if "scopus" in text and ("web" in text or "wos" in text):
        return "Scopus + WoS"

    if "scopus" in text:
        return "Scopus"

    if "web of science" in text or "wos" in text:
        return "Web of Science"

    if text in ["", "nan", "none", "null"]:
        return "Not Available"

    return str(value).strip()


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = fetch_data()

except Exception as e:

    st.error(f"Unable to load publication data: {e}")
    st.stop()


if df.empty:

    st.error("The API returned no publication records.")
    st.stop()


# ============================================================
# COLUMN DETECTION
# ============================================================

YEAR_COL = find_column(
    df,
    [
        "Year",
        "Publication Year",
        "year"
    ]
)

TITLE_COL = find_column(
    df,
    [
        "Title",
        "Publication Title",
        "Article Title"
    ]
)

SCHOOL_COL = find_column(
    df,
    [
        "School",
        "School Name"
    ]
)

AUTHOR_COL = find_column(
    df,
    [
        "SaiU Authors",
        "SAIU Authors",
        "Faculty member",
        "Faculty Member",
        "Authors"
    ]
)

ALL_AUTHOR_COL = find_column(
    df,
    [
        "Authors",
        "Author"
    ]
)

DOC_TYPE_COL = find_column(
    df,
    [
        "Document Type",
        "Publication Type",
        "Type"
    ]
)

INDEXING_COL = find_column(
    df,
    [
        "Indexing Status",
        "Indexing",
        "Indexed"
    ]
)

QUARTILE_COL = find_column(
    df,
    [
        "SJR Quartile",
        "SJR quartile",
        "Quartile",
        "Year-wise Quartile"
    ]
)

PUBLISHER_COL = find_column(
    df,
    [
        "Publisher"
    ]
)

SOURCE_COL = find_column(
    df,
    [
        "Source title",
        "Source Title",
        "Journal",
        "Publication Source"
    ]
)

DOI_COL = find_column(
    df,
    [
        "DOI link",
        "DOI",
        "Doi"
    ]
)

ARTICLE_LINK_COL = find_column(
    df,
    [
        "Article link",
        "Publication link",
        "Link",
        "URL"
    ]
)


# ============================================================
# DATA CLEANING
# ============================================================

if YEAR_COL:

    df["Dashboard Year"] = pd.to_numeric(
        df[YEAR_COL],
        errors="coerce"
    )

else:

    df["Dashboard Year"] = np.nan


for col in df.columns:

    if df[col].dtype == "object":

        df[col] = df[col].apply(clean_value)


# Indexing
if INDEXING_COL:

    df["Dashboard Indexing"] = df[INDEXING_COL].apply(
        normalize_indexing
    )

else:

    df["Dashboard Indexing"] = "Not Available"


# School
if SCHOOL_COL:

    df["Dashboard School"] = df[SCHOOL_COL]

else:

    df["Dashboard School"] = "Not Available"


# Document type
if DOC_TYPE_COL:

    df["Dashboard Document Type"] = df[DOC_TYPE_COL]

else:

    df["Dashboard Document Type"] = "Not Available"


# Quartile
if QUARTILE_COL:

    df["Dashboard Quartile"] = df[QUARTILE_COL]

else:

    df["Dashboard Quartile"] = "Not Available"


# Publisher
if PUBLISHER_COL:

    df["Dashboard Publisher"] = df[PUBLISHER_COL]

else:

    df["Dashboard Publisher"] = "Not Available"


# ============================================================
# SDG DATA
# ============================================================

sdg_columns = [
    col
    for col in df.columns
    if "sdg" in str(col).lower()
]

if sdg_columns:

    df["Dashboard SDGs"] = df[sdg_columns].apply(
        lambda row: sorted(
            set(
                sdg
                for value in row
                for sdg in extract_sdg(value)
            ),
            key=lambda x: int(x.split()[-1])
        ),
        axis=1
    )

else:

    df["Dashboard SDGs"] = [[]]


df["SDG Display"] = df["Dashboard SDGs"].apply(
    lambda x: ", ".join(x) if x else "Not Available"
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">SAI University Research Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Research output, publication quality, institutional contribution and SDG impact'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()


# Year
years = sorted(
    [
        int(x)
        for x in filtered_df["Dashboard Year"].dropna().unique()
    ]
)

selected_years = st.sidebar.multiselect(
    "Year",
    years,
    default=years
)

if selected_years:

    filtered_df = filtered_df[
        filtered_df["Dashboard Year"].isin(selected_years)
    ]


# School
schools = sorted(
    filtered_df["Dashboard School"]
    .dropna()
    .unique()
)

selected_schools = st.sidebar.multiselect(
    "School",
    schools
)

if selected_schools:

    filtered_df = filtered_df[
        filtered_df["Dashboard School"].isin(selected_schools)
    ]


# Author
if AUTHOR_COL:

    author_series = filtered_df[AUTHOR_COL].dropna()

    author_list = sorted(
        set(
            person
            for value in author_series
            for person in split_people(value)
        )
    )

else:

    author_list = []


selected_authors = st.sidebar.multiselect(
    "Faculty Author",
    author_list
)


if selected_authors and AUTHOR_COL:

    filtered_df = filtered_df[
        filtered_df[AUTHOR_COL].apply(
            lambda value: any(
                author in split_people(value)
                for author in selected_authors
            )
        )
    ]


# Document type
doc_types = sorted(
    filtered_df["Dashboard Document Type"]
    .dropna()
    .unique()
)

selected_doc_types = st.sidebar.multiselect(
    "Document Type",
    doc_types
)

if selected_doc_types:

    filtered_df = filtered_df[
        filtered_df["Dashboard Document Type"].isin(
            selected_doc_types
        )
    ]


# Indexing
indexing_options = sorted(
    filtered_df["Dashboard Indexing"]
    .dropna()
    .unique()
)

selected_indexing = st.sidebar.multiselect(
    "Indexing Status",
    indexing_options
)

if selected_indexing:

    filtered_df = filtered_df[
        filtered_df["Dashboard Indexing"].isin(
            selected_indexing
        )
    ]


# Quartile
quartiles = sorted(
    filtered_df["Dashboard Quartile"]
    .dropna()
    .unique()
)

selected_quartiles = st.sidebar.multiselect(
    "SJR Quartile",
    quartiles
)

if selected_quartiles:

    filtered_df = filtered_df[
        filtered_df["Dashboard Quartile"].isin(
            selected_quartiles
        )
    ]


# Publisher
publishers = sorted(
    filtered_df["Dashboard Publisher"]
    .dropna()
    .unique()
)

selected_publishers = st.sidebar.multiselect(
    "Publisher",
    publishers
)

if selected_publishers:

    filtered_df = filtered_df[
        filtered_df["Dashboard Publisher"].isin(
            selected_publishers
        )
    ]


# SDG
all_sdgs = sorted(
    set(
        sdg
        for values in filtered_df["Dashboard SDGs"]
        for sdg in values
    ),
    key=lambda x: int(x.split()[-1])
)

selected_sdgs = st.sidebar.multiselect(
    "SDG",
    all_sdgs
)

if selected_sdgs:

    filtered_df = filtered_df[
        filtered_df["Dashboard SDGs"].apply(
            lambda values: any(
                sdg in values
                for sdg in selected_sdgs
            )
        )
    ]


# Reset button
if st.sidebar.button("Reset Filters"):

    st.rerun()


# ============================================================
# FILTER SUMMARY
# ============================================================

st.caption(
    f"Showing **{len(filtered_df):,}** publications "
    f"from **{len(df):,}** total records."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_publications = len(filtered_df)

scopus_count = filtered_df[
    "Dashboard Indexing"
].str.contains(
    "Scopus",
    case=False,
    na=False
).sum()

wos_count = filtered_df[
    "Dashboard Indexing"
].str.contains(
    "WoS|Web of Science",
    case=False,
    na=False,
    regex=True
).sum()

q1_count = filtered_df[
    "Dashboard Quartile"
].str.contains(
    r"\bQ1\b",
    case=False,
    na=False,
    regex=True
).sum()

school_count = filtered_df[
    "Dashboard School"
].replace(
    "Not Available",
    np.nan
).nunique()

if AUTHOR_COL:

    faculty_authors = set()

    for value in filtered_df[AUTHOR_COL]:

        faculty_authors.update(
            split_people(value)
        )

    faculty_authors = {
        x for x in faculty_authors
        if x and x != "Not Available"
    }

    faculty_count = len(faculty_authors)

else:

    faculty_count = 0


sdg_count = len(
    set(
        sdg
        for values in filtered_df["Dashboard SDGs"]
        for sdg in values
    )
)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">Research Overview</div>',
    unsafe_allow_html=True
)

kpi_columns = st.columns(8)

kpis = [
    ("Total Publications", total_publications),
    ("Scopus Indexed", scopus_count),
    ("Web of Science", wos_count),
    ("Q1 Publications", q1_count),
    ("Schools", school_count),
    ("Faculty Authors", faculty_count),
    ("SDGs Represented", sdg_count),
    ("Years Covered", len(selected_years))
]

for column, (label, value) in zip(kpi_columns, kpis):

    with column:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CHART FUNCTION
# ============================================================

def create_bar_chart(
    data,
    x,
    y,
    title,
    horizontal=False
):

    fig, ax = plt.subplots(
        figsize=(8, 4.5)
    )

    sns.set_theme(
        style="whitegrid"
    )

    if horizontal:

        data = data.sort_values(y)

        sns.barplot(
            data=data,
            x=y,
            y=x,
            ax=ax
        )

    else:

        sns.barplot(
            data=data,
            x=x,
            y=y,
            ax=ax
        )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.tight_layout()

    return fig


# ============================================================
# PUBLICATION TREND
# ============================================================

st.markdown(
    '<div class="section-title">Publication Output</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    if filtered_df["Dashboard Year"].notna().any():

        trend = (
            filtered_df
            .dropna(subset=["Dashboard Year"])
            .groupby("Dashboard Year")
            .size()
            .reset_index(name="Publications")
        )

        trend["Dashboard Year"] = trend[
            "Dashboard Year"
        ].astype(int)

        trend = trend.sort_values(
            "Dashboard Year"
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        sns.lineplot(
            data=trend,
            x="Dashboard Year",
            y="Publications",
            marker="o",
            linewidth=2.5,
            ax=ax
        )

        ax.set_title(
            "Publication Trends Over Time",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Year")
        ax.set_ylabel("Publications")

        plt.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


with col2:

    school_data = (
        filtered_df[
            filtered_df["Dashboard School"] != "Not Available"
        ]
        .groupby("Dashboard School")
        .size()
        .reset_index(name="Publications")
        .sort_values(
            "Publications",
            ascending=False
        )
        .head(10)
    )

    if not school_data.empty:

        fig = create_bar_chart(
            school_data,
            "Dashboard School",
            "Publications",
            "Top Schools by Publication Output",
            horizontal=True
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# SECOND CHART ROW
# ============================================================

col1, col2 = st.columns(2)


with col1:

    doc_data = (
        filtered_df
        .groupby("Dashboard Document Type")
        .size()
        .reset_index(name="Publications")
        .sort_values(
            "Publications",
            ascending=False
        )
    )

    if not doc_data.empty:

        fig = create_bar_chart(
            doc_data.head(10),
            "Dashboard Document Type",
            "Publications",
            "Publications by Document Type",
            horizontal=True
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


with col2:

    indexing_data = (
        filtered_df
        .groupby("Dashboard Indexing")
        .size()
        .reset_index(name="Publications")
        .sort_values(
            "Publications",
            ascending=False
        )
    )

    if not indexing_data.empty:

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        sns.barplot(
            data=indexing_data,
            x="Dashboard Indexing",
            y="Publications",
            ax=ax
        )

        ax.set_title(
            "Indexing Status",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("")
        ax.set_ylabel("Publications")

        plt.xticks(
            rotation=25,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# QUARTILE + SDG
# ============================================================

col1, col2 = st.columns(2)


with col1:

    quartile_data = (
        filtered_df
        .groupby("Dashboard Quartile")
        .size()
        .reset_index(name="Publications")
    )

    quartile_data = quartile_data[
        quartile_data["Dashboard Quartile"]
        != "Not Available"
    ]

    if not quartile_data.empty:

        quartile_order = [
            "Q1",
            "Q2",
            "Q3",
            "Q4"
        ]

        quartile_data[
            "Order"
        ] = quartile_data[
            "Dashboard Quartile"
        ].apply(
            lambda x:
                quartile_order.index(x)
                if x in quartile_order
                else 99
        )

        quartile_data = quartile_data.sort_values(
            "Order"
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        sns.barplot(
            data=quartile_data,
            x="Dashboard Quartile",
            y="Publications",
            ax=ax
        )

        ax.set_title(
            "SJR Quartile Distribution",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("")
        ax.set_ylabel("Publications")

        plt.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


with col2:

    sdg_rows = []

    for values in filtered_df["Dashboard SDGs"]:

        for sdg in values:

            sdg_rows.append(sdg)

    if sdg_rows:

        sdg_data = (
            pd.Series(
                sdg_rows,
                name="SDG"
            )
            .value_counts()
            .reset_index()
        )

        sdg_data.columns = [
            "SDG",
            "Publications"
        ]

        sdg_data = sdg_data.sort_values(
            "SDG",
            key=lambda x: x.str.extract(
                r"(\d+)"
            )[0].astype(int)
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        sns.barplot(
            data=sdg_data,
            x="SDG",
            y="Publications",
            ax=ax
        )

        ax.set_title(
            "SDG Distribution",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("")
        ax.set_ylabel("Publications")

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# FACULTY CONTRIBUTION
# ============================================================

st.markdown(
    '<div class="section-title">Faculty Research Contribution</div>',
    unsafe_allow_html=True
)

if AUTHOR_COL:

    faculty_rows = []

    for _, row in filtered_df.iterrows():

        authors = split_people(
            row[AUTHOR_COL]
        )

        for author in authors:

            if author != "Not Available":

                faculty_rows.append(
                    author
                )

    if faculty_rows:

        faculty_data = (
            pd.Series(
                faculty_rows,
                name="Faculty"
            )
            .value_counts()
            .reset_index()
        )

        faculty_data.columns = [
            "Faculty",
            "Publications"
        ]

        faculty_data = faculty_data.head(15)

        fig = create_bar_chart(
            faculty_data,
            "Faculty",
            "Publications",
            "Top Faculty Authors by Publication Count",
            horizontal=True
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">Automatically Generated Insights</div>',
    unsafe_allow_html=True
)

insights = []


# Year insight
if not filtered_df["Dashboard Year"].dropna().empty:

    yearly = (
        filtered_df
        .groupby("Dashboard Year")
        .size()
    )

    highest_year = yearly.idxmax()
    highest_year_count = yearly.max()

    insights.append(
        f"📈 The highest publication output in the current selection "
        f"occurred in **{int(highest_year)}**, with **{highest_year_count} publications**."
    )


# School insight
school_counts = (
    filtered_df[
        filtered_df["Dashboard School"] != "Not Available"
    ]["Dashboard School"]
    .value_counts()
)

if not school_counts.empty:

    top_school = school_counts.index[0]
    top_school_count = school_counts.iloc[0]

    insights.append(
        f"🏫 **{top_school}** has the highest publication count "
        f"in the current filtered dataset, with **{top_school_count} publications**."
    )


# Q1 insight
if total_publications > 0:

    q1_percentage = (
        q1_count /
        total_publications *
        100
    )

    insights.append(
        f"🏅 Q1 publications account for approximately "
        f"**{q1_percentage:.1f}%** of the filtered publication set."
    )


# Scopus insight
if total_publications > 0:

    scopus_percentage = (
        scopus_count /
        total_publications *
        100
    )

    insights.append(
        f"📚 Approximately **{scopus_percentage:.1f}%** "
        f"of the filtered publications are associated with Scopus indexing."
    )


# SDG insight
if sdg_rows:

    sdg_counts = pd.Series(
        sdg_rows
    ).value_counts()

    top_sdg = sdg_counts.index[0]

    insights.append(
        f"🌍 **{top_sdg}** is the most represented SDG "
        f"in the current publication set."
    )


for insight in insights:

    st.markdown(
        f"""
        <div class="insight-card">
            {insight}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# YEAR-OVER-YEAR ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Year-over-Year Analysis</div>',
    unsafe_allow_html=True
)

if not filtered_df["Dashboard Year"].dropna().empty:

    yoy = (
        filtered_df
        .dropna(subset=["Dashboard Year"])
        .groupby("Dashboard Year")
        .size()
        .reset_index(name="Publications")
        .sort_values("Dashboard Year")
    )

    yoy["Year"] = yoy[
        "Dashboard Year"
    ].astype(int)

    yoy["YoY Change"] = (
        yoy["Publications"]
        .pct_change()
        .mul(100)
        .round(1)
    )

    yoy["YoY Change"] = yoy[
        "YoY Change"
    ].apply(
        lambda x:
            "N/A"
            if pd.isna(x)
            else f"{x:+.1f}%"
    )

    st.dataframe(
        yoy[
            [
                "Year",
                "Publications",
                "YoY Change"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PUBLICATION EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">Publication Explorer</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search publications, authors, journals, publishers or keywords",
    placeholder="e.g. machine learning, AI, Sharma..."
)


explorer_df = filtered_df.copy()


if search:

    search_columns = [
        col
        for col in [
            TITLE_COL,
            AUTHOR_COL,
            ALL_AUTHOR_COL,
            SOURCE_COL,
            PUBLISHER_COL,
            "Keywords",
            "Abstract"
        ]
        if col is not None and col in explorer_df.columns
    ]

    if search_columns:

        mask = pd.Series(
            False,
            index=explorer_df.index
        )

        for col in search_columns:

            mask |= explorer_df[col].astype(
                str
            ).str.contains(
                search,
                case=False,
                na=False
            )

        explorer_df = explorer_df[
            mask
        ]


# ============================================================
# TABLE
# ============================================================

display_columns = []

column_mapping = [
    (TITLE_COL, "Publication"),
    (AUTHOR_COL, "Faculty Author"),
    (SCHOOL_COL, "School"),
    (YEAR_COL, "Year"),
    (SOURCE_COL, "Source"),
    (DOC_TYPE_COL, "Document Type"),
    (INDEXING_COL, "Indexing"),
    (QUARTILE_COL, "SJR Quartile"),
    (PUBLISHER_COL, "Publisher")
]

for original, display in column_mapping:

    if original and original in explorer_df.columns:

        display_columns.append(
            (original, display)
        )


table_df = pd.DataFrame()

for original, display in display_columns:

    table_df[display] = explorer_df[
        original
    ].values


# Add links
if DOI_COL and DOI_COL in explorer_df.columns:

    table_df["DOI"] = explorer_df[
        DOI_COL
    ].values


if ARTICLE_LINK_COL and ARTICLE_LINK_COL in explorer_df.columns:

    table_df["Publication Link"] = explorer_df[
        ARTICLE_LINK_COL
    ].values


st.caption(
    f"{len(explorer_df):,} matching publications"
)


st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    height=500
)


# ============================================================
# EXPORT
# ============================================================

st.markdown(
    '<div class="section-title">Export Data</div>',
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇ Download Filtered Publications CSV",
    data=csv_data,
    file_name="sai_research_filtered.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "SAI University Research Intelligence Dashboard • "
    "Data dynamically retrieved from the SAI University Publications API"
)