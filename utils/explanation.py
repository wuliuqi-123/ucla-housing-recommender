import streamlit as st



def generate_explanation(row, df):
    reasons = []

    comparable = df[
        (df["neighbourhood_cleansed"] == row["neighbourhood_cleansed"]) &
        (df["room_type"] == row["room_type"]) 
    ]

    if len(comparable) < 5:
        comparable = df[df["room_type"] == row["room_type"]]

    median_rent = comparable["monthly_rent"].median()

    if row["monthly_rent"] < median_rent:
        diff = (
            (median_rent - row["monthly_rent"])
            / median_rent
            * 100
        )
        reasons.append(
            f"💰 {diff:.0f}% lower rent than similar listings"
        )

    median_drive = df["drive_time"].median()
    if row["drive_time"] < median_drive:
        reasons.append(
            f"🚗 Faster-than-average drive to UCLA ({row['drive_time']:.0f} min)"
        )

    median_transit = df["transit_time"].median()
    if row["transit_time"] < median_transit:
        reasons.append(
            f"🚌 Better-than-average transit access ({row['transit_time']:.0f} min)"
        )

    median_neigh = df["neigh_score"].median()
    if row["neigh_score"] > median_neigh:
        reasons.append(
            "📍 Above-average neighborhood score"
        )

    if not reasons:
        reasons.append(
            "⚖️ Offers a balanced combination of rent, commute, and location"
        )

    return reasons