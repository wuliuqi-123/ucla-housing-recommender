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



def generate_personalized_explanation(
    row,
    preferences
):

    reasons = []


    budget = preferences["budget"]

    priority = preferences["priority"]



    # budget match

    if row["monthly_rent"] <= budget:

        reasons.append(
            f"💰 Within your budget (${budget})"
        )



    # priority

    if priority == "💰 Cheapest":

        reasons.append(
            "💰 Matches your preference for affordable housing"
        )


    elif priority == "🚗 Closest to UCLA":

        if row["drive_time"] <= 15:

            reasons.append(
                f"🚗 Short commute to UCLA ({row['drive_time']:.0f} min)"
            )


    elif priority == "🏡 Best Neighborhood":

        reasons.append(
            "📍 Located in a highly rated neighborhood"
        )



    # general fallback

    if row["transit_time"] <= 30:

        reasons.append(
            "🚌 Good public transportation access"
        )


    return reasons[:4]