# Tableau de Bord Spotify

## Aperçu
Ce projet est un **tableau de bord interactif Spotify développé avec Streamlit** qui permet d'explorer et d'analyser les données des morceaux Spotify à travers des visualisations dynamiques et des rapports détaillés.

## Fonctionnalités
- **Visualisations interactives** : Analyse des tendances musicales avec des graphiques dynamiques.
- **Filtres et sélections avancés** : Filtrage par année, artiste, genre et caractéristiques des morceaux.
- **Génération de rapports** : Export en PDF et Excel des analyses effectuées.
- **Interface intuitive** : Utilisation simple via une application web Streamlit.

## Structure du Projet
```
📂 TP2-Data-Viz
├── 📁 data            # Données Spotify
├── 📁 src             # Code source
│   ├── 📁 utils       # Fonctions utilitaires
│   │   ├── data.py    # Gestion et traitement des données
│   │   ├── plots.py   # Fonctions de visualisation
│   │   ├── reports.py # Génération des rapports
├── .gitignore        # Fichiers à ignorer par Git
├── LICENSE          # Licence du projet
├── README.md        # Documentation du projet
├── app.py           # Application principale Streamlit
├── requirements.txt # Liste des dépendances
```

## Installation
### Prérequis
Assurez-vous d'avoir **Python 3.7+** installé. Ensuite, clonez le dépôt et installez les dépendances :
```bash
# Cloner le dépôt
git clone https://github.com/HibaKabada/TP2-Data-Viz.git
cd TP2-Data-Viz

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation
Pour exécuter le tableau de bord Streamlit, utilisez la commande suivante :
```bash
streamlit run app.py
```
L'application s'ouvrira dans votre navigateur.

## Visualisations Disponibles
- **Distribution des morceaux par année**
- **Évolution des caractéristiques audio** (dansabilité, énergie, volume, valence...)
- **Graphiques de dispersion** pour analyser les relations entre variables
- **Popularité des chansons** (histogrammes et classements)
- **Classement des artistes populaires**
- **Matrice de corrélation des caractéristiques audio**
- **Répartition des genres musicaux** (diagrammes circulaires)
- **Graphiques radar** pour visualiser les caractéristiques des morceaux
- **Comparaison d'attributs des artistes** (graphiques empilés)
- **Analyse des genres musicaux par année** (graphiques à bulles)

## Captures
![dash1](https://github.com/user-attachments/assets/a7fd5d3e-c6c1-4744-9923-953ea6b86201)

![dash2](https://github.com/user-attachments/assets/03b1f985-b2ff-4dc7-a3dd-b351ce9d8b83)

![dash3](https://github.com/user-attachments/assets/c47c69c3-fca1-4d35-9022-df50ecac3b3a)

![dash4](https://github.com/user-attachments/assets/a3f6383f-e98d-471f-a86a-71e92c128d6b)

![dash5](https://github.com/user-attachments/assets/1caf87af-c918-4bab-837c-3ee211204b0c)

## Contribution
Les contributions sont les bienvenues ! Forkez le dépôt et proposez vos améliorations.

## Licence
Projet sous licence MIT.

