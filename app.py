import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from src import read_data, top_10_tracks, top_10_year, summary_plots, data_year, \
    create_spider_plot, create_genre_plot
from src.utils.plots import trends_over_time, popularity_distribution, top_artists_popularity, audio_features_trends, correlation_heatmap, genre_distribution, create_scatter_plot_1

SELECT_YEAR_PROMPT = 'Sélectionner une année :'

def run():
    # Configuration de la page
    st.set_page_config(page_title='***Spotify Dashboard***', 
                    page_icon='./public/icon.png', 
                    layout='centered', 
                    initial_sidebar_state='collapsed')

    # Titre principal de la page avec un emoji
    st.title('Spotify Dashboard 🎶')
    st.divider()

    # Menu avec des icônes et des couleurs
    menu_data = st.tabs(['🏠 Accueil',
                        '🎵 Top 10 Chansons',
                        '📈 Trends',
                        '🎧 Genres',
                        '📊 Analyses',
                        '📑 Rapports'])

    with menu_data[0]:
        # Accueil avec une introduction
        st.write('Bienvenue sur le tableau de bord Spotify !')
        st.write('Voici un ensemble complet de données sur les chansons Spotify de 2000 à 2019.')
        st.write('Cette application est un tableau de bord interactif pour analyser ces données.')

        with st.expander("Consultation des données", expanded=True):
            st.write(read_data())
        st.divider()
        # Titre avec couleur pour le graphique des chansons par année
        st.markdown("<h2 style='text-align: center; color: #4CAF50; font-family: Arial, sans-serif;'>Nombre de chansons par année sur Spotify</h2>", unsafe_allow_html=True)
        explicit_filter = st.checkbox('Afficher les explicites', value=False)
        if explicit_filter:
            summary_plots(explicit=True)
        else:
            summary_plots(explicit=False)

    with menu_data[1]:
        # Section des Top 10 Chansons
        st.title('Top 10 chansons 🎵', anchor='top_10_songs')
        year = st.selectbox(SELECT_YEAR_PROMPT, ['Tous'] + list(range(1999, 2020)), key='top_10_tracks')
        if year == 'Tous':
            st.write(top_10_tracks())
            st.divider()
        #   st.write(create_spider_plot(year, song=None))  # Default no song
        elif year:
            st.write(top_10_year(year))
            st.divider()

            song = st.selectbox('Sélectionner une chanson', top_10_year(year)['song'].tolist())
            st.write(create_spider_plot(year, song))

    with menu_data[2]:  
        st.title('Évolution des Tendances 📈', anchor='trends')  
        st.write("Visualisation des changements des caractéristiques musicales au fil du temps.")  
        trends_over_time()

    with menu_data[3]:
        # Section des Genres
        st.title('Genres 🎧', anchor='genres')
        create_genre_plot()
        st.markdown("<h2 style='text-align: center; color: #FF9800; font-family: 'Helvetica', sans-serif;'>Jouez avec les filtres</h2>", unsafe_allow_html=True)
        year = st.selectbox(SELECT_YEAR_PROMPT, list(range(1998, 2021)), index=None, key='genres')
        x = st.selectbox('Axe X', ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"], index=0)
        y = st.selectbox('Axe Y', ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"], index=2)
        if x == y:
            st.error("Veuillez sélectionner des valeurs différentes pour l'axe X et l'axe Y.")
            st.stop()
        if year:
            create_scatter_plot_1(year, x, y)

    with menu_data[4]:
        # Section des Analyses
        st.title('Analyses 📊', anchor='analyses')
        st.write('Cette page montre l analyse de l ensemble de données Spotify.')
        # Choix de l'analyse à afficher
        analysis_choice = st.selectbox("Sélectionnez une analyse :", [
            "Distribution de la Popularité",
            "Top Artistes Populaires",
            "Tendances des Caractéristiques Audio",
            "Corrélations Audio",
            "Répartition des Genres"
        ])

        # Affichage des visualisations
        if analysis_choice == "Distribution de la Popularité":
            popularity_distribution()
        elif analysis_choice == "Top Artistes Populaires":
            top_artists_popularity()
        elif analysis_choice == "Tendances des Caractéristiques Audio":
            audio_features_trends()
        elif analysis_choice == "Corrélations Audio":
            correlation_heatmap()
        elif analysis_choice == "Répartition des Genres":
            genre_distribution()
        
    with menu_data[5]:
        # Section des Rapports
        st.title('Rapports 📑', anchor='reports')
        st.write('Cette page montre les rapports du jeu de données Spotify.')
        year = st.selectbox(SELECT_YEAR_PROMPT, ['Tous'] + list(range(1998, 2021)), index=None, key='reports')
        if year == 'Tous':
            st.download_button('Télécharger CSV 📥', read_data().to_csv(index=False), 'SpotifyData_CSV.csv')
        if year is not None and year != 'Tous':
            st.download_button('Télécharger CSV 📥', data_year(year), f'SpotifyData_{year}_CSV.csv')

# Lancer l'application
if __name__ == "__main__":
    run()
