# 📊 Google Play Store Data Analytics

An interactive **Google Play Store Data Analytics Dashboard** developed as part of an internship project. The project analyzes Google Play Store application data and user reviews using Python and presents the analysis through an interactive Streamlit dashboard.

The dashboard contains **six internship tasks**, each implementing specific filtering, visualization, analytical, and time-based requirements.

---

## 🚀 Live Project

### 🌐 Live Streamlit Dashboard

https://playstoreanalytics-g54eowappqc648mpt8dsy9m.streamlit.app

### 💻 GitHub Repository

https://github.com/codewithankit45/PlayStoreAnalytics

### 📂 Dataset – Google Drive

https://drive.google.com/drive/folders/1VYJ-riP2b6baCrnkkkF2E7R4i63mUBzG?usp=sharing

---

## 📌 Project Overview

The objective of this project is to perform data analysis on Google Play Store applications and their user reviews and convert the analysis into an interactive dashboard.

The project includes:

* Data cleaning and preprocessing
* Dataset merging
* Application/category filtering
* Rating and review analysis
* Install analysis
* Revenue analysis
* Free vs Paid application comparison
* Category-wise analysis
* Monthly install trend analysis
* Interactive visualizations
* Time-based dashboard visibility
* Six internship-specific analytical tasks

---

## 📁 Datasets

The project uses the following datasets:

### 1. Play Store Data

**File:** `Play Store Data.csv`

Contains information about Google Play Store applications, including:

* App Name
* Category
* Rating
* Reviews
* Size
* Installs
* Type
* Price
* Content Rating
* Genres
* Last Updated
* Current Version
* Android Version

### 2. User Reviews

**File:** `User Reviews.csv`

Contains user-review information used for sentiment-related analysis, including:

* App
* Translated Review
* Sentiment
* Sentiment Polarity
* Sentiment Subjectivity

---

# 📊 Internship Tasks

## Task 1 — App Size vs Average Rating

### Visualization

Bubble Chart

### Analysis

The task analyzes the relationship between:

* App Size
* Average Rating
* Number of Installs

The visualization applies the required internship filters, including rating, reviews, installs, app-name conditions, sentiment subjectivity and selected categories.

The **Game** category is highlighted according to the task requirement.

Category translations are also applied for the specified categories.

The chart is displayed only during its assigned IST time window.

---

## Task 2 — Global Installs by Category

### Visualization

Choropleth Map

The task analyzes global application installs by category.

The dashboard:

* Identifies the top application categories
* Applies the required category filters
* Highlights categories according to the install threshold
* Displays the geographical distribution using a choropleth visualization
* Applies the assigned IST time restriction

---

## Task 3 — Monthly Install Trend by Category

### Visualization

Time Series Line Chart

The task analyzes monthly installation trends across application categories.

The analysis includes:

* Monthly install aggregation
* Category filtering
* Review filtering
* App-name filtering
* Month-over-month install growth analysis
* Highlighting periods with significant MoM growth
* Category translations where required
* Logarithmic install scale for better visualization of highly varying install values

The chart is available only during its assigned IST time window.

---

## Task 4 — Cumulative Installs by Category

### Visualization

Stacked Area Chart

The task analyzes cumulative installs over time for application categories.

The analysis includes:

* App-name filtering
* Category filtering
* Category translation
* Monthly data preparation
* Month-over-month install analysis
* Highlighting months with significant MoM growth
* Stacked area visualization for cumulative category-wise installs

Each category is represented as a separate area band.

The chart follows the assigned IST time restriction.

---

## Task 5 — Top Categories by Installs

### Visualization

Grouped Bar Chart

The task compares the top application categories based on installs.

The analysis includes:

* Data cleaning
* Missing-value handling
* Category-wise aggregation
* Identification of top categories by total installs
* Review conversion into millions
* Average rating calculation
* Total review calculation
* Grouped visualization
* Required dashboard time restriction

---

## Task 6 — Average Installs vs Average Revenue — Free vs Paid

### Visualization

Dual-Axis Chart

This task compares application performance between **Free** and **Paid** applications.

The analysis includes:

* App Name Length calculation
* Free/Paid application classification
* Revenue filtering
* Top 3 category identification
* Category and App Type aggregation
* Average Installs calculation
* Average Revenue calculation
* Free vs Paid comparison
* Dual-axis visualization

For paid applications, the required revenue threshold is applied before analysis.

The final visualization keeps the **Top 3 categories** in the required order.

---

# 🛠️ Technologies Used

### Programming Language

* Python

### Data Analysis

* Pandas
* NumPy

### Data Visualization

* Plotly
* Matplotlib
* Seaborn

### Dashboard

* Streamlit

### Development Tools

* VS Code
* Jupyter Notebook
* Git
* GitHub

---

# 📂 Project Structure

```text
PlayStoreAnalytics/
│
├── app.py
├── style.css
├── requirements.txt
│
├── Internship_Project.ipynb
├── Analysis.ipynb
├── Analysis2.ipynb
├── Analysis3.ipynb
│
├── Play Store Data.csv
├── User Reviews.csv
│
├── README.md
└── .gitignore
```

---

# ▶️ Run the Project Locally

## 1. Clone the Repository

```bash
git clone https://github.com/codewithankit45/PlayStoreAnalytics.git
```

## 2. Open the Project Folder

```bash
cd PlayStoreAnalytics
```

## 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

## 4. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will then open in your browser.

---

# ⏰ Time-Based Dashboard Behavior

Each internship task has an assigned IST time window.

The dashboard checks the current IST time before displaying the corresponding task visualization.

For testing charts outside their assigned time windows, temporarily set:

```python
DEBUG_MODE = True
```

For final/project submission behavior, keep:

```python
DEBUG_MODE = False
```

---

# 📓 Jupyter Notebook

The analytical development and task implementation are also available in the project notebooks:

* `Internship_Project.ipynb`
* `Analysis.ipynb`
* `Analysis2.ipynb`
* `Analysis3.ipynb`

These notebooks contain the underlying data analysis and visualization work used during project development.

---

# 📦 Main Application

The main dashboard entry point is:

```text
app.py
```

The dashboard styling is handled through:

```text
style.css
```

Dependencies are listed in:

```text
requirements.txt
```

---

# 🔗 Project Resources

| Resource                 | Link                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------ |
| 🌐 Live Dashboard        | https://playstoreanalytics-g54eowappqc648mpt8dsy9m.streamlit.app                     |
| 💻 GitHub Repository     | https://github.com/codewithankit45/PlayStoreAnalytics                                |
| 📂 Google Drive Datasets | https://drive.google.com/drive/folders/1VYJ-riP2b6baCrnkkkF2E7R4i63mUBzG?usp=sharing |

---

# 🎯 Project Outcome

The final project provides an interactive dashboard for analyzing Google Play Store applications through multiple analytical perspectives.

The completed dashboard integrates all **six internship tasks** into a single Streamlit application with task-specific visualizations, filters, analytical calculations and time-based visibility.

---

## 👨‍💻 Project

**Google Play Store Data Analytics**

Developed using Python, Pandas, Plotly and Streamlit as an internship data analytics project.
