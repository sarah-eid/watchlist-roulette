import streamlit as st
import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIG ---
OMDB_API_KEY = "YOUR_ACTUAL_KEY_HERE"

st.set_page_config(
    page_title="Sarah's Archive Movie Selection",
    page_icon="🎬",
    layout="centered"

)

# --- MODELS ---
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

# --- FUNCTIONS ---
def fetch_omdb_data(title, year):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}&y={year}"
        response = requests.get(url).json()
        if response.get("Response") == "True":
            return {
                "poster": response.get("Poster"),
                "runtime": response.get("Runtime"),
                "summary": response.get("Plot"),
                "rating": response.get("imdbRating"),
                "genre": response.get("Genre")
            }
    except Exception as e:
        st.error(f"CONNECTION_ERROR: {e}")
    return None


@st.cache_data
def build_watchlist_embeddings(df):
    titles, plots = [], []

    for _, row in df.iterrows():
        data = fetch_omdb_data(row["Name"], row["Year"])
        if data and data.get("summary"):
            titles.append(row["Name"])
            plots.append(data["summary"])

    embeddings = embedding_model.encode(plots)
    return titles, embeddings


def recommend_similar_movies(current_plot, titles, embeddings, top_k=3):
    current_embedding = embedding_model.encode([current_plot])
    similarities = cosine_similarity(current_embedding, embeddings)[0]

    ranked = sorted(
        zip(titles, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[1:top_k + 1]  # skip itself


# --- STYLING ---
st.markdown("""
<style>
.main {
    background-color: #050505;
    color: #e0e0e0;
    font-family: 'Courier New', monospace;
}
h1 {
    color: #ff0000;
    border-bottom: 2px solid #ff0000;
    padding-bottom: 10px;
    letter-spacing: 4px;
    margin-bottom: 60px !important;
    text-shadow: 0 0 10px #ff0000;
}
div.stButton {
    text-align: center;
    margin-bottom: 40px;
}
.stButton>button {
    border: 1px solid #ff0000;
    background: black;
    color: #ff0000;
    height: 3.5em;
    width: 280px;
    font-weight: bold;
    letter-spacing: 2px;
    transition: 0.3s;
}
.stButton>button:hover {
    background: #ff0000;
    color: black;
    box-shadow: 0 0 20px #ff0000;
    border: 1px solid white;
}
.movie-card {
    background: #0a0a0a;
    border-radius: 5px;
    padding: 25px;
    border: 1px solid #222;
    border-left: 4px solid #ff0000;
}
</style>
""", unsafe_allow_html=True)

# --- UI ---
st.title("SARAH_ARCHIVE // MOVIE_SELECTION")

st.sidebar.markdown("### SYSTEM_INPUT")
uploaded_file = st.sidebar.file_uploader("UPLOAD_WATCHLIST_CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    titles, embeddings = build_watchlist_embeddings(df)

    col_l, col_btn, col_r = st.columns([1, 2, 1])
    with col_btn:
        execute_scan = st.button("INITIATE_RANDOM_SCAN")

    if execute_scan:
        selection = df.sample(n=1).iloc[0]
        title = selection["Name"]
        year = selection["Year"]

        with st.spinner("DECRYPTING_FILM_DATA..."):
            data = fetch_omdb_data(title, year)

        if data:
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 1.5], gap="large")

            with res_col1:
                if data["poster"] and data["poster"] != "N/A":
                    st.image(data["poster"], use_container_width=True)
                else:
                    st.error("VISUAL_REDACTED")

            with res_col2:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.markdown(
                    f"<h2 style='color:#ff0000; margin-top:0;'>{title.upper()}</h2>",
                    unsafe_allow_html=True
                )

                st.markdown(f"""
                <div style="line-height: 1.8; font-size: 15px;">
                    <span style="color:#ff0000;">▶</span> <b>YEAR:</b> {year}<br>
                    <span style="color:#ff0000;">▶</span> <b>RUNTIME:</b> {data['runtime']}<br>
                    <span style="color:#ff0000;">▶</span> <b>GENRE:</b> {data['genre']}<br>
                    <span style="color:#ff0000;">▶</span> <b>RATING:</b> ⭐ {data['rating']}/10
                </div>
                """, unsafe_allow_html=True)

                st.write("---")
                st.markdown(
                    "<p style='color:#ff0000; font-size:12px; font-weight:bold;'>[ANALYSIS_PLOT]</p>",
                    unsafe_allow_html=True
                )
                st.write(data["summary"])

                st.write("---")
                st.markdown(
                    "<p style='color:#ff0000; font-size:12px; font-weight:bold;'>[SIMILAR_INTELLIGENCE]</p>",
                    unsafe_allow_html=True
                )

                recommendations = recommend_similar_movies(
                    data["summary"],
                    titles,
                    embeddings
                )

                for rec_title, score in recommendations:
                    st.write(f"▶ {rec_title}  ({score:.2f})")

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("DATABASE_MISMATCH: No intelligence found for this entry.")
else:
    st.info("SYSTEM_IDLE: Please upload your 'watchlist.csv' to begin.")

