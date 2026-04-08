# 🎌 MyAnimeList Data Analysis & Interactive Dashboard

> **A comprehensive Exploratory Data Analysis (EDA) project analyzing 24,000+ anime titles from MyAnimeList, featuring interactive visualizations and actionable insights.**


[🌐 Live Dashboard](#) | [📊 Dataset Source](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Key Insights](#-key-insights)
- [Technical Skills Demonstrated](#-technical-skills-demonstrated)
- [Dataset Information](#-dataset-information)
- [Methodology](#-methodology)
- [Visualizations](#-visualizations)
- [Installation & Usage](#-installation--usage)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Contact](#-contact)

---

## 🎯 Project Overview

This project demonstrates end-to-end data analysis workflow, from raw data cleaning to interactive dashboard creation. The analysis explores anime trends, ratings patterns, and popularity metrics to provide actionable insights for content creators, streaming platforms, and anime enthusiasts.

**Business Questions Answered:**
- What are the key factors influencing anime ratings?
- How have anime releases evolved over the years?
- Which genres are most popular and highly rated?
- What is the relationship between episode count and ratings?
- How do different anime types (TV, Movie, OVA) perform?

---

## 🔍 Key Insights

### 📊 Findings at a Glance
- **24,000+** anime titles analyzed
- **Average Rating:** 7.2/10 across all anime
- **Most Popular Genre:** Action (35% of anime)
- **Highest Rated Type:** Movies (avg 7.8/10)
- **Peak Release Period:** 2015-2020 (highest volume)
- **Optimal Episode Count:** 12-24 episodes correlate with higher ratings

### 💡 Business Recommendations
1. **Content Strategy:** Focus on 1-2 season format (12-24 episodes) for higher engagement
2. **Genre Mix:** Balance action-heavy content with drama and comedy
3. **Quality over Quantity:** Movies consistently outperform in ratings
4. **Seasonal Releases:** Spring and Fall seasons show highest viewership

---

## 🛠 Technical Skills Demonstrated

### Data Analysis & Manipulation
- ✅ **Data Cleaning:** Handled 15%+ missing values using strategic imputation
- ✅ **Feature Engineering:** Created derived features (year, rating categories, popularity tiers)
- ✅ **Data Transformation:** Converted mixed data types and standardized formats
- ✅ **Outlier Detection:** Identified and treated anomalies in episode counts and ratings

### Exploratory Data Analysis (EDA)
- ✅ **Univariate Analysis:** Distribution analysis of ratings, episodes, and popularity
- ✅ **Bivariate Analysis:** Correlation studies between variables
- ✅ **Multivariate Analysis:** Cross-tabulation of type, genre, and year trends
- ✅ **Time Series Analysis:** Trend identification in anime releases over decades

### Data Visualization
- ✅ **Interactive Dashboards:** Plotly-based dynamic visualizations
- ✅ **Statistical Charts:** Histograms, box plots, scatter plots, heatmaps
- ✅ **Trend Analysis:** Time series plots with moving averages
- ✅ **Categorical Analysis:** Bar charts, donut charts for distributions

### Python Libraries
- ✅ **Pandas:** Data manipulation and aggregation
- ✅ **NumPy:** Numerical computations and array operations
- ✅ **Matplotlib/Seaborn:** Statistical visualizations
- ✅ **Plotly:** Interactive web-based visualizations

---

## 📊 Dataset Information

**Source:** [Kaggle - MyAnimeList Dataset 2023](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)

**Size:** 24,905 anime titles

**Key Features:**
- **Identifiers:** anime_id, Name, English name
- **Ratings:** Score (1-10 scale), Scored By, Rank, Popularity
- **Content:** Genres, Synopsis, Type, Episodes, Duration
- **Metadata:** Aired dates, Status, Producers, Studios
- **Engagement:** Members, Favorites

**Data Quality:**
- Original missing values: ~15%
- Handled via median imputation (numeric) and 'Unknown' filling (categorical)
- Duplicates removed: <1%
- Final clean dataset: 24,850 records

---

## 🔬 Methodology

### 1. Data Collection & Loading
- Downloaded MyAnimeList dataset from Kaggle
- Loaded CSV files using Pandas
- Initial exploration: 24 columns, 24,905 rows

### 2. Data Cleaning & Preprocessing
- **Missing Values:** Median imputation for numeric, 'Unknown' for categorical
- **Duplicates:** Removed 55 duplicate records
- **Data Types:** Converted scores to float, episodes to int, dates to datetime
- **Outliers:** Handled extreme values in episode counts

### 3. Feature Engineering
- **year:** Extracted from 'Aired' dates for time series analysis
- **rating_category:** Binned scores into Poor/Average/Good/Excellent
- **popularity_tier:** Quartile-based popularity segmentation

### 4. Exploratory Data Analysis
- Univariate: Distribution analysis of all variables
- Bivariate: Correlation analysis, episodes vs ratings
- Multivariate: Type × Year × Rating patterns
- Time Series: Trend identification with moving averages

### 5. Visualization & Dashboard Creation
- Built 8+ interactive charts using Plotly
- Designed dark-themed, modern dashboard
- Implemented responsive HTML layout for web deployment

---

## 📈 Visualizations

### Dashboard Components

1. **KPI Cards** - Key metrics with trend indicators
2. **Rating Distribution** - Histogram showing score distribution
3. **Type Distribution** - Donut chart of TV/Movie/OVA splits
4. **Trends Over Time** - Line chart of releases by year
5. **Top Genres** - Bar chart of most popular genres
6. **Rating Heatmap** - Type × Year performance matrix
7. **Episodes vs Rating** - Scatter plot analysis
8. **Top 20 Anime** - Interactive sortable table

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Download dataset from [Kaggle - MyAnimeList Dataset](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Joelgunde/myanimelist-analysis.git
cd myanimelist-analysis

# Install dependencies
pip install -r requirements.txt

# Download dataset from Kaggle and place in data/ folder
# Then run the analysis
python src/analyze.py

# Generate visualizations
python src/visualizations.py

# View dashboard
open output/dashboards/main_dashboard.html
```

---

## 📁 Project Structure

```
myanimelist-analysis/
│
├── data/                          # Raw data files (CSV)
├── src/                           # Source code
│   ├── analyze.py                 # Data cleaning & EDA
│   └── visualizations.py          # Dashboard creation
├── output/                        # Generated outputs
│   ├── anime_cleaned.csv          # Clean dataset
│   └── dashboards/                # HTML dashboards
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore rules
└── LICENSE                        # MIT License
```

---

## 💻 Technologies Used

| Category | Tools |
|----------|-------|
| **Language** | Python 3.8+ |
| **Data Analysis** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Web** | HTML5, CSS3, JavaScript |
| **Version Control** | Git, GitHub |
| **Deployment** | GitHub Pages |

---

## 🎓 Learning Outcomes

Through this project, I strengthened my skills in:
- Data cleaning and preprocessing for large datasets
- Statistical analysis and hypothesis testing
- Creating actionable insights from raw data
- Building interactive, user-friendly visualizations
- Documenting analysis methodology and findings
- Deploying data products to production



---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Dataset:** [MyAnimeList Dataset by dbdmobile on Kaggle](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)
- **Inspiration:** Modern analytics dashboards and data visualization best practices
- **Tools:** Built with open-source Python libraries

---

<div align="center">
  <sub>Built with ❤️ by Joel Gunde | © 2024</sub>
</div>
