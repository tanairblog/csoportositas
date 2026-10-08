import webbrowser
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# --- 1. LOAD DATA ---
# Change the filename below to match your file (.csv or .xlsx)
DATA_FILE = "ratings.csv"

file_path = Path(DATA_FILE)
if file_path.suffix == ".xlsx":
    df = pd.read_excel(file_path, index_col=0)
else:
    df = pd.read_csv(file_path, index_col=0)

# The first column is used as index (Song titles).
# All remaining columns are assumed to be student names.
song_titles = df.index.astype(str).tolist()
student_names = df.columns.astype(str).tolist()

# --- 2. HANDLE MISSING / DIAGONAL VALUES ---
# If self-ratings are left empty/NaN, fill them with 10 (or a baseline score).
df_clean = df.fillna(10.0)
X = df_clean.values

# --- 3. STANDARDIZATION (Z-SCORES PER STUDENT) ---
# Removes individual rater bias (harsh vs generous grading).
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- 4. 3D PCA DECOMPOSITION ---
pca = PCA(n_components=3)
song_coords = pca.fit_transform(X_scaled)  # (N_songs, 3)
student_loadings = pca.components_.T       # (N_students, 3)

var_exp = pca.explained_variance_ratio_ * 100

# --- 5. BUILD 3D VISUALIZATION ---
fig = go.Figure()

# A. Plot Songs as Points
fig.add_trace(go.Scatter3d(
    x=song_coords[:, 0],
    y=song_coords[:, 1],
    z=song_coords[:, 2],
    mode="markers+text",
    text=song_titles,
    textposition="top center",
    marker=dict(
        size=7,
        color="royalblue",
        opacity=0.85,
        line=dict(width=1, color="white")
    ),
    name="Songs"
))

# B. Plot Students as Preference Vectors
# Scale vector lengths to sit naturally within the song coordinate space
scale_factor = np.abs(song_coords).max() * 0.95

for i, student in enumerate(student_names):
    x_end = student_loadings[i, 0] * scale_factor
    y_end = student_loadings[i, 1] * scale_factor
    z_end = student_loadings[i, 2] * scale_factor

    # Line from origin (0, 0, 0)
    fig.add_trace(go.Scatter3d(
        x=[0, x_end],
        y=[0, y_end],
        z=[0, z_end],
        mode="lines",
        line=dict(color="crimson", width=3),
        showlegend=False,
        hoverinfo="none"
    ))

    # Name label at vector tip
    fig.add_trace(go.Scatter3d(
        x=[x_end],
        y=[y_end],
        z=[z_end],
        mode="text",
        text=[student],
        textfont=dict(color="crimson", size=12),
        showlegend=False
    ))

# --- 6. LAYOUT & LABELS ---
fig.update_layout(
    title=dict(
        text="3D Music Preference Landscape: Songs & Listener Taste Vectors",
        font=dict(size=18)
    ),
    scene=dict(
        xaxis_title=f"Dimension 1 ({var_exp[0]:.1f}%)",
        yaxis_title=f"Dimension 2 ({var_exp[1]:.1f}%)",
        zaxis_title=f"Dimension 3 ({var_exp[2]:.1f}%)",
        bgcolor="rgba(245, 245, 245, 0.5)"
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)

# --- 7. EXPORT & LAUNCH ---
output_file = Path("music_landscape_3d.html").resolve()
fig.write_html(str(output_file))
webbrowser.open(output_file.as_uri())
print(f"Visualization generated successfully: {output_file}")