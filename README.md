# Watchlist Roulette

**A random movie selector for your Letterboxd watchlist**

I had a problem, as a Letterboxd user with 800+ of films on my watchlist, I often found myself paralyzed by choice. This tool solves the "what should I watch?" problem by adding an element of chance while still providing intelligent recommendations for what to watch next. 
This tool randomly selects a film from your exported Letterboxd watchlist and recommends similar movies using AI-powered semantic analysis. This is a personal project and not meant as any infringement on Letterboxd's copyright.

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features
- **One-Click Randomizer**: Instantly pick a random movie from your Letterboxd watchlist
- **AI Recommendations**: Get 3 similar movie suggestions using semantic analysis
- **Full Movie Details**: Poster, runtime, genre, rating, and plot summary
- **OMDB Integration**: Automatic fetching of movie metadata

### Requirements
- Python 3.8+
- OMDB API key (free)
- Letterboxd account with watchlist

## For Letterboxd Users - Quick Setup

### **Step 1: Export Your Letterboxd Watchlist**
1. Go to your Letterboxd profile → "Watchlist"
2. Click the **••• (More)** button
3. Select **"Export"** → **"CSV"**
4. Save the file as `watchlist.csv`

### **Step 2: Get Your OMDB API Key**
1. Visit [OMDB API](http://www.omdbapi.com/apikey.aspx)
2. Sign up for a **free API key** 
3. Copy your key - you'll need it in Step 4

### **Step 3: Clone & Install**
```bash
# Clone the repository
git clone https://github.com/sarah-eid/watchlist-roulette.git
cd watchlist-roulette

# Install dependencies
pip install -r requirements.txt
```

### **Step 4: Add Your API Key**
Open `app.py` in any text editor and replace the API key on **line 8**:

```python
# In app.py, line 8, change this:
OMDB_API_KEY = "YOUR_ACTUAL_KEY_HERE"  # ← Paste your OMDB key here
```

**Save the file after making this change.**

### **Step 5: Run the App**
```bash
streamlit run app.py
```

### **Step 6: Upload & Play!**
1. Upload your exported `watchlist.csv`
2. Click **"INITIATE_RANDOM_SCAN"**
3. Let fate decide your next movie!

## How It Works

1. **Upload** your Letterboxd CSV export
2. **Click** the scan button to randomly select a film
3. **View** full movie details 
4. **Get** AI-powered recommendations for similar films
5. **Repeat** when you can't decide what to watch next!

## Repository Structure
```
watchlist-roulette/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Technical Details

**Powered by:**
- `sentence-transformers` - For semantic embeddings
- `scikit-learn (cosine similarity)` - For finding similar movies
- `OMDB API` - For movie metadata
- `Streamlit` - For the web interface

**The Algorithm:**
1. Converts movie plots into vector embeddings
2. Uses cosine similarity to find closest matches
3. Excludes the selected movie from recommendations
4. Returns top 3 most similar films

## ⚠️ Notes
- Requires an active internet connection for OMDB API calls
- Free OMDB tier allows 1,000 requests per day
- Works with standard Letterboxd CSV export format
- Recommendation quality depends on available plot summaries

## Troubleshooting

**"No intelligence found for this entry"**
- Check your OMDB API key in `app.py`
- Ensure the movie exists in OMDB database
- Verify your CSV has correct "Name" and "Year" columns

**"VISUAL_REDACTED"**
- Some movies don't have posters in OMDB
- This doesn't affect functionality

**Slow loading?**
- First run caches embeddings for faster future use
- Large watchlists take longer to process initially

## 📄 License
MIT License 

## 👤 Author
Created by [Sarah Eid](https://github.com/sarah-eid) - A fellow Letterboxd user tired of decision paralysis.
