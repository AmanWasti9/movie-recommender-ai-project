import streamlit as st
import pickle
import requests

# Custom CSS to change the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
    }
    h1{
        text-align: center;
    }
    h1, p{
        color: white;
    }
    .stButton button {
        background-color: black;
        color: white;
        border: 2px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fetching Movies Data
movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_lst = movies_df['title'].values
casts_lst = movies_df['actorsandactress'].values

# Importing similarity
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c2648d543899e65bfca55760eb18f276'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id

        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


def recommend_by_actor_or_actress(cast):
    # Find movies with the given cast
    matching_movies = movies_df[movies_df['actorsandactress'].str.contains(cast, case=False)]

    # Check if any matching movies are found
    if matching_movies.empty:
        st.write(f"No movies found with cast: {cast}")
        return [], [], []  # Return empty lists for names, posters, and ratings

    # Sort matching movies by vote_average in descending order
    matching_movies = matching_movies.sort_values(by='vote_average', ascending=False)

    # Get top 5 movies
    top_5_movies = matching_movies.head(5)

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_ratings = []

    for index, row in top_5_movies.iterrows():
        recommended_movies.append(row['title'])
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(row['movie_id']))
        recommended_movies_ratings.append(row['vote_average'])

    return recommended_movies, recommended_movies_poster, recommended_movies_ratings


# Search By Tags

def recommend_by_tags(tag):
    # Find movies with the given tag
    matching_movies = movies_df[movies_df['tags'].str.contains(tag, case=False)]

    # Check if any matching movies are found
    if matching_movies.empty:
        st.write(f"No movies found with tag: {tag}")
        return [], []  # Return empty lists for names and posters

    movie_index = matching_movies.index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id

        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster




# Title
st.title('Movie Recommender System')

# Select Options for movies
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies_lst)

# Recommend Button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# Search by Actor Or Actress

# Title
st.title('Search Top 5 Movies Of Actor Or Actress With Highest Ratings')

# Input field to enter the actor or actress name
selected_cast_name = st.text_input('Enter Actor or Actress Name:', '')

# Recommend Button
if st.button('Recommends'):
    names, posters, ratings = recommend_by_actor_or_actress(selected_cast_name)

    if names:  # Check if names list is not empty
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
            st.text(f'Rating: {ratings[0]}')
        with col2:
            st.text(names[1])
            st.image(posters[1])
            st.text(f'Rating: {ratings[1]}')
        with col3:
            st.text(names[2])
            st.image(posters[2])
            st.text(f'Rating: {ratings[2]}')
        with col4:
            st.text(names[3])
            st.image(posters[3])
            st.text(f'Rating: {ratings[3]}')
        with col5:
            st.text(names[4])
            st.image(posters[4])
            st.text(f'Rating: {ratings[4]}')
    else:
        st.write(f"No movies found for actor or actress name: {selected_cast_name}")



# Search by Tags

# Title
st.title('Search Top 5 Movies By Tags')

# Input field to enter the actor or actress name
selected_tag_name = st.text_input('Enter Any Tag like; Horror, Crime, Thrill:', '')

# Recommend Button
if st.button('Search'):
    names, posters = recommend_by_tags(selected_tag_name)

    if names:  # Check if names list is not empty
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
    else:
        st.write(f"No movies found for tag: {selected_tag_name}")
