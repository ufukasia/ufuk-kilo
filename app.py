import sqlite3
from pathlib import Path
from typing import Optional, Tuple

import streamlit as st


DB_PATH = Path(__file__).with_name("ufuk_asil_tahminleri.sqlite3")
TABLE_NAME = "guesses"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                height_guess INTEGER NOT NULL,
                weight_guess INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_guess(height_guess: int, weight_guess: int) -> None:
    with get_connection() as conn:
        conn.execute(
            f"""
            INSERT INTO {TABLE_NAME} (height_guess, weight_guess)
            VALUES (?, ?)
            """,
            (height_guess, weight_guess),
        )
        conn.commit()


def get_averages() -> Tuple[int, Optional[float], Optional[float]]:
    with get_connection() as conn:
        row = conn.execute(
            f"""
            SELECT
                COUNT(*) AS total_count,
                AVG(height_guess) AS avg_height,
                AVG(weight_guess) AS avg_weight
            FROM {TABLE_NAME}
            """
        ).fetchone()

    total_count = int(row["total_count"] or 0)
    avg_height = float(row["avg_height"]) if row["avg_height"] is not None else None
    avg_weight = float(row["avg_weight"]) if row["avg_weight"] is not None else None
    return total_count, avg_height, avg_weight


def reset_guesses() -> None:
    with get_connection() as conn:
        conn.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()


def validate_guess(height_guess: int, weight_guess: int) -> Tuple[bool, str]:
    if not isinstance(height_guess, int) or not isinstance(weight_guess, int):
        return False, "Sayılar tam sayı olmalı. Ondalıklar bu deneyde kapıdan dönüyor."

    if not 100 <= height_guess <= 999:
        return False, "Boy tahmini 3 basamaklı olmalı. Ufuk ASIL için mikroskobik ya da gökdelen modu kapalı."

    if not 100 <= weight_guess <= 999:
        return False, "Kilo tahmini 3 basamaklı olmalı. Terazi de bu deneyde üç haneli konuşuyor."

    return True, ""


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --main-red: #ef4444;
            --main-yellow: #facc15;
            --main-blue: #0ea5e9;
            --ink: #111827;
            --soft: #f8fafc;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(250, 204, 21, 0.32), transparent 28rem),
                radial-gradient(circle at bottom right, rgba(14, 165, 233, 0.24), transparent 26rem),
                linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            color: var(--ink);
        }

        .block-container {
            max-width: 820px;
            padding-top: 1.4rem;
            padding-bottom: 2.2rem;
        }

        .hero-card {
            border: 2px solid rgba(17, 24, 39, 0.12);
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 1.15rem 1rem;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.12);
            margin-bottom: 1rem;
        }

        .hero-eyebrow {
            display: inline-block;
            background: #111827;
            color: #ffffff;
            border-radius: 8px;
            padding: 0.25rem 0.55rem;
            font-size: 0.85rem;
            font-weight: 800;
            margin-bottom: 0.65rem;
        }

        .hero-title {
            font-size: clamp(2rem, 8vw, 3.25rem);
            line-height: 1.02;
            font-weight: 950;
            margin: 0 0 0.65rem 0;
            color: #111827;
        }

        .hero-copy {
            font-size: 1.04rem;
            line-height: 1.55;
            margin: 0;
            color: #334155;
        }

        .info-box, .result-box, .danger-box {
            border-radius: 8px;
            padding: 1rem;
            margin: 0.85rem 0;
            border: 2px solid rgba(17, 24, 39, 0.12);
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
        }

        .info-box {
            border-left: 8px solid var(--main-blue);
        }

        .result-box {
            border-left: 8px solid #22c55e;
        }

        .danger-box {
            border-left: 8px solid var(--main-red);
        }

        .box-title {
            font-size: 1.12rem;
            font-weight: 900;
            margin-bottom: 0.35rem;
            color: #111827;
        }

        .box-copy {
            color: #334155;
            line-height: 1.5;
            margin: 0;
        }

        div.stButton > button,
        div.stFormSubmitButton > button {
            width: 100%;
            min-height: 3.1rem;
            border-radius: 8px;
            border: 2px solid #111827;
            background: #facc15;
            color: #111827;
            font-weight: 900;
            font-size: 1rem;
            box-shadow: 0 5px 0 #111827;
            transition: transform 0.08s ease, box-shadow 0.08s ease, background 0.12s ease;
            white-space: normal;
            word-break: normal;
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            background: #fde047;
            border-color: #111827;
            color: #111827;
        }

        div.stButton > button:active,
        div.stFormSubmitButton > button:active {
            transform: translateY(4px);
            box-shadow: 0 1px 0 #111827;
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.92);
            border: 2px solid rgba(17, 24, 39, 0.12);
            border-radius: 8px;
            padding: 0.85rem;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
        }

        [data-testid="stMetricLabel"] {
            font-weight: 800;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-left: 0.85rem;
                padding-right: 0.85rem;
                padding-top: 0.8rem;
            }

            .hero-card, .info-box, .result-box, .danger-box {
                padding: 0.9rem;
            }

            .hero-title {
                font-size: 2.25rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-eyebrow">Sınıf içi istatistik curcunası</div>
            <h1 class="hero-title">Ufuk ASIL Kaç Santim, Kaç Kilo?</h1>
            <p class="hero-copy">
                Bilim, sezgi ve kontrollü sallama aynı potada buluşuyor.
                Tahminini bırak; kolektif akıl birazdan tek kişilik özgüveni nazikçe dürtebilir.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-box">
            <div class="box-title">Görev: Ufuk ASIL tahmin olimpiyatları</div>
            <p class="box-copy">
                Boy ve kilo için üç basamaklı tam sayı gir. Sonra tahminin sınıf ortalamasına karışsın.
                Ortalamayı açınca hep birlikte “Acaba gerçekten mi?” anını yaşayacağız.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_guess_form() -> None:
    with st.form("guess_form", clear_on_submit=False):
        st.subheader("Tahminini mikrofona bırak")
        height_guess = st.number_input(
            "Boy tahmini (cm)",
            min_value=100,
            max_value=999,
            value=175,
            step=1,
            help="Üç basamaklı tam sayı gir: örn. 175",
        )
        weight_guess = st.number_input(
            "Kilo tahmini (kg)",
            min_value=100,
            max_value=999,
            value=100,
            step=1,
            help="Üç basamaklı tam sayı gir: örn. 100",
        )
        submitted = st.form_submit_button("Tahminimi ortalamaya fırlat")

    if submitted:
        is_valid, message = validate_guess(int(height_guess), int(weight_guess))
        if not is_valid:
            st.error(f"Minik bir istatistik freni: {message}")
            return

        try:
            add_guess(int(height_guess), int(weight_guess))
            st.success("Tahmin kayda geçti. Artık bu sayıların da sınıfta bir karakter gelişimi var.")
        except sqlite3.Error:
            st.error("Veritabanı şu an hesap makinesine küsmüş olabilir. Tahmin kaydedilemedi.")


def render_results() -> None:
    if "show_results" not in st.session_state:
        st.session_state.show_results = False

    if st.button("Kolektif akıl perdesini aç"):
        st.session_state.show_results = True

    if not st.session_state.show_results:
        return

    try:
        total_count, avg_height, avg_weight = get_averages()
    except sqlite3.Error:
        st.error("Ortalama hesaplanırken istatistik kazanında bir fokurdama oldu.")
        return

    if total_count == 0:
        st.warning("Henüz tahmin yok. Kolektif akıl şu an boş sandalyeye bakıyor.")
        return

    st.markdown(
        """
        <div class="result-box">
            <div class="box-title">Sonuçlar geldi: istatistik sahneye çıktı</div>
            <p class="box-copy">
                Tek tek tahminler kenara çekildi, ortalama kravatını düzeltti ve konuşmaya başladı.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Tahminci sayısı", f"{total_count}")
    col2.metric("Ortalama boy", f"{avg_height:.1f} cm")
    col3.metric("Ortalama kilo", f"{avg_weight:.1f} kg")

    st.info("Kolektif akıl notu: Ortalama bazen profesör edasıyla gelir, bazen de sınıfın ortak kaş kaldırmasıyla.")


def render_reset_area() -> None:
    st.markdown(
        """
        <div class="danger-box">
            <div class="box-title">Nükleer silgi bölgesi</div>
            <p class="box-copy">
                Buradaki düğmeler tüm tahminleri siler. Yanlışlıkla basarsan istatistikler bavulunu toplar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    confirm_reset = st.checkbox("Evet, tüm tahminleri silmek istediğimi biliyorum. İstatistiklere mendil uzatıldı.")
    if st.button("Tüm tahminleri usulca yok et", disabled=not confirm_reset):
        try:
            reset_guesses()
            st.session_state.show_results = False
            st.success("Tüm tahminler silindi. Veritabanı şu an tertemiz bir tahta gibi.")
        except sqlite3.Error:
            st.error("Silme işlemi tökezledi. Veritabanı 'bir dakika' dedi.")


def main() -> None:
    st.set_page_config(
        page_title="Ufuk ASIL Tahmin Arenası",
        page_icon="📏",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    apply_styles()

    try:
        init_db()
    except sqlite3.Error:
        st.error("Veritabanı hazırlanamadı. İstatistik treni istasyondan çıkamadı.")
        st.stop()

    render_header()
    render_guess_form()

    st.divider()
    render_results()

    st.divider()
    render_reset_area()


if __name__ == "__main__":
    main()
