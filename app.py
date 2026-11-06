import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE (Design) ---
st.set_page_config(page_title="AHP - VPR Logistics", page_icon="🏭", layout="wide")

# Custom CSS pour un design premium
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1 {color: #2c3e50; font-family: 'Helvetica Neue', sans-serif;}
    h2 {color: #34495e;}
    .stButton>button {background-color: #3498db; color: white; border-radius: 8px;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("🏭 Aide à la Décision : Choix de l'Entrepôt Intelligent")
st.markdown("**Méthode AHP (Analytic Hierarchy Process) - Projet de Hala**")
st.write("---")

st.markdown("""
### 📋 Contexte du Scénario
**VPR Logistics** doit ouvrir un nouveau hub européen pour distribuer ses colis. 
Trois villes sont candidates : **Lyon**, **Barcelone** et **Milan**. 
En tant que Cheffe de Projet, vous devez utiliser la méthode AHP pour recommander la meilleure implantation au comité de direction.
""")

st.write("---")

# --- SECTION 1 : PONDÉRATION DES CRITÈRES ---
st.markdown("### ⚖️ 1. Définissez l'importance des critères")
st.write("Comparez chaque critère par rapport à l'autre (1 = importance égale, 9 = importance extrême).")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Critères Logistiques & Management :**")
    c1 = st.number_input("Coût d'implantation vs Accessibilité (Routière/Aéroportuaire)", min_value=1.0, max_value=9.0, value=2.0, step=1.0)
    c2 = st.number_input("Coût d'implantation vs Qualité de vie (Main-d'œuvre)", min_value=1.0, max_value=9.0, value=3.0, step=1.0)
    c3 = st.number_input("Accessibilité vs Qualité de vie", min_value=1.0, max_value=9.0, value=2.0, step=1.0)

# Matrice des critères (4x4)
# Ordre : Coût, Accessibilité, Qualité de vie, Impact environnemental
matrice_criteres = np.array([
    [1, c1, c2, 3],           # Coût
    [1/c1, 1, c3, 2],         # Accessibilité
    [1/c2, 1/c3, 1, 2],       # Qualité
    [1/3, 1/2, 1/2, 1]        # Environnement
])

# Calcul des poids (Vecteur propre)
valeurs_propres, vecteurs_propres = np.linalg.eig(matrice_criteres)
index_max = np.argmax(valeurs_propres)
poids_criteres = np.real(vecteurs_propres[:, index_max])
poids_criteres = poids_criteres / np.sum(poids_criteres)

st.write("---")
st.markdown("#### 📊 Poids calculés par l'algorithme AHP :")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("💰 Coût", f"{poids_criteres[0]*100:.1f} %")
col_b.metric("🛣️ Accessibilité", f"{poids_criteres[1]*100:.1f} %")
col_c.metric("👥 Qualité", f"{poids_criteres[2]*100:.1f} %")
col_d.metric("🌱 Environnement", f"{poids_criteres[3]*100:.1f} %")

st.write("---")

# --- SECTION 2 : NOTATION DES VILLES ---
st.markdown("### 🏙️ 2. Notez les villes candidates (sur 10)")
st.write("Attribuez une note à chaque ville pour chaque critère (10 = parfait, 0 = catastrophique).")

col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    st.subheader("🇫🇷 Lyon")
    lyon_coût = st.slider("Coût", 0, 10, 7, key="l_c")
    lyon_acc = st.slider("Accessibilité", 0, 10, 8, key="l_a")
    lyon_qual = st.slider("Qualité de vie", 0, 10, 9, key="l_q")
    lyon_env = st.slider("Environnement", 0, 10, 7, key="l_e")

with col_v2:
    st.subheader("🇪🇸 Barcelone")
    bar_coût = st.slider("Coût", 0, 10, 8, key="b_c")
    bar_acc = st.slider("Accessibilité", 0, 10, 9, key="b_a")
    bar_qual = st.slider("Qualité de vie", 0, 10, 8, key="b_q")
    bar_env = st.slider("Environnement", 0, 10, 6, key="b_e")

with col_v3:
    st.subheader("🇮🇹 Milan")
    mil_coût = st.slider("Coût", 0, 10, 6, key="m_c")
    mil_acc = st.slider("Accessibilité", 0, 10, 7, key="m_a")
    mil_qual = st.slider("Qualité de vie", 0, 10, 7, key="m_q")
    mil_env = st.slider("Environnement", 0, 10, 8, key="m_e")

# --- SECTION 3 : CALCULS ET RÉSULTATS ---
# Calcul des scores finaux (Somme pondérée)
score_lyon = (lyon_coût * poids_criteres[0] + lyon_acc * poids_criteres[1] + lyon_qual * poids_criteres[2] + lyon_env * poids_criteres[3])
score_bar = (bar_coût * poids_criteres[0] + bar_acc * poids_criteres[1] + bar_qual * poids_criteres[2] + bar_env * poids_criteres[3])
score_mil = (mil_coût * poids_criteres[0] + mil_acc * poids_criteres[1] + mil_qual * poids_criteres[2] + mil_env * poids_criteres[3])

villes = ['Lyon', 'Barcelone', 'Milan']
scores = [score_lyon, score_bar, score_mil]
gagnant = villes[np.argmax(scores)]

st.write("---")
st.markdown("### 🏆 3. Recommandation Finale de l'IA")

# Affichage du gagnant avec un effet visuel
st.success(f"Le comité de direction devrait choisir : **{gagnant}** (Score AHP : {max(scores):.2f}/10)")

# Graphique Premium
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#2ecc71' if v == gagnant else '#95a5a6' for v in villes]
bars = ax.bar(villes, scores, color=colors, edgecolor='#2c3e50', linewidth=1.5)
ax.set_ylabel('Score global pondéré (sur 10)', fontsize=12)
ax.set_title("Classement des villes candidates selon la méthode AHP", fontsize=14, fontweight='bold')
ax.set_ylim(0, 10)

# Ajouter les valeurs sur les barres
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=12)

st.pyplot(fig)
