import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# --- LOGIN ---
def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if username == "christmbassybremen" and password == "CEde2025":
        return True
    elif username or password:
        st.sidebar.warning("❌ Invalid credentials. Try again.")
    return False

# --- MAIN DASHBOARD ---
def run_dashboard():
    st.title("📊 Christ Embassy Attendance Dashboard")
    uploaded_file = st.file_uploader("📁 Upload Attendance CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        # Format key columns
        df['Reporting For (Date)'] = pd.to_datetime(df['Reporting For (Date)'], errors='coerce')
        df['Church'] = df['Church'].str.strip()

        attendance_cols = ['Men- Total', 'Women- Total', 'Youth- Total', 'Children- Total', 'Total Attendance']
        for col in attendance_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Sidebar filters
        st.sidebar.header("📌 Filters")
        church_options = ["All"] + sorted(df['Church'].dropna().unique().tolist())
        selected_church = st.sidebar.selectbox("🏠 Select Church", options=church_options)

        date_options = ["All"] + sorted(df['Reporting For (Date)'].dropna().dt.strftime("%Y-%m-%d").unique().tolist())
        selected_date = st.sidebar.selectbox("📅 Select Reporting Date", options=date_options)

        # Apply filters
        filtered_df = df.copy()
        if selected_church != "All":
            filtered_df = filtered_df[filtered_df['Church'] == selected_church]
        if selected_date != "All":
            date_obj = pd.to_datetime(selected_date)
            filtered_df = filtered_df[filtered_df['Reporting For (Date)'] == date_obj]

        # Summary section
        st.caption(f"🗓️ File uploaded: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.subheader("🔢 Summary Statistics")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("🧍 Men", int(filtered_df['Men- Total'].sum()))
        col2.metric("👩 Women", int(filtered_df['Women- Total'].sum()))
        col3.metric("🧒 Youth", int(filtered_df['Youth- Total'].sum()))
        col4.metric("🧸 Children", int(filtered_df['Children- Total'].sum()))
        col5.metric("👥 Total Attendance", int(filtered_df['Total Attendance'].sum()))

        # Visuals
        st.subheader("📈 Visual Analysis")

        # Bar Chart: Attendance by Church
        st.markdown("#### 🏠 Attendance by Church")
        church_summary = filtered_df.groupby('Church')['Total Attendance'].sum().sort_values(ascending=False)
        if not church_summary.empty:
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            sns.barplot(x=church_summary.values, y=church_summary.index, ax=ax1)
            ax1.set_xlabel("Total Attendance")
            ax1.set_ylabel("Church")
            st.pyplot(fig1)
        else:
            st.info("No data to show for selected filters.")

        # Pie Chart: Gender distribution
        st.markdown("#### 🧑‍🤝‍🧑 Gender & Age Group Distribution")
        pie_data = {
            "Men": filtered_df['Men- Total'].sum(),
            "Women": filtered_df['Women- Total'].sum(),
            "Youth": filtered_df['Youth- Total'].sum(),
            "Children": filtered_df['Children- Total'].sum()
        }
        fig2, ax2 = plt.subplots()
        ax2.pie(pie_data.values(), labels=pie_data.keys(), autopct='%1.1f%%', startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)

        # Line Chart: Attendance trend over time
        st.markdown("#### 📊 Attendance Over Time")
        trend_data = filtered_df.groupby('Reporting For (Date)')['Total Attendance'].sum().reset_index()
        if not trend_data.empty:
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=trend_data, x='Reporting For (Date)', y='Total Attendance', marker='o', ax=ax3)
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Attendance")
            ax3.set_title("Total Attendance Over Time")
            plt.xticks(rotation=45)
            st.pyplot(fig3)
        else:
            st.info("No trend data available for current filters.")

    else:
        st.info("⬆️ Please upload a CSV file to begin.")

# --- RUN APP ---
if login():
    run_dashboard()
else:
    st.stop()
