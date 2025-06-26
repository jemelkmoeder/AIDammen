import streamlit as st
import pandas as pd
import random
from better_profanity import profanity
 
# Gebruik de nieuwe dataset met een 'Category'-kolom
df = pd.read_csv("all_jokes_combined_categorized.csv")
jokes = df["Joke"].dropna()
categories = sorted(df["Category"].dropna().unique().tolist())  # ✅ Gesorteerde categorieën
 
blocked_words = ["black", "lack people", "lack person", "ack", "ck people", "ck person", "k people", "k person", 
                 "farming equipment", "terrorist", "knee", "grow", "snickers", "nickers", "nicker", 
                 "sickness", "sick", "cancer", "diabetes", "butt", "die", "dying", "death", "dead", "jerking"]
 
st.title("Joke Generator (English Version)")
 
st.markdown("""<style>.stApp {background-image: url("https://img.freepik.com/free-vector/flat-comic-style-background-copy-space_52683-54924.jpg?semt=ais_hybrid&w=740");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;}</style>""", unsafe_allow_html=True)
 
censor = st.checkbox("Do you want to censor dark jokes? (These can be hurtful to some people)", value=True)
if not censor:
    st.error("We advise you to only turn off the censor when you are 16 years or older!")

subject = st.text_input("What subject do you want to hear a joke about?")
selected_category = st.selectbox("Choose a joke category:", ["Any"] + categories)
generate = st.button("Generate Joke")
 
# 🔍 Filterfunctie met onderwerp én/of categorie
def filter_jokes(subject_text, category_text):
    filtered_df = df
    if category_text != "Any":
        filtered_df = filtered_df[filtered_df["Category"] == category_text]
    if subject_text:
        filtered_df = filtered_df[filtered_df["Joke"].str.lower().str.contains(subject_text.lower())]
    return filtered_df["Joke"] if not filtered_df.empty else pd.Series()
 
if generate and subject.strip():
    lower_subject = subject.lower()
 
    if censor:
        profanity.load_censor_words()
        if profanity.contains_profanity(lower_subject) or any(word in lower_subject for word in blocked_words):
            st.warning("This subject is inappropriate 😬")
        else:
            results = filter_jokes(lower_subject, selected_category)
            if not results.empty:
                selected_joke = random.choice(results.tolist())
                st.success("Here it comes:")
                st.markdown(f"*****{profanity.censor(selected_joke)}*****")
                st.image("https://static.vecteezy.com/system/resources/thumbnails/048/560/668/small_2x/cheerful-cute-emoji-png.png", use_container_width=True)
            else:
                st.error("Sorry, no jokes found about that subject 🌚")
    else:
        results = filter_jokes(lower_subject, selected_category)
        if not results.empty:
            selected_joke = random.choice(results.tolist())
            st.success("Here it comes:")
            st.markdown(f"*****{selected_joke}*****")
            st.image("https://static.vecteezy.com/system/resources/thumbnails/048/560/668/small_2x/cheerful-cute-emoji-png.png", use_container_width=True)
        else:
            st.error("Sorry, no jokes found about that subject 🌚")
 
elif generate and not subject.strip():
    results = filter_jokes("", selected_category)
    if not results.empty:
        selected_joke = random.choice(results.tolist())
        st.success("Here it comes:")
        st.markdown(f"*****{selected_joke}*****")
        st.image("https://static.vecteezy.com/system/resources/thumbnails/048/560/668/small_2x/cheerful-cute-emoji-png.png", use_container_width=True)
    else:
        st.error("Please enter a subject or choose a category 😊")
