import os
import ssl
import time
import threading
import tempfile
import smtplib

import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime, timedelta
from email.message import EmailMessage

from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


 
# PAGE CONFIG

st.set_page_config(page_title="AI Water Tracker", layout="wide")



# HELPERS

def generate_pdf_report(user_data: dict) -> str:
    """Generate a simple PDF report and return the path."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("AI Water Tracker Health Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.5 * inch))

    for key, value in user_data.items():
        elements.append(Paragraph(f"<b>{key}:</b> {value}", styles["Normal"]))
        elements.append(Spacer(1, 0.25 * inch))

    doc.build(elements)
    return temp_file.name


def calculate_streak(history, recommended_water: float) -> int:
    """
    Streak = consecutive days (ending today) where daily total >= recommended_water.
    history items expected like: [(intake_ml, "YYYY-MM-DD"), ...]
    """
    if not history:
        return 0

    daily_totals = {}
    for intake, date_str in history:
        daily_totals[date_str] = daily_totals.get(date_str, 0) + intake

    streak = 0
    day = datetime.today()

    while True:
        day_str = day.strftime("%Y-%m-%d")
        if daily_totals.get(day_str, 0) >= recommended_water:
            streak += 1
            day -= timedelta(days=1)
        else:
            break

    return streak


def get_level_from_streak(streak: int) -> str:
    if streak <= 0:
        return "Beginner 💧"
    if streak < 3:
        return "Getting Started 🚀"
    if streak < 7:
        return "Consistent Performer 💪"
    if streak < 14:
        return "Hydration Warrior 🔥"
    return "Hydration Master 👑"


def send_email_reminder(to_email: str, remaining_ml: float, percent: float) -> tuple[bool, str]:
    """
    Sends an email reminder using Gmail SMTP.
    Requires .env:
      GMAIL_USER=yourgmail@gmail.com
      GMAIL_APP_PASSWORD=your_16_char_app_password
    """
    gmail_user = os.getenv("GMAIL_USER", "").strip()
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "").strip()

    if not gmail_user or not gmail_pass:
        return False, "Email credentials not found in .env file (GMAIL_USER / GMAIL_APP_PASSWORD)."

    try:
        msg = EmailMessage()
        msg["Subject"] = "💧 Hydration Reminder"
        msg["From"] = gmail_user
        msg["To"] = to_email

        msg.set_content(
            f"Hi!\n\n"
            f"Time to drink water 💦\n"
            f"Today's progress: {percent*100:.1f}%\n"
            f"Remaining water: {max(0, int(remaining_ml))} ml\n\n"
            f"Stay hydrated!\n"
        )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)

        return True, "Reminder email sent ✅"

    except Exception as e:
        return False, f"Email Error: {e}"


def start_hourly_reminder(email: str, remaining_ml: float, percent: float):
    """
    Background thread inside Streamlit process.
    It will run while your Streamlit server is running.
    """
    def loop():
        while st.session_state.get("reminder_running", False):
            ok, msg = send_email_reminder(email, remaining_ml, percent)
            # store last status for UI
            st.session_state["last_email_status"] = msg
            time.sleep(3600)  # 1 hour

    t = threading.Thread(target=loop, daemon=True)
    t.start()
    st.session_state["reminder_thread"] = t


 
# SIDEBAR: USER DETAILS

st.sidebar.header("Your Details")

age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=23)
gender = st.sidebar.selectbox("Gender", ["Female", "Male"])

height_unit = st.sidebar.radio("Height Unit", ["cm", "ft"])
if height_unit == "cm":
    height_cm = st.sidebar.number_input("Height (cm)", min_value=50.0, value=170.0)
else:
    height_ft = st.sidebar.number_input("Height (ft)", min_value=1.0, value=5.5)
    height_cm = height_ft * 30.48

weight = st.sidebar.number_input("Weight (kg)", min_value=10.0, value=70.0)

# BMI
height_m = height_cm / 100
bmi = weight / (height_m ** 2)

if bmi < 18.5:
    category = "Underweight"
elif 18.5 <= bmi < 24.9:
    category = "Normal Weight"
elif 25 <= bmi < 29.9:
    category = "Overweight"
else:
    category = "Obese"

st.sidebar.write(f"### Your BMI: {bmi:.2f}")
st.sidebar.write(f"Category: **{category}**")

# Water recommendation
recommended_water = weight * 35  # ml
if gender == "Male":
    recommended_water += 300

st.sidebar.write(f"Recommended Water: **{recommended_water:.0f} ml**")

 
# SIDEBAR: LOG WATER

st.sidebar.header("Log Water Intake")

user_id = st.sidebar.text_input("User ID", value="manali")
intake_ml = st.sidebar.number_input("Water Intake (ml)", min_value=0, step=100)

if st.sidebar.button("Submit"):
    if user_id and intake_ml > 0:
        log_intake(user_id, intake_ml)
        st.sidebar.success(f"Logged {intake_ml} ml ✅")

        agent = WaterIntakeAgent()
        advice = agent.analyze_intake(intake_ml)
        st.sidebar.info(f"🤖 AI Advice: {advice}")
    else:
        st.sidebar.warning("Please enter valid User ID and water amount.")


 
# MAIN TITLE
 
st.title("💧 AI Water Tracker Dashboard")
st.markdown("---")



# HISTORY SECTION

st.header("📋 Water Intake History")

history = get_intake_history(user_id) if user_id else []

if history:
    # Build dataframe
    dates = [datetime.strptime(row[1], "%Y-%m-%d") for row in history]
    values = [row[0] for row in history]

    df = pd.DataFrame({"Date": dates, "Water Intake (ml)": values})

    st.dataframe(df, use_container_width=True)
    st.line_chart(df, x="Date", y="Water Intake (ml)")

    # Today's total
    today_str = datetime.today().strftime("%Y-%m-%d")
    today_total = sum(row[0] for row in history if row[1] == today_str)

    percent = min(today_total / recommended_water, 1.0) if recommended_water > 0 else 0
    remaining = max(0, recommended_water - today_total)

    # Daily progress
    st.markdown("## 🎯 Daily Progress")
    st.progress(percent)
    st.write(f"**{percent*100:.1f}%** of daily goal completed")
    st.markdown(f"### 💧 Remaining Water Today: **{int(remaining)} ml**")

    # Weekly average (using df mean)
    weekly_avg = df["Water Intake (ml)"].mean()
    st.markdown(f"## 📊 Weekly Hydration Average: **{weekly_avg:.0f} ml**")

    # Health Insight (BMI-based)
    st.markdown("## 🧠 Health Insight")
    if category == "Underweight":
        st.warning("You may need balanced nutrition along with proper hydration.")
    elif category == "Normal Weight":
        st.success("Your BMI is healthy. Maintain hydration daily.")
    elif category == "Overweight":
        st.warning("Proper hydration helps metabolism and weight control.")
    else:
        st.error("Consider improving lifestyle and hydration habits.")

    # 
    # STREAK SYSTEM
    # 
    streak = calculate_streak(history, recommended_water)

    st.markdown("## 🔥 Hydration Streak")
    if streak == 0:
        st.info("Start your hydration streak today 💧")
    elif streak < 3:
        st.success(f"**{streak}** day streak! Keep going 💪")
    elif streak < 7:
        st.success(f"**{streak}** day streak! You're building consistency 🔥")
    else:
        st.success(f"**{streak}** day streak! Hydration Pro 🏆")

    # 
    # GAMIFICATION / LEVEL
    # 
    st.markdown("## 🏆 Hydration Level")
    level = get_level_from_streak(streak)
    st.markdown(f"### {level}")

    # Progress to next level (target = 7 days)
    next_target = 7
    progress_to_next = min(streak / next_target, 1.0)
    st.progress(progress_to_next)
    st.write(f"{progress_to_next*100:.0f}% towards **Hydration Warrior 🔥**")

    
    # CALENDAR HEATMAP
     
    st.markdown("## 📅 Hydration Calendar Heatmap")

    df2 = df.copy()
    df2["DateOnly"] = df2["Date"].dt.date
    daily = df2.groupby("DateOnly")["Water Intake (ml)"].sum().reset_index()
    daily["DateOnly"] = pd.to_datetime(daily["DateOnly"])
    daily["Day"] = daily["DateOnly"].dt.day
    daily["Month"] = daily["DateOnly"].dt.month

    fig = px.density_heatmap(
        daily,
        x="Day",
        y="Month",
        z="Water Intake (ml)",
        color_continuous_scale="Blues",
        title="Monthly Hydration Heatmap",
    )
    st.plotly_chart(fig, use_container_width=True)

    
    # HYDRATION REMINDER (OPTIONAL) - MAIN AREA
    
    st.markdown("---")
    st.markdown("# 📩 Hydration Reminder (Optional)")
    st.caption("Enter your Gmail to receive reminders. If you leave it empty, no emails will be sent.")

    if "reminder_running" not in st.session_state:
        st.session_state["reminder_running"] = False
    if "last_email_status" not in st.session_state:
        st.session_state["last_email_status"] = ""

    reminder_email = st.text_input("Enter your Gmail (optional)", value="")

    colA, colB = st.columns(2)

    with colA:
        if st.button("Start Hydration Reminder"):
            if reminder_email.strip() == "":
                st.warning("Please enter an email (or keep it empty if you don't want reminders).")
            else:
                # Send immediately once (first entry)
                ok, msg = send_email_reminder(reminder_email.strip(), remaining, percent)
                if ok:
                    st.success("First reminder sent ✅ (next reminders every 1 hour)")
                else:
                    st.error(msg)

                # Start hourly loop
                st.session_state["reminder_running"] = True
                start_hourly_reminder(reminder_email.strip(), remaining, percent)

    with colB:
        if st.button("Stop Reminder"):
            st.session_state["reminder_running"] = False
            st.success("Reminder stopped ✅")

    if st.session_state["last_email_status"]:
        st.info(st.session_state["last_email_status"])

    
    # PDF EXPORT (AFTER REMINDER)
    
    st.markdown("---")
    st.markdown("## 📄 PDF Health Report Export")

    report_data = {
        "Age": age,
        "Gender": gender,
        "Height (cm)": round(height_cm, 2),
        "Weight (kg)": weight,
        "BMI": round(bmi, 2),
        "Category": category,
        "Recommended Water (ml)": round(recommended_water, 0),
        "Today's Intake (ml)": today_total,
        "Remaining Today (ml)": int(remaining),
        "Goal Completion (%)": f"{percent*100:.1f}%",
        "Weekly Average (ml)": round(weekly_avg, 0),
        "Hydration Streak (days)": streak,
        "Hydration Level": level,
    }

    pdf_path = generate_pdf_report(report_data)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Download Health Report",
            data=f,
            file_name="water_health_report.pdf",
            mime="application/pdf",
        )

else:
    st.warning("No water intake data found. Please log water from the sidebar first.")