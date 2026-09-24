# SAI University Research Intelligence Dashboard

An interactive **Research Analytics Dashboard** built with Python, Pandas, Matplotlib, Seaborn and Streamlit to explore SAI University's research publications, publication quality, institutional contributions and research impact.

The dashboard consumes publication data dynamically from the official SAI University Publications API rather than relying on manually entered records.

---

## Project Overview

Universities generate research across multiple schools, disciplines and research areas. However, raw publication records can make it difficult to understand broader research patterns.

This project transforms the SAI University publication dataset into an interactive analytics platform that allows users to explore:

* Research output over time
* Publication contribution by school
* Faculty publication activity
* Publication and document types
* Scopus and Web of Science indexing
* SJR journal quartiles
* Sustainable Development Goal (SDG) representation
* Publishers and research sources
* Individual publication records

The dashboard is designed to support different users including university leadership, faculty members, researchers and students.

---

## Objectives

The main objectives of the project are to:

1. Retrieve publication data dynamically using a REST API.
2. Clean and standardize the publication dataset using Pandas.
3. Calculate meaningful research KPIs.
4. Analyse publication trends and institutional contributions.
5. Visualize publication quality and research impact.
6. Provide interactive filtering across multiple dimensions.
7. Provide a searchable publication explorer.
8. Handle missing and incomplete metadata appropriately.
9. Generate automatic insights from the filtered dataset.
10. Provide filtered-data export functionality.

---

## Technology Stack

| Technology      | Purpose                                    |
| --------------- | ------------------------------------------ |
| Python          | Core programming and data processing       |
| Pandas          | Data cleaning, transformation and analysis |
| Requests        | Fetching data from the REST API            |
| Matplotlib      | Data visualization                         |
| Seaborn         | Statistical visualization                  |
| Streamlit       | Interactive dashboard interface            |
| REST API / JSON | Dynamic publication data source            |

---

## Data Source

The dashboard uses the SAI University Publications API:

**API Endpoint:**

https://sai-publications-dashboard.vercel.app/api/publications

The data is retrieved dynamically when the application runs.

Publication records contain information such as:

* Publication title
* Authors
* SAIU authors
* School
* Publication year
* Publication date
* Source/journal
* Document type
* Publisher
* DOI
* Publication links
* Indexing status
* SJR quartile
* Year-wise quartile
* SDG information
* Abstract
* Keywords

The application does **not** manually store individual publication records.

---

## Dashboard Features

### 1. KPI Section

The dashboard displays dynamically calculated research KPIs including:

* Total publications
* Scopus-indexed publications
* Web of Science-indexed publications
* Q1 publications
* Number of schools
* Number of faculty authors
* Number of SDGs represented
* Number of publication years

All KPIs update automatically when filters are applied.

---

### 2. Publication Trend

A time-series visualization shows how the number of publications changes across years.

This helps answer:

> How has SAI University's research output changed over time?

---

### 3. Publications by School

A horizontal bar chart compares publication output across schools.

This helps identify:

* Schools with higher publication activity
* Relative research contribution
* Changes in school-level output after applying filters

---

### 4. Document Type Analysis

The dashboard visualizes different publication types such as:

* Articles
* Conference papers
* Book chapters
* Reviews
* Other document categories available in the API

The visualization updates according to the active filters.

---

### 5. Indexing Status

The dashboard analyses publication indexing status, including available categories such as:

* Scopus
* Web of Science
* Scopus + Web of Science
* Non Indexed
* Other API-provided categories

This provides an overview of the indexed research output.

---

### 6. SJR Quartile Distribution

Publications are analysed according to their available SJR quartile:

* Q1
* Q2
* Q3
* Q4
* Not Available

Missing quartile information is preserved as **Not Available** rather than incorrectly assigning a quartile.

---

### 7. Faculty Contribution

The dashboard identifies researchers with the highest publication counts within the current filter selection.

This provides a view of individual faculty publication activity.

---

### 8. SDG Distribution

Publication-level SDG information is processed and combined from the available SDG fields.

The dashboard shows the number of publications associated with different United Nations Sustainable Development Goals.

This helps answer:

> Which global development goals are represented in SAI University's research?

---

### 9. Interactive Filters

Users can filter the dashboard using dimensions such as:

* Year
* School
* Author
* Document type
* Indexing status
* SJR quartile
* Publisher

All major KPIs and visualizations respond to the selected filters.

---

### 10. Publication Explorer

The Publication Explorer provides a searchable and sortable view of the underlying research records.

Users can search for:

* Publication titles
* Authors
* Journals
* Publishers
* Keywords
* Abstract content

Available DOI and publication links can be opened directly from the dashboard.

---

### 11. Year-over-Year Analysis

The dashboard calculates annual publication counts and year-over-year percentage change.

This allows users to examine changes in research output between consecutive years.

---

### 12. Automatic Research Insights

The dashboard generates summary observations based on the currently selected data.

Examples include:

* Current publication count
* Latest publication year
* School with the highest publication count
* Faculty member with the highest publication count
* Number of Q1 publications

These insights change dynamically with the applied filters.

---

### 13. Export

Users can download the currently filtered publication dataset as a CSV file.

This allows further analysis outside the dashboard.

---

## Data Cleaning and Handling

Data quality is important because the API contains incomplete metadata for some publications.

The application performs several preprocessing operations:

### Missing values

Empty categorical values are converted to:

`Not Available`

This prevents missing values from being incorrectly interpreted.

### Year conversion

Publication years are converted to numeric values using error handling so invalid or missing years do not crash the application.

### SDG processing

SDG information may appear across multiple API fields.

The dashboard combines available SDG values and removes duplicate SDGs within each publication.

### Indexing

Indexing information is interpreted from the API's available indexing-status fields.

### Quartiles

Available SJR quartiles are preserved as provided by the API.

Missing quartile information is represented as:

`Not Available`

This ensures that missing data is not incorrectly classified as Q4.

---

## Project Architecture

```text
                    SAI Publications API
                            │
                            ▼
                    REST API / JSON
                            │
                            ▼
                     Python Requests
                            │
                            ▼
                         Pandas
                            │
                  Data Cleaning & Processing
                            │
                            ▼
                    Filtered DataFrame
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          KPIs        Visualizations    Insights
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                       Streamlit UI
                            │
                            ▼
                 Research Intelligence
                       Dashboard
```

---

## Project Structure

```text
sai-research-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
└── assets/
    └── logo.png
```

---

## Installation

### 1. Clone or download the project

```bash
git clone <repository-url>
cd sai-research-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

The `requirements.txt` file contains:

```text
streamlit
pandas
requests
matplotlib
seaborn
```

---

## Running the Dashboard

Run the following command from the project directory:

```bash
streamlit run app.py
```

Streamlit will start a local web server and provide a URL for the dashboard.

---

## Example Workflow

The dashboard follows the required data-analysis pipeline:

```text
Fetch
  ↓
Clean
  ↓
Transform
  ↓
Filter
  ↓
Analyse
  ↓
Visualize
  ↓
Generate Insights
  ↓
Explore / Export
```

---

## Design Principles

The dashboard was designed around five principles:

### Data Accuracy

Statistics are calculated directly from the API dataset.

### Dynamic Analysis

Publication records are retrieved dynamically instead of being manually entered.

### Interactive Exploration

Filters affect KPIs, visualizations and publication results.

### Research Intelligence

The dashboard focuses on meaningful research questions rather than simply displaying charts.

### Missing Data Transparency

Incomplete metadata is explicitly represented instead of being silently converted into potentially misleading values.

---

## Key Research Questions

The dashboard is designed to answer questions such as:

### Research Output

* How many publications are represented?
* How has publication output changed over time?
* What is the year-over-year change?

### Institutional Contribution

* Which schools contribute most to publication output?
* Which faculty members have significant publication activity?
* How does the distribution change under different filters?

### Publication Quality

* How many publications are indexed in Scopus?
* How many are indexed in Web of Science?
* How many publications are classified as Q1?
* What is the distribution across SJR quartiles?

### Research Impact

* Which SDGs are represented?
* Which SDGs have the largest publication representation?
* How does SDG distribution vary by school or year?

### Publication Discovery

* Which researchers have published on a particular topic?
* Which journals or publishers appear most frequently?
* Can users directly access the DOI or publication?

---

## Performance Considerations

The API response is cached using Streamlit's data caching mechanism.

This reduces unnecessary API requests during normal dashboard interaction while still allowing the application to refresh the data periodically.

```python
@st.cache_data(ttl=3600)
def load_data():
    ...
```

The cache is configured with a one-hour lifetime.

---

## Limitations

The dashboard depends on the metadata supplied by the SAI University Publications API.

Therefore:

* Missing metadata cannot be reliably inferred.
* Some publications may not contain DOI information.
* Some records may not contain indexing information.
* Quartile information may be unavailable for some publications.
* SDG information may be incomplete.
* Publication metadata may change when the API is updated.

The dashboard therefore distinguishes between **zero**, **not applicable**, and **not available** wherever possible.

---

## Future Enhancements

Possible future improvements include:

* Individual researcher profile pages
* School-specific dashboards
* SDG heatmaps
* Advanced multi-field search
* Publication comparison tools
* Research collaboration/network analysis
* Co-author network visualization
* Interactive drill-down charts
* More detailed year-over-year analysis
* PDF report generation
* Scheduled data refresh
* Mobile-optimized layouts
* Dark mode
* Research topic/keyword analysis
* Geographic analysis of publishers and collaborations

---

## Conclusion

The SAI University Research Intelligence Dashboard converts raw publication data into an interactive analytical system for understanding the university's research ecosystem.

The project demonstrates the complete data analytics workflow:

**Data → Cleaning → Analysis → Visualization → Interaction → Insights**

Rather than treating the publication dataset as a static table, the dashboard provides users with an interactive way to investigate research output, publication quality, institutional contribution and research impact.

---

## Author

**SAI University Student Project**

Built using:

**Python · Pandas · Matplotlib · Seaborn · Streamlit · REST API**
