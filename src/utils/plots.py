import io
import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
from .data import read_data, top_10_tracks, top_10_year, top_5_artists, top_5_artists_year, genres

def summary_plots(explicit: bool):
    base = read_data()

    years = base['year'].unique()
    years.sort()

    YEAR_AXIS = 'year:O'
    COUNT_AXIS = 'count:Q'

    if explicit:
        df_explicit = base.groupby(['year', 'explicit']).size().reset_index(name='count')

        fig = alt.Chart(df_explicit).mark_bar().encode(
            x=YEAR_AXIS,
            y=COUNT_AXIS,
            color='explicit:N'
        )

        st.altair_chart(fig, use_container_width=True)    
    else:
        df_count = pd.DataFrame(base['year'].value_counts()).reset_index()
        df_count.columns = ['year', 'count']

        fig = alt.Chart(df_count).mark_bar().encode(
            x=YEAR_AXIS,
            y=COUNT_AXIS
        )

        st.altair_chart(fig, use_container_width=True)

def trends_over_time():
    # Lire les données
    base = read_data()

    # Calculer la moyenne des caractéristiques par année
    avg_features = base.groupby("year")[["danceability", "energy", "loudness", "valence"]].mean().reset_index()

    # Vérifier si les données sont vides
    if avg_features.empty:
        st.warning("Aucune donnée disponible pour afficher les tendances.")
        return

    # Liste des caractéristiques disponibles
    features = ["danceability", "energy", "loudness", "valence"]

    # Sélection dynamique de la caractéristique à afficher
    selected_feature = st.selectbox("📊 Sélectionnez une caractéristique musicale :", features)

    # Créer un graphique interactif avec Plotly
    fig = px.line(avg_features, x="year", y=selected_feature, markers=True,
                  title=f"📈 Évolution de {selected_feature.capitalize()} (2000-2019)",
                  labels={"year": "Année", selected_feature: "Valeur Moyenne"},
                  template="plotly_white")

    # Afficher le graphique interactif
    st.plotly_chart(fig, use_container_width=True)



def create_scatter_plot_1(year, x, y):
    # Lire les données
    base = read_data()

    # Filtrer par année
    base_year = base[base["year"] == year]

    # Vérifier si les données sont vides
    if base_year.empty:
        st.warning(f"Aucune donnée disponible pour l'année {year}.")
        return

    # Créer un scatter plot interactif
    fig = px.scatter(base_year, x=x, y=y, color="genre", hover_data=["song", "artist"],
                     title=f"🎶 Relation entre {x} et {y} pour l'année {year}",
                     labels={x: x.capitalize(), y: y.capitalize(), "genre": "Genre"},
                     template="plotly_white")

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

def popularity_distribution():
    base = read_data()
    
    year = st.slider("Sélectionner une année", min_value=int(base["year"].min()), max_value=int(base["year"].max()), step=1)
    
    data_year = base[base["year"] == year]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data_year["popularity"], bins=20, kde=True, color="blue", ax=ax)
    
    ax.set_title(f"Distribution de la popularité des chansons en {year}")
    ax.set_xlabel("Popularité")
    ax.set_ylabel("Nombre de chansons")
    
    st.pyplot(fig)


def top_artists_popularity():
    base = read_data()

    num_artists = st.slider("Sélectionner le nombre d'artistes à afficher", min_value=5, max_value=20, value=10)
    
    artist_popularity = base.groupby("artist")["popularity"].mean().sort_values(ascending=False).head(num_artists)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=artist_popularity.values, y=artist_popularity.index, palette="magma", ax=ax)
    
    ax.set_title("Top artistes selon la popularité moyenne")
    ax.set_xlabel("Popularité Moyenne")
    ax.set_ylabel("Artiste")
    
    st.pyplot(fig)

def audio_features_trends():
    base = read_data()

    feature = st.selectbox("Sélectionnez une caractéristique audio", ["danceability", "energy", "loudness", "valence", "tempo"])
    
    avg_features = base.groupby("year")[feature].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=avg_features, x="year", y=feature, marker="o", ax=ax, color="purple")
    
    ax.set_title(f"Évolution de {feature} au fil du temps")
    ax.set_xlabel("Année")
    ax.set_ylabel(feature.capitalize())
    ax.grid(True)
    
    st.pyplot(fig)


def correlation_heatmap():
    base = read_data()
    features = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
    
    corr_matrix = base[features].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)

    ax.set_title("Matrice de Corrélation des Caractéristiques Audio")
    
    st.pyplot(fig)

def genre_distribution():
    base = read_data()
    base['genre'] = base['genre'].str.split(', ')
    base = base.explode('genre')

    genre_counts = base['genre'].value_counts()
    
    num_genres = st.slider("Nombre de genres à afficher", min_value=5, max_value=20, value=10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    genre_counts.head(num_genres).plot.pie(autopct="%1.1f%%", startangle=90, cmap="Set3", ax=ax)
    
    ax.set_ylabel("")
    ax.set_title("Répartition des Genres Musicaux")

    st.pyplot(fig)



def create_spider_plot(year: int, song: str = None, all_tracks: bool = False):
    if all_tracks:
        data = top_10_tracks()
    else:
        data = top_10_year(year)

    df_top = pd.DataFrame(data)
    df_top.columns = ['song', 'artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']

    if song:  # Check if a song is selected
        # Check if song exists
        if song not in df_top['song'].values:
            st.error(f"Chanson '{song}' non trouvée dans les données.")
            return

        selected_track = df_top[df_top['song'] == song].iloc[0]
    else:
        # Default to first song if no song is selected
        selected_track = df_top.iloc[0]

    # Prepare data for the plot
    track_features = selected_track[['popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']]
    attributes = track_features.index.tolist()
    values = track_features.tolist()
    
    color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)"

    # Create the spider plot
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=attributes,
        fill='toself',
        fillcolor=color
    ))

    st.markdown(f"<h2 style='text-align: center;'>{selected_track['song']} by <i>{selected_track['artist']}</i></h2>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

def create_stacked_bar_plot(year: int, all_time: bool = False):
    if all_time:
        data_5 = top_5_artists()
    else:
        data_5 = top_5_artists_year(year)

    df_top_5 = pd.DataFrame(data_5)
    df_top_5.columns = ['artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']

    df_top_5['danceability'] = df_top_5['danceability'] * 100
    df_top_5['energy'] = df_top_5['energy'] * 100
    df_top_5['liveness'] = df_top_5['liveness'] * 100
    df_top_5['loudness'] = df_top_5['loudness'] * -5
    df_top_5['tempo'] = df_top_5['tempo'] / 2.1

    df_top_5 = df_top_5.melt(id_vars=['artist'], var_name='attribute', value_name='count')

    fig = alt.Chart(df_top_5).mark_bar().encode(
        x='artist:O',
        y=alt.Y('count:Q', axis=alt.Axis(title='', values=[])),
        color='attribute:N'
    )

    st.altair_chart(fig, use_container_width=True)

def create_scatter_plot():
    base = read_data()

    fig = alt.Chart(base).mark_circle().encode(
        x='danceability',
        y='loudness',
        color='year',
        size='popularity'
    )

    st.altair_chart(fig, use_container_width=True)

def create_genre_plot():
    base = genres()

    fig = px.bar(base, x=base.index, y='count', labels={'x': 'Genre', 'y': 'Count'})

    st.plotly_chart(fig, use_container_width=True)


def create_bubble_plot(year: int, x: str, y: str):
    base = read_data()
    base['genre'] = base['genre'].str.split(',')
    base = base.explode('genre')
    
    # Créer le scatter plot
    fig = px.scatter(
        base.query(f"year=={year}"), 
        x=x, 
        y=y,
        color="genre",
        hover_name="song",
        log_x=True,  # Si pertinent pour vos données
        title=f"{y} vs {x} par genre pour l'année {year}"
    )
    
    # Ajuster les paramètres du graphique
    fig.update_traces(marker=dict(size=10, opacity=0.7))  # Taille uniforme des points
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        legend_title="Genre",
        template="simple_white"
    )
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

def create_spider_plots_pdf(year: int = 0, all_tracks: bool = False):
    if all_tracks:
        data = top_10_tracks()
    else:
        data = top_10_year(year)

    df_top = pd.DataFrame(data)
    df_top.columns = ['song', 'artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']

    df_top['danceability'] = df_top['danceability'] * 100
    df_top['energy'] = df_top['energy'] * 100
    df_top['liveness'] = df_top['liveness'] * 100
    df_top['loudness'] = df_top['loudness'] * -5
    df_top['tempo'] = df_top['tempo'] / 2.1

    images = []
    
    for index, track in df_top.iterrows():
        attributes = ['popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']
        track_features = track[attributes]
        color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)"

        fig = go.Figure(data=go.Scatterpolar(
            r=track_features,
            theta=attributes,
            fill='toself',
            fillcolor=color
            ))
        
        image_data = fig.to_image(format="png", engine="kaleido")
        image = io.BytesIO(image_data)
        images.append(image)
    
    return images