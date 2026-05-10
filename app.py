import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import datetime
import re

# --- PAGE SETUP ---
st.set_page_config(page_title="Deepa Pathak | GOC TA Hub", layout="wide", page_icon="🎯")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #e3f2fd, #ffffff); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 2px solid #4285F4; }
    h1, h2, h3 { color: #1a73e8; font-family: 'Open Sans', sans-serif; }
    .stButton>button { background-color: #4285F4; color: white; border-radius: 20px; border: none; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR GOOGLE LOGO ---
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="150">
        <p style="color: #5f6368; font-weight: bold; margin-top: 10px;">GOC Operations Hub</p>
    </div>
    """, unsafe_allow_html=True)

menu = ["AI Resume Matcher (Universal)", "TA Project Dashboard", "Sourcing Analytics (Real-time)", "Professional Profile"]
choice = st.sidebar.radio("Navigate", menu)

# Helper function to find email/phone
def extract_contact(text):
    email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    phone = re.findall(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', text)
    return (email[0] if email else "Not Found"), (phone[0] if phone else "Not Found")

# --- MODULE 1: AI RESUME MATCHER ---
if choice == "AI Resume Matcher (Universal)":
    st.header("🤖 Universal AI Resume Screening")
    st.write("Scan resumes and download the hiring report along with candidate contact details. 🤖📂📥.")
    
    col1, col2 = st.columns(2)
    with col1:
        job_role = st.text_input("Target Job Role", "Data Analyst / HR")
        jd_text = st.text_area("Paste Job Requirements (Keywords)")
    
    with col2:
        uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

    if st.button("Start AI Matching"):
        if jd_text and uploaded_files:
            target_keywords = [word.strip().lower() for word in jd_text.replace(',', ' ').split() if len(word) > 3]
            results = []
            
            for file in uploaded_files:
                reader = PdfReader(file)
                resume_text = "".join([page.extract_text().lower() for page in reader.pages])
                
                # Extracting Contact Info
                email, phone = extract_contact(resume_text)
                
                # Match calculation
                match_count = sum(1 for key in target_keywords if key in resume_text)
                score = round((match_count / len(target_keywords)) * 100, 2) if target_keywords else 0
                
                results.append({
                    "Candidate": file.name,
                    "Email": email,
                    "Phone": phone,
                    "Match Score (%)": score,
                    "Status": "Recommended" if score >= 60 else "Review Required"
                })
            
            df_results = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False)
            st.dataframe(df_results, use_container_width=True)
            
            # DOWNLOAD FEATURE
            csv = df_results.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Hiring Report (Excel/CSV)", data=csv, file_name=f"Hiring_Report_{job_role}.csv", mime='text/csv')
        else:
            st.warning("Please provide JD and Resumes.")

# --- MODULE 2: TA PROJECT DASHBOARD (DYNAMIC) ---
elif choice == "TA Project Dashboard":
    st.header("📊 TA Project Lifecycle Tracker")
    c_edit1, c_edit2 = st.columns(2)
    with c_edit1:
        s_prog = st.slider("Candidate Sourcing Progress", 0, 100, 75)
        i_prog = st.slider("Interview Coordination Progress", 0, 100, 20)
    with c_edit2:
        s_date = st.date_input("Sourcing Deadline", datetime.date(2026, 5, 25))
        i_date = st.date_input("Interview Deadline", datetime.date(2026, 6, 10))

    data = {
        "Milestones": ["Market Mapping", "Candidate Sourcing", "Interview Coordination", "Offer Management"],
        "Deadline": ["2026-05-15", s_date, i_date, "2026-06-20"],
        "Progress (%)": [100, s_prog, i_prog, 0],
        "Risk": ["Low", "Low" if s_prog > 50 else "High", "Medium" if i_prog > 15 else "High", "High"]
    }
    st.table(pd.DataFrame(data))

# --- MODULE 3: SOURCING ANALYTICS ---
elif choice == "Sourcing Analytics (Real-time)":
    st.header("📈 Sourcing Channel Efficiency")
    c1, c2, c3, c4 = st.columns(4)
    with c1: link = st.number_input("LinkedIn", value=120)
    with c2: ref = st.number_input("Referrals", value=45)
    with c3: ind = st.number_input("Indeed", value=80)
    with c4: port = st.number_input("Portal", value=60)

    source_df = pd.DataFrame({"Channel": ["LinkedIn", "Referrals", "Indeed", "Portal"], "Apps": [link, ref, ind, port]})
    st.bar_chart(source_df.set_index("Channel"))
    
    total = link + ref + ind + port
    ref_per = round((ref / total) * 100, 1) if total > 0 else 0
    st.write(f"**Referral Share:** {ref_per}%")
    if ref_per < 20: st.warning("⚠️ Action: Boost Referral Program")

# --- MODULE 4: PROFILE ---
elif choice == "Professional Profile":
    st.header("👤 Deepa Pathak")
    st.write("**MBA HRM | Data Science & AI Professional**")
    st.info("Automating Talent Acquisition with AI and Data Insights.")