import streamlit as st
import random

st.set_page_config(page_title="💱 Cross Currency Game", layout="centered")

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(135deg, #1a237e 0%, #8B0000 100%);
        color: #ffffff !important;
        text-align: center;
    }

    h1 {
        color: #14213d !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }

    .stButton>button {
            background-color: #8B0000;      /* 🔴 solid maroon */
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.7rem 1.4rem;
            font-size: 1.1rem;
            font-weight: 600;
            transition: 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }
    .stButton>button:hover {
        background: #1a237e;
        transform: scale(1.05);
    }

    .soal-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 18px;
        border: 3px solid #1a237e;
        box-shadow: 0 0 12px rgba(255,255,255,0.15);
        text-align: center;
        margin-top: 1.2rem;
    }

    .kurs-box {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin: 1rem 0;
    }

    .kurs-item {
        background-color: rgba(255,255,255,0.2);
        padding: 1rem 2rem;
        border-radius: 14px;
        font-size: 1.4rem;
        font-weight: 600;
        min-width: 220px;
        box-shadow: 0 0 8px rgba(255,255,255,0.15);
    }

    .soal-box p {
        font-size: 1.4rem !important;
        line-height: 2rem !important;
    }

    .stNumberInput input {
        border-radius: 10px;
        font-size: 2.3rem;
        text-align: center;
    }

    .result-box {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-top: 1.2rem;
        padding: 1.2rem;
        border-radius: 18px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
        animation: fadeIn 0.4s ease-in;
    }

    .success-box {
        background-color: #2e7d32;
        color: #e8f5e9;
        border: 3px solid #81c784;
    }

    .error-box {
        background-color: #b71c1c;
        color: #ffebee;
        border: 3px solid #ef9a9a;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: scale(0.9);}
        to {opacity: 1; transform: scale(1);}
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ======================
# JUDUL
# ======================
st.title("Mission: Cross Possible")
#st.markdown("##“Misi menaklukkan kurs silang — cepat hitung, jangan ngarang! 🏆💹”")
st.markdown("<h4>Misi menaklukkan kurs silang, cepat hitung, jangan ngarang! 🏆</h4>", unsafe_allow_html=True)
# ======================
# LOGIKA DASAR
# ======================
def make_anchor_rates():
    return {
        "USDJPY": random.randint(130, 170),
        "USDIDR": random.randint(15000, 17000),
        "JPYIDR": random.randint(90, 110),
    }

def calc_cross(target, known1, known2, rates):
    s = {known1, known2}
    if s == {"USDJPY", "JPYIDR"} and target == "USDIDR":
        return rates["USDJPY"] * rates["JPYIDR"]
    if s == {"USDIDR", "JPYIDR"} and target == "USDJPY":
        return rates["USDIDR"] // rates["JPYIDR"]
    if s == {"USDJPY", "USDIDR"} and target == "JPYIDR":
        return rates["USDIDR"] // rates["USDJPY"]
    return None

def fmt(pair): return f"{pair[:3]}/{pair[3:]}"

def new_question():
    rates = make_anchor_rates()
    combos = [["USDJPY", "JPYIDR", "USDIDR"], ["USDIDR", "JPYIDR", "USDJPY"], ["USDJPY", "USDIDR", "JPYIDR"]]
    combo = random.choice(combos)
    target = random.choice(combo)
    known = [p for p in combo if p != target]
    random.shuffle(known)
    answer = calc_cross(target, known[0], known[1], rates)
    st.session_state.setup = {"target": target, "known1": known[0], "known2": known[1],
                              "rates": rates, "answer": int(answer) if answer else None}

# ======================
# INISIALISASI
# ======================
if "setup" not in st.session_state:
    new_question()

if st.button("🎲 Soal Baru", use_container_width=True):
    new_question()
    st.rerun()

S = st.session_state.setup

# ======================
# SOAL (CENTERED)
# ======================
st.markdown(f"""
    <div class="soal-box">
        <p><b>Diketahui kurs berikut:</b></p>
        <div class="kurs-box">
            <div class="kurs-item">{fmt(S['known1'])} = {int(S['rates'][S['known1']])}</div>
            <div class="kurs-item">{fmt(S['known2'])} = {int(S['rates'][S['known2']])}</div>
        </div>
        <p><b>Berapa nilai {fmt(S['target'])} ?</b></p>
    </div>
""", unsafe_allow_html=True)

# ======================
# INPUT & BUTTONS
# ======================
st.markdown("<br>", unsafe_allow_html=True)
ans = st.number_input(f"Masukkan jawaban {fmt(S['target'])}", min_value=0, step=1, format="%d")
col1, col2 = st.columns(2)
check = col1.button("✅ Cek Jawaban", use_container_width=True)
reveal = col2.button("❔ Lihat Jawaban", use_container_width=True)

# ======================
# EVALUASI
# ======================
if check or reveal:
    true_val = S["answer"]
    if true_val is None:
        st.error("⚠️ Kombinasi soal tidak valid. Klik Soal Baru.")
    else:
        if check:
            if int(ans) == int(true_val):
                st.markdown("""<div class="result-box success-box">🏆 Selamat, kamu jago banget! 🏆</div>""",
                            unsafe_allow_html=True)
            else:
                st.markdown("""<div class="result-box error-box">🔁 Ayo, yuk bisa coba lagi! 💪</div>""",
                            unsafe_allow_html=True)
        else:
            st.info("📘 Jawaban ditampilkan.")

        st.markdown(
            f"""
            <div style="background-color:rgba(255,255,255,0.1);
            padding:1rem;border-radius:12px;margin-top:1rem;text-align:center;
            box-shadow:0 0 8px rgba(255,255,255,0.2);font-size:1.3rem;">
            <b>Kunci:</b> {fmt(S['target'])} =
            <span style="color:#FFD700;font-weight:700;">{int(true_val)}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)
#st.caption("🎨 Desain by DJPPR Booth Edition | Tema: Maroon × Navy | Font: Poppins")








