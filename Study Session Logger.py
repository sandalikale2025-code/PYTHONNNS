import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Study Session Logger",
    page_icon="📘",
    layout="centered"
)

# ---------- CUSTOM STYLING ----------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .card {
            padding: 1.2rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- TITLE ----------
st.title("📘 Study Session Logger")
st.caption("Log your study sessions and get a simple revision suggestion.")

st.divider()

# ---------- SESSION STATE ----------
if "sessions" not in st.session_state:
    st.session_state.sessions = []

# ---------- INPUT CARD ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📝 Log a Study Session")

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject", placeholder="e.g. Economics")
    duration = st.number_input("Minutes studied", min_value=1, step=1)

with col2:
    topic = st.text_input("Topic", placeholder="e.g. Elasticity")
    focus = st.slider("Focus level", 1, 5)

fatigue = st.radio(
    "Did you feel tired after studying?",
    ["No", "Yes"],
    horizontal=True
) == "Yes"

st.markdown("</div>", unsafe_allow_html=True)

# ---------- LOG BUTTON ----------
if st.button("📌 Log Session", use_container_width=True):

    session = {
        "subject": subject,
        "topic": topic,
        "duration": duration,
        "focus": focus,
        "fatigue": fatigue
    }

    st.session_state.sessions.append(session)

    # ---- NEXT STUDY LOGIC ----
    if focus <= 2:
        next_study = "Tomorrow"
    elif focus == 3:
        next_study = "In 2 days"
    elif focus == 4:
        next_study = "In 3 days"
    else:
        next_study = "In 7 days"

    # ---- FEEDBACK ----
    st.markdown("### 📊 Session Feedback")

    if focus >= 4 and not fatigue:
        st.success("Great session! You were focused and energetic.")
    elif fatigue:
        st.warning("You seem tired. Consider resting before your next session.")
    else:
        st.info("Decent effort. Try improving focus next time.")

    st.markdown(
        f"📅 **Recommended next study time:** `{next_study}`"
    )

# ---------- SESSION HISTORY ----------
st.divider()
st.subheader("📚 Study History")

if st.session_state.sessions:
    for i, s in enumerate(st.session_state.sessions, 1):
        st.markdown(
            f"""
            <div class="card">
            <b>Session {i}</b><br>
            📘 <b>{s['subject']}</b> – {s['topic']}<br>
            ⏱ {s['duration']} minutes<br>
            🎯 Focus level: {s['focus']}<br>
            😴 Fatigue: {"Yes" if s['fatigue'] else "No"}
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No study sessions logged yet.")
