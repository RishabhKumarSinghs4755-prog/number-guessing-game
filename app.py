import random
import streamlit as st

st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎯",
    layout="centered"
)

# ------------------------------------------------------------------ settings
LEVELS = {
    "Easy": (50, 10),
    "Normal": (100, 8),
    "Hard": (200, 8),
}

# dark palette
BG = "#262624"
PANEL = "#30302E"
TRACK = "#44443F"
TEXT = "#FAF9F5"
MUTED = "#B8B5A9"
ACCENT = "#D97757"
LOW = "#6AA9F0"
HIGH = "#EE7B7B"
WIN = "#5FCB9A"

# ------------------------------------------------------------------ styling
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

:root {{
    --bg:{BG}; --panel:{PANEL}; --track:{TRACK}; --text:{TEXT}; --muted:{MUTED};
    --accent:{ACCENT}; --low:{LOW}; --high:{HIGH}; --win:{WIN};
}}

html, body, [class*="css"], .stApp {{
    font-family:'DM Sans',sans-serif;
    color:var(--text);
}}

.stApp {{
    background:
        radial-gradient(800px 380px at 90% -10%, rgba(217,119,87,.14) 0%, transparent 60%),
        radial-gradient(700px 380px at -10% 5%, rgba(106,169,240,.10) 0%, transparent 55%),
        var(--bg);
}}

.stApp p, .stApp label, .stApp span {{
    color:var(--text);
}}

#MainMenu, footer, header[data-testid="stHeader"] {{
    visibility:hidden;
    height:0;
}}

.block-container {{
    max-width:640px;
    padding-top:2.5rem;
    padding-bottom:3rem;
}}

h1.title {{
    font-family:'Bricolage Grotesque',sans-serif;
    font-weight:800;
    color:var(--text);
    font-size:3.1rem;
    line-height:1.02;
    letter-spacing:-0.03em;
    margin:0 0 .4rem 0;
}}

p.sub {{
    font-size:1.05rem;
    color:var(--muted) !important;
    margin:0 0 1.6rem 0;
    max-width:46ch;
}}

/* stats */
.stats {{
    display:flex;
    margin:1.2rem 0 1.4rem 0;
}}

.stat {{
    flex:1;
    padding:0 1.1rem;
    border-left:2px solid var(--track);
}}

.stat:first-child {{
    padding-left:0;
    border-left:none;
}}

.stat .n {{
    font-family:'Bricolage Grotesque',sans-serif;
    font-weight:800;
    font-size:2.1rem;
    line-height:1;
    color:var(--text);
}}

.stat .l {{
    font-size:.85rem;
    color:var(--muted);
    margin-top:.25rem;
}}

/* range bar */
.rangewrap {{
    background:var(--panel);
    border:1px solid #3A3A37;
    border-radius:18px;
    padding:1.1rem 1.3rem 1rem 1.3rem;
    box-shadow:0 14px 34px -20px rgba(0,0,0,.8);
}}

.rangewrap .cap {{
    font-size:.92rem;
    margin-bottom:.9rem;
    color:var(--muted);
}}

.rangewrap .cap b {{
    color:var(--text);
}}

.track {{
    position:relative;
    height:14px;
    border-radius:99px;
    background:var(--track);
}}

.window {{
    position:absolute;
    top:0;
    bottom:0;
    border-radius:99px;
    background:linear-gradient(90deg,var(--low),var(--win),var(--high));
    transition:left .5s ease, width .5s ease;
}}

.tick {{
    position:absolute;
    top:-5px;
    width:4px;
    height:24px;
    border-radius:3px;
    transform:translateX(-50%);
    box-shadow:0 0 0 2px var(--panel);
}}

.ends {{
    display:flex;
    justify-content:space-between;
    font-size:.8rem;
    color:var(--muted);
    margin-top:.6rem;
}}

/* feedback */
.fb {{
    margin:1.2rem 0 .8rem 0;
    padding:.95rem 1.2rem;
    border-radius:14px;
    font-weight:700;
    font-size:1.05rem;
}}

.fb.low {{
    background:rgba(106,169,240,.14);
    color:#A4CBF7;
    border:1px solid rgba(106,169,240,.35);
}}

.fb.high {{
    background:rgba(238,123,123,.14);
    color:#F6A3A3;
    border:1px solid rgba(238,123,123,.35);
}}

.fb.win {{
    background:rgba(95,203,154,.14);
    color:#93E3BD;
    border:1px solid rgba(95,203,154,.35);
}}

.fb.lose,
.fb.info {{
    background:rgba(250,249,245,.06);
    color:var(--text);
    border:1px solid #3F3F3B;
}}

.fb.info {{
    font-weight:500;
}}

.fb small {{
    display:block;
    font-weight:500;
    opacity:.85;
    margin-top:.15rem;
}}

/* history chips */
.chips {{
    display:flex;
    flex-wrap:wrap;
    gap:.5rem;
    margin-top:.6rem;
}}

.chip {{
    background:var(--panel);
    color:var(--text);
    border-radius:99px;
    padding:.35rem .85rem;
    font-weight:700;
    font-size:.95rem;
    border:2px solid transparent;
}}

.chip.low {{
    border-color:var(--low);
}}

.chip.high {{
    border-color:var(--high);
}}

.chip.win {{
    border-color:var(--win);
    background:var(--win);
    color:#12372A;
}}

.chip span {{
    font-weight:500;
    font-size:.8rem;
    opacity:.75;
    margin-left:.35rem;
}}

/* streamlit widgets */
div[data-testid="stRadio"] label p {{
    font-weight:700;
    color:var(--text);
}}

div[data-testid="stForm"] {{
    border:none;
    padding:0;
    background:transparent;
}}

div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] div[data-baseweb="base-input"] {{
    background:var(--panel) !important;
    border-radius:14px;
    border-color:#3F3F3B;
}}

div[data-testid="stNumberInput"] input {{
    font-family:'Bricolage Grotesque',sans-serif;
    font-weight:800;
    font-size:1.6rem;
    height:3.4rem;
    color:var(--text) !important;
    background:var(--panel) !important;
    -webkit-text-fill-color:var(--text);
}}

div[data-testid="stNumberInput"] input::placeholder {{
    color:#7C7A71;
    -webkit-text-fill-color:#7C7A71;
    font-weight:500;
}}

div[data-testid="stNumberInput"] button {{
    background:var(--panel) !important;
    color:var(--muted) !important;
}}

div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {{
    border-color:var(--accent);
    box-shadow:0 0 0 1px var(--accent);
}}

.stButton > button,
div[data-testid="stFormSubmitButton"] > button {{
    width:100%;
    height:3.4rem;
    border-radius:14px;
    border:none;
    font-weight:700;
    font-size:1.05rem;
    background:var(--accent);
    color:#fff;
    transition:transform .12s ease, background .12s ease;
}}

.stButton > button p,
div[data-testid="stFormSubmitButton"] > button p {{
    color:#fff;
    font-weight:700;
}}

.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {{
    background:#C6613F;
    color:#fff;
    transform:translateY(-1px);
}}

.stButton > button:focus-visible,
div[data-testid="stFormSubmitButton"] > button:focus-visible {{
    outline:3px solid var(--low);
    outline-offset:2px;
}}

.credit {{
    margin-top:2.2rem;
    font-size:.82rem;
    color:var(--muted);
    opacity:.7;
}}

@media (max-width:520px) {{
    h1.title {{
        font-size:2.4rem;
    }}

    .stat .n {{
        font-size:1.7rem;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    .window {{
        transition:none;
    }}
}}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ game logic

def new_game():
    top, max_tries = LEVELS[st.session_state.level]

    st.session_state.update(
        top=top,
        max_tries=max_tries,
        secret=random.randint(1, top),
        lo=1,
        hi=top,
        history=[],
        status="playing",
        msg=None,
    )


def closeness(guess):
    gap = abs(guess - st.session_state.secret) / st.session_state.top

    if gap <= 0.05:
        return "Very close"

    if gap <= 0.15:
        return "Getting warm"

    if gap <= 0.30:
        return "Cool"

    return "Far away"


def submit_guess():
    s = st.session_state
    guess = s.get("guess_input")

    if guess is None:
        s.msg = (
            "info",
            "Type a number first.",
            f"Pick anything from 1 to {s.top}."
        )
        return

    guess = int(guess)

    if any(g == guess for g, _ in s.history):
        s.msg = (
            "info",
            f"You already tried {guess}.",
            "Pick a number you haven't used."
        )
        return

    if guess == s.secret:
        s.history.append((guess, "win"))
        s.status = "won"

        best = s.best.get(s.level)
        tries = len(s.history)

        if best is None or tries < best:
            s.best[s.level] = tries

        s.msg = (
            "win",
            f"Correct! It was {s.secret}.",
            f"You got it in {tries} "
            f"{'attempt' if tries == 1 else 'attempts'}.",
        )

        s.celebrate = True
        return

    if guess < s.secret:
        s.history.append((guess, "low"))
        s.lo = max(s.lo, guess + 1)

        s.msg = (
            "low",
            f"{guess} is too low. Go higher.",
            closeness(guess)
        )

    else:
        s.history.append((guess, "high"))
        s.hi = min(s.hi, guess - 1)

        s.msg = (
            "high",
            f"{guess} is too high. Go lower.",
            closeness(guess)
        )

    if len(s.history) >= s.max_tries:
        s.status = "lost"

        s.msg = (
            "lose",
            f"Out of attempts. The number was {s.secret}.",
            "Start a new game to try again."
        )


def range_bar():
    s = st.session_state

    span = max(s.top - 1, 1)

    left = (s.lo - 1) / span * 100
    width = max((s.hi - s.lo) / span * 100, 1.5)

    ticks = ""

    for g, kind in s.history:
        color = {
            "low": LOW,
            "high": HIGH,
            "win": WIN
        }[kind]

        ticks += (
            f'<div class="tick" '
            f'style="left:{(g - 1) / span * 100}%;'
            f'background:{color}"></div>'
        )

    caption = (
        f"The number is between <b>{s.lo}</b> and <b>{s.hi}</b>"
        if s.status == "playing"
        else f"The number was <b>{s.secret}</b>"
    )

    st.markdown(
        f"""
<div class="rangewrap">
  <div class="cap">{caption}</div>
  <div class="track">
    <div class="window" style="left:{left}%;width:{width}%"></div>
    {ticks}
  </div>
  <div class="ends">
    <span>1</span>
    <span>{s.top}</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------ state

if "best" not in st.session_state:
    st.session_state.best = {}

if "level" not in st.session_state:
    st.session_state.level = "Normal"

if "secret" not in st.session_state:
    new_game()


s = st.session_state


# ------------------------------------------------------------------ page

st.markdown(
    '<h1 class="title">Guess the number.</h1>',
    unsafe_allow_html=True
)

st.markdown(
    f'<p class="sub">I picked a secret number from 1 to {s.top}. '
    f"You have {s.max_tries} attempts to find it.</p>",
    unsafe_allow_html=True,
)


st.radio(
    "Difficulty",
    list(LEVELS),
    key="level",
    horizontal=True,
    on_change=new_game,
    label_visibility="collapsed",
)


best = s.best.get(s.level)

st.markdown(
    f"""
<div class="stats">
  <div class="stat">
    <div class="n">{len(s.history)}</div>
    <div class="l">guesses made</div>
  </div>

  <div class="stat">
    <div class="n">{best if best else "-"}</div>
    <div class="l">best on {s.level}</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


range_bar()


if s.msg:
    kind, head, detail = s.msg

    st.markdown(
        f'<div class="fb {kind}">{head}'
        f'<small>{detail}</small></div>',
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        '<div class="fb info">Make your first guess below.'
        '<small>Each answer narrows the range above.</small></div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------ input
# Enter key + Guess button both submit the guess

if s.status == "playing":

    with st.form(
        "guess_form",
        clear_on_submit=True,
        enter_to_submit=True
    ):

        c1, c2 = st.columns([2, 1])

        with c1:
            st.number_input(
                "Your guess",
                min_value=1,
                max_value=s.top,
                value=None,
                step=1,
                placeholder=f"1 to {s.top}",
                key="guess_input",
                label_visibility="collapsed",
            )

        with c2:
            st.form_submit_button(
                "Guess",
                on_click=submit_guess
            )

else:

    st.button(
        "Play again",
        on_click=new_game
    )

    if s.pop("celebrate", False):
        st.balloons()


# ------------------------------------------------------------------ history

if s.history:

    labels = {
        "low": "low",
        "high": "high",
        "win": "correct"
    }

    chips = "".join(
        f'<div class="chip {k}">'
        f'{g}<span>{labels[k]}</span>'
        f'</div>'
        for g, k in s.history
    )

    st.markdown(
        f'<div class="chips">{chips}</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------------ new game

if s.status == "playing" and s.history:

    st.button(
        "New game",
        on_click=new_game,
        key="restart"
    )


st.markdown(
    '<div class="credit">Built with Python and Streamlit</div>',
    unsafe_allow_html=True
)