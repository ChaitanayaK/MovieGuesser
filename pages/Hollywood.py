import streamlit as st
import pandas as pd
import scripts.cipher as cipher
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Movie Guesser",
    page_icon="assets/icon.png",
)

state = 'hollywood'

if 'toggle' not in st.session_state:
    st.session_state.toggle = state
elif st.session_state.toggle != state:
    st.session_state.clear()
    st.rerun()

st.write("# Guess this Hollywood movie...")

if 'movie' not in st.session_state:
    df = pd.read_csv('data/hollywood.csv')
    st.session_state.movie = df.sample(n=1).iloc[0]

if 'store' not in st.session_state:
    st.session_state.store = []
    st.session_state.store.append(cipher.encrypt(st.session_state.movie['Title'], []))

if 'guessedList' not in st.session_state:
    st.session_state.guessedList = []

if 'win' not in st.session_state or 'lose' not in st.session_state:
    st.session_state.win = False
    st.session_state.lose = False

# st.write(st.session_state.movie)

guess = st.chat_input('Enter your guess..')
if guess:
    guess = guess.lower()
    if len(guess) != 1:
        st.warning('Please guess one letter at a time!!', icon="⚠️")
    elif guess in ['a', 'e', 'i', 'o', 'u']:
        st.warning('You don\'t need to guess a vowel, they are already there', icon="⚠️")
    elif guess in st.session_state.guessedList:
        st.warning('You have already guessed that', icon="⚠️")
    else:
        st.session_state.guessedList.append(guess)
        newList = st.session_state.guessedList.copy()
        st.session_state.store.append(newList)
        result = cipher.encrypt(st.session_state.movie['Title'], newList)
        st.session_state.win = result['win']
        st.session_state.store.append(result)

if 'win' in st.session_state and not st.session_state.win and not st.session_state.lose:
    for i, element in enumerate (st.session_state.store):
        if i%2 == 0:
            if  i >= len(st.session_state.store)-2:
                target = list("HOLLYWOOD")
                for i in range (element['length']):
                    target[i] = "-"
                if tuple(target) == 1 and tuple(target)[0] == '-':
                    st.session_state.lose = True
                target = "## " + " ".join(target)
                st.write(target)
            # Encrypted movie name 
            # Sample: {'movie': '_ u _ _ a a _', 'length': 0, 'win': False}
            st.code(element['movie'])
        else:
            # Guessed and Guesses left
            st.write("##### Your Guesses:  " + " , ".join(element))

else:
    if st.session_state.win:
        st.success("You guessed it Right!!")
    elif st.session_state.lose:
        st.error("Oops, you ran out of guesses...")

    link = f"http://www.omdbapi.com/?t={st.session_state.movie['Title'].strip().replace(' ', '_')}&y={st.session_state.movie['Year']}&plot=short&apikey={os.environ.get('API_KEY')}"

    movie_data = cipher.movieData(link)

    if movie_data:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(movie_data['Poster'], width=200)
        with col2:
            st.title(movie_data['Title'])
            st.subheader(f"{movie_data['Year']} - {movie_data['Genre']}")
            st.write(f"**Director:** {movie_data['Director']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write("**Ratings:**")
            imdb_rating = float(movie_data['imdbRating'])
            if imdb_rating >= 8:
                st.success(f"**IMDb:** {movie_data['Ratings'][0]['Value']}")
            elif imdb_rating >= 7:
                st.info(f"**IMDb:** {movie_data['Ratings'][0]['Value']}")
            else:
                st.warning(f"**IMDb:** {movie_data['Ratings'][0]['Value']}")

            st.write(f"**Language:** {movie_data['Language']}")
            st.write(f"**Country:** {movie_data['Country']}")

        st.markdown("""
        <style>
        .stText {
            text-align: justify;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.write(st.session_state.movie)

    if st.button('Next Challenge'):
        st.session_state.clear()
        st.rerun()
