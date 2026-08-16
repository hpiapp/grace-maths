"""Streamlit app for practising prime numbers and cubes."""

from __future__ import annotations

import html
import time

import streamlit as st

from quiz_logic import Question, average, check_answer, make_quiz


st.set_page_config(
    page_title="Prime & Cube Rockstars",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

      :root {
        --ink: #172033;
        --purple: #6c4cff;
        --purple-dark: #5035d7;
        --lime: #c9ff4a;
        --paper: #f7f5ff;
      }
      .stApp {
        background:
          radial-gradient(circle at 15% 10%, rgba(201,255,74,.25), transparent 24rem),
          radial-gradient(circle at 90% 18%, rgba(108,76,255,.18), transparent 28rem),
          #f8f7fc;
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
      }
      .block-container { max-width: 760px; padding-top: 2rem; padding-bottom: 3rem; }
      h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.03em; }
      .hero {
        background: linear-gradient(135deg, #171c32 0%, #3a287f 100%);
        border-radius: 28px;
        padding: 2rem 2.2rem;
        color: white;
        margin-bottom: 1.35rem;
        box-shadow: 0 18px 50px rgba(43, 29, 105, .2);
        position: relative;
        overflow: hidden;
      }
      .hero:after {
        content: '³'; position: absolute; right: 1rem; top: -2.4rem;
        font: 700 12rem 'Space Grotesk'; color: rgba(255,255,255,.06);
      }
      .eyebrow { color: var(--lime); font-weight: 800; text-transform: uppercase; letter-spacing: .14em; font-size: .78rem; }
      .hero h1 { color: white !important; margin: .3rem 0 .4rem; font-size: clamp(2rem, 7vw, 3.5rem); line-height: 1; }
      .hero p { color: rgba(255,255,255,.78); margin: 0; max-width: 34rem; }
      .question-card {
        background: white; border: 1px solid rgba(64,44,135,.1); border-radius: 24px;
        padding: 2rem; text-align: center; box-shadow: 0 14px 40px rgba(44,32,92,.09);
        margin: 1rem 0;
      }
      .question-type {
        display: inline-block; padding: .34rem .72rem; border-radius: 999px;
        background: #efeaff; color: var(--purple-dark); font-weight: 800; font-size: .78rem;
        letter-spacing: .06em; text-transform: uppercase;
      }
      .question-card h2 { font-size: clamp(1.65rem, 5vw, 2.4rem); margin: 1.1rem auto .55rem; color: var(--ink); }
      .hint { color: #687087; font-size: .92rem; }
      .progress-copy { color: #626a7e; font-weight: 700; font-size: .9rem; }
      .feedback {
        border-radius: 18px; padding: 1rem 1.15rem; margin: .8rem 0 1rem; font-weight: 700;
      }
      .feedback.good { background: #eaffbe; color: #315309; border: 1px solid #c7ef74; }
      .feedback.try { background: #fff0ef; color: #8a2d2a; border: 1px solid #ffc6c2; }
      .stButton > button, .stFormSubmitButton > button {
        border-radius: 12px; min-height: 3rem; font-weight: 800; border: 0;
      }
      .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: var(--purple); color: white; box-shadow: 0 8px 20px rgba(108,76,255,.22);
      }
      .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
        background: var(--purple-dark); color: white;
      }
      div[data-testid="stMetric"] {
        background: white; border: 1px solid #e9e5f5; border-radius: 16px; padding: .8rem 1rem;
      }
      div[data-testid="stMetricValue"] { font-family: 'Space Grotesk'; }
      .footer-note { text-align: center; color: #8a8fa0; font-size: .8rem; margin-top: 2rem; }
      @media (max-width: 600px) {
        .block-container { padding: 1rem 1rem 2rem; }
        .hero, .question-card { border-radius: 20px; padding: 1.4rem; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialise_state() -> None:
    defaults = {
        "screen": "setup",
        "quiz": [],
        "question_index": 0,
        "results": [],
        "question_started": None,
        "answered": False,
        "last_result": None,
        "streak": 0,
        "best_streak": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_quiz(mode: str, question_count: int) -> None:
    st.session_state.quiz = make_quiz(mode, question_count)
    st.session_state.question_index = 0
    st.session_state.results = []
    st.session_state.answered = False
    st.session_state.last_result = None
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.question_started = time.perf_counter()
    st.session_state.screen = "quiz"


def reset_quiz() -> None:
    st.session_state.screen = "setup"
    st.session_state.quiz = []
    st.session_state.results = []
    st.session_state.question_started = None
    st.session_state.answered = False


def render_header(subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">⚡ Number training</div>
          <h1>Prime & Cube<br>Rockstars</h1>
          <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_setup() -> None:
    render_header("Fast questions, instant feedback, and a race against your own best time.")

    st.subheader("Set up a practice session")
    with st.form("setup_form"):
        mode = st.segmented_control(
            "Choose a challenge",
            ["Mixed", "Prime numbers", "Cube numbers"],
            default="Mixed",
        )
        question_count = st.select_slider(
            "Number of questions",
            options=[5, 10, 15, 20],
            value=10,
        )
        submitted = st.form_submit_button("Start rocking  →", type="primary", use_container_width=True)

    if submitted:
        start_quiz(mode or "Mixed", question_count)
        st.rerun()

    with st.expander("How it works"):
        st.markdown(
            """
            - **Prime questions:** type every prime in the range. Commas, spaces, or “and” all work.
            - **Cube questions:** type the value of the cube, from 1³ to 12³.
            - The clock starts when each question appears and stops when the answer is submitted.
            - Ranges are **inclusive**, so both end numbers count if they are prime.
            """
        )


def record_answer(question: Question, raw_answer: str) -> None:
    elapsed = max(0.0, time.perf_counter() - st.session_state.question_started)
    is_correct = check_answer(question, raw_answer)

    if is_correct:
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
    else:
        st.session_state.streak = 0

    result = {
        "question": question.prompt,
        "kind": question.kind,
        "given": raw_answer.strip() or "—",
        "answer": question.display_answer,
        "correct": is_correct,
        "seconds": elapsed,
    }
    st.session_state.results.append(result)
    st.session_state.last_result = result
    st.session_state.answered = True


def next_question() -> None:
    if st.session_state.question_index + 1 >= len(st.session_state.quiz):
        st.session_state.screen = "results"
    else:
        st.session_state.question_index += 1
        st.session_state.answered = False
        st.session_state.last_result = None
        st.session_state.question_started = time.perf_counter()


def render_quiz() -> None:
    total = len(st.session_state.quiz)
    index = st.session_state.question_index
    question: Question = st.session_state.quiz[index]

    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.markdown(f'<div class="progress-copy">QUESTION {index + 1} OF {total}</div>', unsafe_allow_html=True)
    with top_right:
        st.markdown(
            f'<div class="progress-copy" style="text-align:right">🔥 {st.session_state.streak} streak</div>',
            unsafe_allow_html=True,
        )
    st.progress((index + 1) / total)

    label = "Prime finder" if question.kind == "prime" else "Cube power"
    st.markdown(
        f"""
        <div class="question-card">
          <span class="question-type">{label}</span>
          <h2>{html.escape(question.prompt)}</h2>
          <div class="hint">{html.escape(question.hint)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.answered:
        with st.form(f"answer_form_{index}", clear_on_submit=False):
            answer = st.text_input(
                "Your answer",
                placeholder="Type your answer here…",
                autocomplete="off",
            )
            submitted = st.form_submit_button("Lock it in", type="primary", use_container_width=True)

        if submitted:
            if not answer.strip():
                st.warning("Type an answer before locking it in.")
            else:
                record_answer(question, answer)
                st.rerun()
    else:
        result = st.session_state.last_result
        if result["correct"]:
            st.markdown(
                f'<div class="feedback good">✓ Correct! You nailed it in {result["seconds"]:.1f} seconds.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="feedback try">Not this time. The answer is <strong>{html.escape(result["answer"])}</strong>.</div>',
                unsafe_allow_html=True,
            )

        button_text = "See my results  →" if index + 1 == total else "Next question  →"
        if st.button(button_text, type="primary", use_container_width=True):
            next_question()
            st.rerun()

    if st.button("Quit practice", type="tertiary"):
        reset_quiz()
        st.rerun()


def render_results() -> None:
    results = st.session_state.results
    correct = sum(result["correct"] for result in results)
    total = len(results)
    accuracy = round(100 * correct / total) if total else 0
    average_time = average(result["seconds"] for result in results)

    if accuracy == 100:
        subtitle = "A perfect set. That was seriously sharp."
        st.balloons()
    elif accuracy >= 80:
        subtitle = "Brilliant work—your number knowledge is getting fast."
    elif accuracy >= 60:
        subtitle = "Good session. Every round makes the tricky ones easier."
    else:
        subtitle = "Nice effort. Have another go and beat this score."

    render_header(subtitle)
    st.subheader("Session complete")
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", f"{correct}/{total}")
    col2.metric("Accuracy", f"{accuracy}%")
    col3.metric("Avg. time", f"{average_time:.1f}s")
    st.caption(f"Best streak: 🔥 {st.session_state.best_streak}")

    if st.button("Play again", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()

    with st.expander("Review every answer", expanded=accuracy < 100):
        for number, result in enumerate(results, start=1):
            icon = "✅" if result["correct"] else "❌"
            st.markdown(f"**{icon} {number}. {result['question']}**  ·  {result['seconds']:.1f}s")
            if result["correct"]:
                st.caption(f"Your answer: {result['given']}")
            else:
                st.caption(f"Your answer: {result['given']}  |  Correct answer: {result['answer']}")


initialise_state()

if st.session_state.screen == "setup":
    render_setup()
elif st.session_state.screen == "quiz":
    render_quiz()
else:
    render_results()

st.markdown('<div class="footer-note">Built for brave brains who like a challenge.</div>', unsafe_allow_html=True)
