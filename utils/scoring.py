import streamlit as st


def calculate_personalized_score(
    row,
    preferences,
    df
):

    score = row["recommendation_score"]


    budget = preferences["budget"]

    priority = preferences["priority"]


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
