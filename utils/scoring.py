import streamlit as st


def calculate_personalized_score(
    row,
    preferences,
    df
):
    
    base_score = float(
        row.get("recommendation_score", 0)
    )

    if not preferences:
        return base_score

    budget = preferences.get("budget")
    priority = preferences.get(
        "priority",
        "Balanced"
    )
    room_type = preferences.get(
        "room_type",
        "No preference"
    )
    max_drive_time = preferences.get(
        "max_drive_time"
    )
    max_transit_time = preferences.get(
        "max_transit_time"
    )
    preferred_neighborhood = preferences.get(
        "preferred_neighborhood",
        "No preference"
    )

    score = base_score


    if row["monthly_rent"] <= budget:

        score += 5

    else:

        score -= 10



    if priority == "💰 Cheapest":

        if row["monthly_rent"] < df["monthly_rent"].median():

            score += 10



    elif priority == "🚗 Closest to UCLA":

        if row["drive_time"] < df["drive_time"].median():

            score += 10



    elif priority == "🏡 Best Neighborhood":

        score += row["neighborhood_score"] * 0.1



    return min(max(score,0),100)
