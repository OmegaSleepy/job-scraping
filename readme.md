> A: От къде разбрахте за тази позиция?    
> B: Ами написах си един web scraper.   
> ~ my cousin

# Job Market Research Analysis

An in-depth data analysis project exploring modern job listings to identify trends in employment categories, geographic distribution, and the most in-demand technical skills across various sectors.

---

## 📊 Project Overview
This repository contains a comprehensive analysis of job market data. By processing thousands of job listings, this research highlights which sectors are growing and which specific skill sets are mandatory for candidates in today’s economy.

## 📈 Local Trends (BG)
These high-level visualizations provide an overview of the entire dataset, showing where the jobs are and what they entail.

### Job Categories & Locations
I analyzed the distribution of roles to see which industries dominate the current market and where those jobs are physically concentrated.

| Job Categories | Job Locations |
| :---: | :---: |
| ![Job Categories](plots/Job_Distribution_By_Category.png) | ![Job Locations](plots/Job_Distribution_By_Location.png) |

### Most In-Demand Skills (Overall)
This chart represents the frequency of skill mentions across the entire dataset, regardless of the specific job category.
![Top Skills Overall](plots/Top_Skills_Required.png)

---

## 🔍 Skills Analysis by Category
The core of this research breaks down the "Top Skills" required for specific career paths. Below are the visual breakdowns for each major industry sector:

### Development & Software Engineering
* **Full Stack Development:** ![Full Stack](plots_by_category/Top_Skills_For_full_stack_development.png)
* **Back-End Development:** ![Back End](plots_by_category/Top_Skills_For_back_end_development.png)
* **Front-End Development:** ![Front End](plots_by_category/Top_Skills_For_front_end_development.png)
* **Mobile Development:** ![Mobile](plots_by_category/Top_Skills_For_mobile_development.png)
* **Hardware & Engineering:** ![Hardware](plots_by_category/Top_Skills_For_hardware_and_engineering.png)

### Data, Design & Specialized Tech
* **Data Science:** ![Data Science](plots_by_category/Top_Skills_For_data_science.png)
* **UI/UX & Arts:** ![UI/UX](plots_by_category/Top_Skills_For_ui_ux_and_arts.png)
* **ERP/CRM Development:** ![ERP/CRM](plots_by_category/Top_Skills_For_erp_crm_development.png)

### Operations & Support
* **Operations:** ![Operations](plots_by_category/Top_Skills_For_operations.png)
* **Quality Assurance:** ![QA](plots_by_category/Top_Skills_For_quality_assurance.png)
* **Technical Support:** ![Tech Support](plots_by_category/Top_Skills_For_technical_support.png)
* **Customer Support:** ![Customer Support](plots_by_category/Top_Skills_For_customer_support.png)
* **PM, BA & More:** ![Project Management](plots_by_category/Top_Skills_For_pm_ba_and_more.png)

---

## 🛠 Methodology
1. **Data Collection:** Data was aggregated from multiple* job boards and listing sites.
2. **Data Cleaning:** Removed duplicate listings, handled missing values, and normalized job titles into standardized categories.
3. **Visualization:** Generated using Python-based libraries (Matplotlib).

## Limitations
* Due to TOS, I cannot share the website I scraped the data from.   
* The data is only for the Bulgarian programming/tech market.

## Working on
1. Integrating more datasets

# 🛠 Setup & Execution
## 1. Scraper (Java/Maven)

Build and run the data collection tool:
```Bash

# Build the project
mvn clean install

# Run the scraper
mvn exec:java -Dexec.mainClass="your.package.Main"
```
## 2. Statistics (Python)

Process the data and generate the plots:
```Bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate plots
python generate_stats.py
```
## 📂 Project Structure
  `pom.xml` — Maven configuration.   
  `src/` — Java scraper source code.   
  `generate_stats.py` — Python analysis script.   
  `plots/` — Global trend visualizations.    
  `plots_by_category/` — Sector-specific skill breakdowns.   
