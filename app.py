import streamlit as st
import json
from pathlib import Path

# --- Config ---
st.set_page_config(page_title="PyChallenge", layout="centered", page_icon="🐍")

# --- Load Data ---
DATA_PATH = Path("data/sample_quizzes.json")
with open(DATA_PATH) as f:
    quizzes = json.load(f)

# --- State ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

# --- Sidebar Navigation ---
menu = st.sidebar.radio("📚 Navigate", ["🏠 Home", "🧩 Play Quiz", "✏️ Create Quiz", "🏆 Leaderboard"])

# --- Home Page ---
if menu == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🐍 PyChallenge</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; font-size:18px'>
    Test your Python knowledge with fun, interactive challenges!  
    Choose a quiz, answer questions, and see how you rank.
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.info("Navigate to **Play Quiz** on the sidebar to begin!")

# --- Play Quiz Page ---
elif menu == "🧩 Play Quiz":
    quiz_titles = [q["title"] for q in quizzes]
    selected_title = st.selectbox("Choose a Quiz:", quiz_titles)
    quiz = next(q for q in quizzes if q["title"] == selected_title)

    st.markdown(f"### 🎯 {selected_title}")
    st.caption("Answer the following questions:")

    st.session_state.quiz_completed = False

    for i, q in enumerate(quiz["questions"]):
        st.write(f"**Q{i+1}.** {q['question']}")
        answer = st.radio("Select an option:", q["options"], key=f"ans{i}")
        if st.button(f"Submit Q{i+1}", key=f"submit{i}"):
            if answer == q["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error("❌ Incorrect.")
                with st.expander("💡 Show Hint"):
                    st.info(q["hint"])
        st.divider()

    if st.button("Finish Quiz"):
        st.session_state.quiz_completed = True
        st.markdown(f"### 🧮 Your Score: {st.session_state.score} / {len(quiz['questions'])}")
        if st.session_state.score == len(quiz["questions"]):
            st.balloons()
            st.success("Perfect Score! 🎉")
        st.button("Reset Score", on_click=lambda: st.session_state.update(score=0))

# --- Create Quiz Page ---
elif menu == "✏️ Create Quiz":
    st.header("🧩 Create a New Quiz")
    st.info("Add questions and test them locally. Save feature coming soon.")
    title = st.text_input("Quiz Title")
    if "new_quiz" not in st.session_state:
        st.session_state.new_quiz = []
    if st.button("➕ Add Question"):
        st.session_state.new_quiz.append({"question": "", "options": [], "answer": ""})

    for i, q in enumerate(st.session_state.new_quiz):
        q["question"] = st.text_input(f"Question {i+1}", key=f"new_q{i}")
        opts = st.text_area(f"Options (comma separated)", key=f"opts{i}")
        q["options"] = [x.strip() for x in opts.split(",") if x]
        q["answer"] = st.text_input(f"Correct Answer", key=f"ans{i}")

    if st.button("💾 Save Quiz (local demo)"):
        st.success("Quiz saved temporarily (not written to file yet).")

# --- Leaderboard Page ---
elif menu == "🏆 Leaderboard":
    st.header("🏆 Leaderboard (Local Prototype)")
    st.info("Leaderboard tracking will be added later.")

