# 🏠 UCLA Housing Recommendation System

An interactive data-driven housing recommendation system designed for UCLA students.  
The project integrates real housing listings, Google Maps API commute estimation, and a custom scoring model to help users find optimal apartments based on rent, accessibility, and commute time.

👉 **Live App:** https://YOUR_STREAMLIT_LINK_HERE

---

# 📌 Project Motivation

Finding housing near UCLA is difficult due to tradeoffs between:
- Rent affordability
- Commute time (driving vs public transit)
- Neighborhood quality

This project aims to build a **data-driven decision tool** that helps users compare housing options quantitatively instead of manually browsing listings.

---

# ⚙️ Features

## 🏡 Housing Data Processing
- Real-world housing dataset (Airbnb/Zillow-style listings)
- Data cleaning and normalization
- Feature engineering for rent and location attributes

## 🚗 Commute Time Enrichment
- Google Maps API integration
- Driving time estimation to UCLA
- Public transit time estimation
- Coordinate-based batch processing with caching optimization

## 📊 Scoring System
Custom ranking score combining:
- Monthly rent (normalized)
- Driving commute time
- Transit commute time
- Distance to UCLA

Final score allows ranking of housing options.

---

# 🗺️ Interactive Dashboard (Streamlit)

The deployed app includes:
- Interactive map visualization (Folium)
- Filter system:
  - Max rent
  - Max drive time
  - Max transit time
  - Minimum score
- Ranked recommendation table
- Color-coded housing markers based on score

---

# 🧠 Tech Stack

- Python
- Pandas / NumPy
- Google Maps API
- Streamlit
- Folium (interactive maps)
- Scikit-learn (for feature scaling / normalization)

---

# 📈 Key Insights

- Rent distribution varies significantly across LA neighborhoods
- Commute time is not linearly correlated with distance
- Some mid-distance neighborhoods offer better cost-performance tradeoffs
- Multi-objective scoring improves decision-making compared to raw rent comparison

---

# 🚀 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py