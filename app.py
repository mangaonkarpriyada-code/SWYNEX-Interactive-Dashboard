import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="SWYNEX | Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = Path(__file__).parent / "data" / "cleaned_student_data.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    required = {"student_id", "name", "age", "marks", "attendance_percentage"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

    for col in ["age", "marks", "attendance_percentage"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["student_id"] = df["student_id"].astype(str)
    df["name"] = df["name"].fillna("Unknown").astype(str).str.strip()
    df["marks_valid"] = df["marks"].between(0, 100)
    df["attendance_valid"] = df["attendance_percentage"].between(0, 100)
    df["valid_record"] = df["marks_valid"] & df["attendance_valid"]
    return df

st.title("Student Performance & Attendance Dashboard")
st.caption("SWYNEX Data Analyst Internship | Task 3: Interactive Dashboard")
st.markdown(
    "Explore student marks and attendance, compare performance, and identify records "
    "that may need further review."
)

if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Copy cleaned_student_data.csv from your Task2-EDA/data folder "
        "into the data folder beside app.py."
    )
    st.code("SWYNEX_Task3_Interactive_Dashboard/\n  app.py\n  requirements.txt\n  data/\n    cleaned_student_data.csv")
    st.stop()

try:
    df = load_data(DATA_PATH)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

with st.sidebar:
    st.header("Dashboard Filters")
    st.caption("Filters update the KPIs, charts and table below.")

    age_values = df["age"].dropna()
    if not age_values.empty:
        age_min, age_max = int(age_values.min()), int(age_values.max())
        if age_min == age_max:
            selected_ages = (age_min, age_max)
            st.write(f"Age: {age_min}")
        else:
            selected_ages = st.slider("Age range", age_min, age_max, (age_min, age_max))
    else:
        selected_ages = None

    names = sorted(df["name"].dropna().unique().tolist())
    selected_names = st.multiselect("Student name", names, default=names)

    record_filter = st.selectbox(
        "Data quality",
        ["All records", "Valid marks and attendance only", "Records needing review"]
    )

filtered = df.copy()
if selected_ages is not None:
    filtered = filtered[filtered["age"].between(selected_ages[0], selected_ages[1])]
filtered = filtered[filtered["name"].isin(selected_names)]

if record_filter == "Valid marks and attendance only":
    filtered = filtered[filtered["valid_record"]]
elif record_filter == "Records needing review":
    filtered = filtered[~filtered["valid_record"]]

valid_marks = filtered.loc[filtered["marks_valid"], "marks"]
valid_attendance = filtered.loc[filtered["attendance_valid"], "attendance_percentage"]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Students in view", f"{len(filtered):,}")
k2.metric("Average valid marks", f"{valid_marks.mean():.2f}" if not valid_marks.empty else "N/A")
k3.metric("Average attendance", f"{valid_attendance.mean():.2f}%" if not valid_attendance.empty else "N/A")
k4.metric("Records to review", f"{int((~filtered['valid_record']).sum()):,}")

st.divider()

if filtered.empty:
    st.warning("No records match the selected filters. Change the filters to see results.")
    st.stop()

left, right = st.columns(2)

with left:
    marks_df = filtered[filtered["marks_valid"]].copy()
    if not marks_df.empty:
        fig = px.bar(
            marks_df.sort_values("marks", ascending=False),
            x="name", y="marks", color="marks",
            hover_data=["student_id", "age", "attendance_percentage"],
            title="Marks by Student",
            labels={"name": "Student", "marks": "Marks"}
        )
        fig.update_layout(xaxis_tickangle=-35, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid marks are available for the current selection.")

with right:
    age_df = filtered.dropna(subset=["age"])
    if not age_df.empty:
        fig = px.histogram(
            age_df, x="age", nbins=max(1, min(10, age_df["age"].nunique())),
            title="Student Age Distribution",
            labels={"age": "Age", "count": "Number of Students"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No age values are available for the current selection.")

left, right = st.columns(2)

with left:
    scatter_df = filtered[filtered["marks_valid"] & filtered["attendance_valid"]]
    if not scatter_df.empty:
        fig = px.scatter(
            scatter_df, x="attendance_percentage", y="marks",
            color="age", hover_name="name",
            hover_data=["student_id"],
            title="Attendance vs Marks",
            labels={
                "attendance_percentage": "Attendance (%)",
                "marks": "Marks",
                "age": "Age"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        if len(scatter_df) >= 3:
            corr = scatter_df[["marks", "attendance_percentage"]].corr().iloc[0, 1]
            st.caption(f"Correlation in the current filtered view: {corr:.3f}. Correlation does not prove causation.")
    else:
        st.info("At least one valid marks and attendance record is needed for this chart.")

with right:
    attendance_df = filtered[filtered["attendance_valid"]].copy()
    if not attendance_df.empty:
        attendance_df["Attendance Group"] = pd.cut(
            attendance_df["attendance_percentage"],
            bins=[-0.01, 60, 75, 90, 100],
            labels=["0–60%", "61–75%", "76–90%", "91–100%"],
            include_lowest=True
        )
        group_counts = (
            attendance_df["Attendance Group"].value_counts(sort=False)
            .rename_axis("Attendance Group").reset_index(name="Students")
        )
        fig = px.bar(
            group_counts, x="Attendance Group", y="Students",
            title="Students by Attendance Range",
            labels={"Attendance Group": "Attendance range", "Students": "Number of Students"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid attendance values are available for the current selection.")

st.subheader("Filtered Student Records")
display_cols = ["student_id", "name", "age", "marks", "attendance_percentage", "valid_record"]
table = filtered[display_cols].rename(columns={
    "student_id": "Student ID",
    "name": "Name",
    "age": "Age",
    "marks": "Marks",
    "attendance_percentage": "Attendance (%)",
    "valid_record": "Valid record"
})
st.dataframe(table, use_container_width=True, hide_index=True)

csv_data = table.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data (CSV)",
    data=csv_data,
    file_name="swynex_filtered_student_data.csv",
    mime="text/csv"
)

st.subheader("Key Findings")
all_valid_marks = df.loc[df["marks_valid"], "marks"]
all_valid_attendance = df.loc[df["attendance_valid"], "attendance_percentage"]
all_valid_pair = df[df["marks_valid"] & df["attendance_valid"]]

insights = []
if not all_valid_marks.empty:
    insights.append(f"Valid marks range from {all_valid_marks.min():.0f} to {all_valid_marks.max():.0f}; average valid marks are {all_valid_marks.mean():.2f}.")
if not all_valid_attendance.empty:
    insights.append(f"Average valid attendance is {all_valid_attendance.mean():.2f}%.")
invalid_marks_count = int((~df["marks_valid"]).sum())
invalid_attendance_count = int((~df["attendance_valid"]).sum())
if invalid_marks_count or invalid_attendance_count:
    insights.append(f"Data quality review: {invalid_marks_count} invalid/missing mark value(s) and {invalid_attendance_count} invalid/missing attendance value(s) were detected.")
if len(all_valid_pair) >= 3:
    overall_corr = all_valid_pair[["marks", "attendance_percentage"]].corr().iloc[0, 1]
    insights.append(f"The correlation between marks and attendance is {overall_corr:.3f} for valid paired records. Interpret this as association, not proof of cause.")
for item in insights:
    st.markdown(f"- {item}")

st.caption("Note: Invalid values are excluded from relevant KPI calculations and clearly flagged for review; the original dataset is not modified.")
