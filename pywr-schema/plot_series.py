import pandas as pd
import os
from plotnine import (
    ggplot, aes, geom_line, theme_minimal,
    labs, theme, element_text
)

# --- 1. Lire le CSV ---
df = pd.read_csv("./../outputs.csv", parse_dates=["time_start", "time_end"])

# --- 2. Préparer le temps pour le plot ---
df["time"] = df["time_start"]

# --- 3. Identifier les séries uniques ---
df["series"] = df["name"] + " - " + df["attribute"]

# --- 4. Créer le dossier 'plot' s'il n'existe pas ---
plot_dir = os.path.join(os.getcwd(), "plot")
os.makedirs(plot_dir, exist_ok=True)

# --- 5. Créer un graphique par série et sauvegarder ---
series_list = df["series"].unique()

for s in series_list:
    subset = df[df["series"] == s]
    
    p = (
        ggplot(subset, aes(x="time", y="value"))
        + geom_line()
        + theme_minimal()
        + labs(
            title=s,
            x="Time",
            y="Value"
        )
        + theme(
            axis_text_x=element_text(rotation=45, ha="right"),
            figure_size=(10, 4)
        )
    )
    
    # Nettoyer le nom pour qu'il soit valide comme fichier
    filename = s.replace(" ", "_").replace(">", "_").replace("/", "_") + ".png"
    
    # Sauvegarder dans le dossier 'plot'
    p.save(os.path.join(plot_dir, filename), verbose=False)

print(f"Graphiques sauvegardés dans : {plot_dir}")
