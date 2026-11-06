
# SWYNEX Interactive Dashboard

## Project Overview

This project focuses on developing an interactive student performance and attendance dashboard using Python, Streamlit, Pandas, and Plotly.

The goal is to analyze student data, visualize performance patterns, identify useful insights, and present the results through an interactive dashboard.

## Dashboard Features

- KPI cards for total students, average valid marks, average valid attendance, and records needing review.
- Student marks bar chart.
- Age distribution chart.
- Attendance vs marks scatter plot.
- Attendance-range comparison.
- Interactive sidebar filters for age, student name, and data quality.
- Filtered student data table.
- CSV download functionality.
- Key findings and data-quality notes.

## Dataset

The cleaned student dataset is stored in the `data` folder.

**Dataset file:** `cleaned_student_data.csv`

**Required columns:**
- `student_id`
- `name`
- `age`
- `marks`
- `attendance_percentage`

The dashboard identifies marks and attendance values outside the 0–100 range. It does not modify the original source CSV.

## Tools Used

- Python
- Streamlit
- Pandas
- Plotly
- Visual Studio Code
- GitHub

## Project Structure

```text
SWYNEX-Interactive-Dashboard/
├── data/
│   └── cleaned_student_data.csv
├── screenshots/
│   ├── dashboard-overview.png
│   ├── data-explorer.png
│   └── performance-analysis.png
├── app.py
├── requirements.txt
└── README.md
```

## Screenshots

### 1. Dashboard Overview

This screenshot shows the main dashboard with KPI cards and student performance information.

![Dashboard Overview](screenshots/dashboard-overview.png)

### 2. Data Exploration

This screenshot shows the interactive data exploration section with filters and student records.

![Data Exploration](screenshots/data-explorer.png)

### 3. Performance Analysis

This screenshot shows the visual analysis of student performance, attendance patterns, and related insights.

![Performance Analysis](screenshots/performance-analysis.png)

## Results

- Displays total student count and average valid marks.
- Calculates average valid attendance.
- Identifies records requiring data-quality review.
- Visualizes student performance and attendance patterns.
- Provides interactive filtering and CSV download options.
- Presents key findings through charts and visualizations.

## How to Run

### 1. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Run the Dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser. If it does not open automatically, use the local address displayed in the terminal.

## Deployment on Streamlit Community Cloud

1. Upload the project to a GitHub repository.
2. Ensure `app.py`, `requirements.txt`, and `data/cleaned_student_data.csv` are included.
3. Open Streamlit Community Cloud.
4. Connect your GitHub repository.
5. Select `app.py` as the main file.
6. Deploy the application.

## Conclusion

This project demonstrates the practical application of data analysis and visualization techniques using Python. It provides an interactive way to explore student performance and attendance data, identify patterns, review data quality, and communicate meaningful insights through a dashboard.

## Author

**Priyada Mangaonkar**

## Connect & Project

- **GitHub Repository:** [SWYNEX Interactive Dashboard](https://github.com/mangaonkarpriyada-code/SWYNEX-Interactive-Dashboard)
- **LinkedIn Profile:** [Connect with Priyada Mangaonkar](https://www.linkedin.com/in/priyada-mangaonkar-906b42424/)