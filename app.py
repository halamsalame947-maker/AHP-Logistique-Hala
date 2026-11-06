import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="AHP - VPR Logistics", page_icon="🏭", layout="wide")

# CSS Avancé pour un look "Dashboard de Direction"
st.markdown("""
    <style>
    /* Fond général et polices */
    .stApp { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Titres */
    h1 { color: #1a252f; font-weight: 800; margin-bottom: 0px; }
    h2 { color: #2c3e50; font-weight: 600; }
    h3 { color: #34495e; font-weight: 500; }
    
    /* Cartes des métriques (Poids) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 4px solid #3498db;
    }
    
    /* Style des sliders */
    .stSlider > div > div > div > div { background-color: #3498db; }
    
    /* Le message de succès */
    .stAlert { border-radius: 12px; border-left: 5px solid #2ecc71; }
    
    /* Barre de séparation */
    hr { margin-top: 20px; margin-bottom: 20px; border-top: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 Aide à la Décision : Choix de l'Entrepôt Intelligent")
st.markdown("<p style='color: #7f8c8d; font-size: 16px;'><b>Méthode AHP (Analytic Hierarchy Process)</b> | Projet de Hala</p>", unsafe_allow_html=True)
st.divider()

# --- CONTEXTE ---
st.markdown("### 📋 Contexte du Scénario")
st.info("**VPR Logistics** doit ouvrir un nouveau hub européen pour distribuer ses colis. Trois villes sont candidates : **Lyon**, **Barcelone** et **Milan**. En tant que Cheffe de Projet, vous devez utiliser la méthode AHP pour recommander la meilleure implantation au comité de direction.")

st.divider()

# --- SECTION 1 : CRITÈRES ---
st.markdown("### ⚖️ 1. Importance des critères")
st.write("Comparez l'importance de chaque critère par rapport à l'autre (1 = importance égale, 9 = importance extrême).")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Comparaisons :**")
    c1 = st.slider("Coût vs Accessibilité (Routière/Aéroportuaire)", 1.0, 9.0, 2.0, 1.0)
    c2 = st.slider("Coût vs Qualité de vie (Main-d'œuvre)", 1.0, 9.0, 3.0, 1.0)
    c3 = st.slider("Accessibilité vs Qualité de vie", 1.0, 9.0, 2.0, 1.0)

# Matrice des critères (4x4)
matrice_criteres = np.array([
    [1, c1, c2, 3],           # Coût
    [1/c1, 1, c3, 2],         # Accessibilité
    [1/c2, 1/c3, 1, 2],       # Qualité
    [1/3, 1/2, 1/2, 1]        # Environnement
])

# Calcul des poids (Vecteur propre)
valeurs_propres, vecteurs_propres = np.linalg.eig(matrice_criteres)
index_max = np.argmax(valeurs_propres)
poids = np.real(vecteurs_propres[:, index_max])
poids = poids / np.sum(poids)

# Affichage des poids
st.write("#### 📊 Poids calculés par l'algorithme AHP :")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("💰 Coût", f"{poids[0]*100:.1f} %")
col_b.metric("🛣️ Accessibilité", f"{poids[1]*100:.1f} %")
col_c.metric("👥 Qualité de vie", f"{poids[2]*100:.1f} %")
col_d.metric("🌱 Environnement", f"{poids[3]*100:.1f} %")

st.divider()

# --- SECTION 2 : VILLES ---
st.markdown("### 🏙️ 2. Évaluation des villes candidates")
st.write("Notez chaque ville sur 10 pour chaque critère (10 = parfait, 0 = catastrophique).")

col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    st.markdown("#### 🇫🇷 Lyon")
    l_c = st.slider("Coût", 0, 10, 7, key="lyon_c")
    l_a = st.slider("Accessibilité", 0, 10, 8, key="lyon_a")
    l_q = st.slider("Qualité de vie", 0, 10, 9, key="lyon_q")
    l_e = st.slider("Environnement", 0, 10, 7, key="lyon_e")

with col_v2:
    st.markdown("#### 🇪🇸 Barcelone")
    b_c = st.slider("Coût", 0, 10, 8, key="bar_c")
    b_a = st.slider("Accessibilité", 0, 10, 9, key="bar_a")
    b_q = st.slider("Qualité de vie", 0, 10, 8, key="bar_q")
    b_e = st.slider("Environnement", 0, 10, 6, key="bar_e")

with col_v3:
    st.markdown("#### 🇮🇹 Milan")
    m_c = st.slider("Coût", 0, 10, 6, key="mil_c")
    m_a = st.slider("Accessibilité", 0, 10, 7, key="mil_a")
    m_q = st.slider("Qualité de vie", 0, 10, 7, key="mil_q")
    m_e = st.slider("Environnement", 0, 10, 8, key="mil_e")

# --- SECTION 3 : RESULTATS ---
s_lyon = (l_c * poids[0] + l_a * poids[1] + l_q * poids[2] + l_e * poids[3])
s_bar = (b_c * poids[0] + b_a * poids[1] + b_q * poids[2] + b_e * poids[3])
s_mil = (m_c * poids[0] + m_a * poids[1] + m_q * poids[2] + m_e * poids[3])

villes = ['Lyon', 'Barcelone', 'Milan']
scores = [s_lyon, s_bar, s_mil]
gagnant = villes[np.argmax(scores)]

st.divider()
st.markdown("### 🏆 3. Recommandation Finale de l'IA")

# Affichage du gagnant avec un effet visuel
st.success(f"Le comité de direction devrait choisir : **{gagnant}** (Score AHP : {max(scores):.2f}/10)")

# Graphique Premium (Barres horizontales)
fig, ax = plt.subplots(figsize=(8, 3))
fig.patch.set_facecolor('#f8f9fa')
ax.set_facecolor('#ffffff')

# Couleurs : Vert pour le gagnant, Gris pour les autres
colors = ['#2ecc71' if v == gagnant else '#bdc3c7' for v in villes]
bars = ax.barh(villes, scores, color=colors, height=0.5, edgecolor='#2c3e50')

# Ligne verticale pour la moyenne
ax.axvline(x=sum(scores)/3, color='#e74c3c', linestyle='--', linewidth=1, label='Moyenne')

ax.set_xlim(0, 10)
ax.set_xlabel('Score global pondéré (sur 10)', fontsize=11, fontweight='bold')
ax.set_title("Classement des villes candidates selon la méthode AHP", fontsize=13, fontweight='bold', pad=15)

# Ajouter les valeurs au bout des barres
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', va='center', fontweight='bold', fontsize=11)

st.pyplot(fig)
