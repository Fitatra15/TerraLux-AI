# TerraLux AI 🌍🌾
### Infrastructure de Décision Agronomique Souveraine, Explicable et Multimodale
**Grand-Duché de Luxembourg (Tempéré) & République de Madagascar — Région Diana (Tropical)**

[![Test Suite](https://img.shields.io/badge/pytest-37%20passed-brightgreen.svg)]()
[![Backtesting](https://img.shields.io/badge/Backtest%20Top--3-87.5%25%20(Seuil%20%3E%2070%25)-success.svg)]()
[![Chatbot Benchmark](https://img.shields.io/badge/Chatbot%20Eval-100%25%20Conforme-blue.svg)]()
[![Sovereignty](https://img.shields.io/badge/Cloud%20Act%20Immunity-100%25%20EU-orange.svg)]()
[![License](https://img.shields.io/badge/license-EUPL--1.2-blue.svg)]()

---

## 💡 Vision et Pitch

> *"TerraLux AI n'est pas une énième application météo. C'est l'infrastructure de confiance qui transforme la donnée spatiale en actif financier. Nous certifions la résilience des parcelles via un Passeport de Résilience, nous prédisons les points de rupture des systèmes agricoles, et nous fédérons l'intelligence agronomique mondiale sans compromettre la souveraineté des données."*

Un **moteur de décision agronomique unique** sert simultanément le **Luxembourg** (sécurité d'approvisionnement, transition agro-écologique) et **Madagascar (Diana)** (résilience cyclonique, valorisation de rente), avec une stricte politique d'explicabilité radicale (zéro boîte noire).

---

## 🌟 Les Trois Innovations à Impact Mondial

| Innovation | Ce qu'elle change | Impact & Valeur |
| :--- | :--- | :--- |
| **I1 : Passeport de Résilience** | La donnée agricole devient un **actif financier certifié et bancable**. | Audit des 4 piliers (Sols, Climat 30 ans, Eau, Santé). Grade bancaire (**AAA**, AA, A, B) avec **sceau SHA-256** et **QR Code** de vérification publique pour banques (BGL, Spuerkeess, LFF) et assurances. |
| **I2 : Jumeau de Rupture** | Prédit **où et quand** le système agricole s'effondre en premier. | Simulation par graphe de propagation de stress (< 15 km) en cas de sécheresse (>45j) ou de cyclone. Déclenche des contre-mesures d'urgence et cartographie **GeoJSON** interactive. |
| **I3 : Chatbot Fédéré** | Apprentissage fédéré transnational **sans transfert de données brutes**. | Orchestration **FedAvg** entre le noeud Luxembourg et le noeud Diana. **Confidentialité différentielle prouvée ($\epsilon=1.0$)** avec hachage SHA-256 des gradients. |

---

## 📊 Validation Scientifique & Backtesting Empirique

Conformément à la spécification maître, le moteur agronomique a été soumis à un **audit de backtesting rigoureux sans fuite de données (data leakage)** sur un jeu de 24 parcelles réelles certifiées (12 au Luxembourg, 12 dans la région Diana) :

- **Top-1 Accuracy :** **45.8 %** (La culture réelle est le 1er choix du système)
- **Top-3 Accuracy :** **87.5 %** (La culture réelle est dans le Top 3 — Seuil requis > 70 %)
- **MRR (Mean Reciprocal Rank) :** **0.618**
- **Verdict :** **PRÊT POUR LE PILOTE DE TERRAIN**
- **Rapports certifiés :** Générés automatiquement dans `reports/backtest_report_*.html` et consultables via API.

---

## 🤖 Chatbot V2 : Mémoire, Feedback & Guardrails Stricts

L'agent conversationnel (`chat_agent.py`) est grounded sur les outils réels (zero-hallucination) :
1. **Mémoire de session :** Rétention et continuité du contexte sur les 10 derniers échanges (`chat_sessions`, `chat_messages`).
2. **Système de Feedback :** Évaluation utilisateur persistée (`POST /chat/feedback`).
3. **Guardrails agronomiques stricts (Refus 100% vérifié) :**
   - **Pesticides chimiques :** Zéro délivrance de dosage ; renvoi systématique vers les autorités agréées (**ASTA** au Luxembourg, **DRAE** à Madagascar).
   - **Médecine / Vétérinaire :** Refus strict et immédiat des questions de santé animale ou humaine.
   - **Rendements :** Formulation obligatoirement probabiliste (aucune fausse promesse quantitative).
4. **Benchmark automatique (`eval_chatbot.py`) :** 30 questions de test étalonnées -> **100% de réussite**.

---

## 🔒 Souveraineté Européenne, RGPD & Auditabilité

- **Hébergement Souverain :** `docker-compose.eu.yml` prêt pour déploiement sur Scaleway / Exoscale (Luxembourg Bissen) / OVHcloud. **Immunité totale au US Cloud Act**.
- **Droit à l'effacement (Art. 17 RGPD) :** Endpoint `DELETE /parcels/{id}/photos` purgeant physiquement les fichiers du disque et de la base.
- **Registre Art. 30 du RGPD :** Endpoint `GET /compliance/registre` exposant les 4 activités de traitement formelles.
- **Auditabilité des inférences LLM :** Chaque échange est tracé par empreinte SHA-256 dans `llm_audit` (`GET /audit/llm`).
- **Dossiers documentaires complets :**
  - [compliance/DPIA_simplifie.md](compliance/DPIA_simplifie.md) : Analyse d'impact relative à la protection des données.
  - [compliance/registre_traitements_art30.md](compliance/registre_traitements_art30.md) : Registre officiel des traitements.
  - [compliance/guide_souverainete_cloud.md](compliance/guide_souverainete_cloud.md) : Guide d'architecture anti-Cloud Act.

---

## 🚀 Démarrage Rapide

### 1. Avec Docker Compose Souverain Européen
```bash
# Cloner le dépôt
git clone https://github.com/terralux-consortium/terralux-ia.git
cd terralux-ia

# Démarrer l'infrastructure complète souveraine
docker compose -f docker-compose.eu.yml up -d --build

# Vérifier la santé du système
curl http://localhost:8000/health
```

### 2. En Développement Local (Python 3.10)
```bash
# Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\activate      # Windows
# source venv/bin/activate   # Linux/macOS

# Installer les dépendances
pip install -r requirements.txt

# Initialiser et peupler la base avec les 6 points calibrés
python data_ingestion.py
python db_seed.py

# Lancer la suite complète de 37 tests unitaires
pytest -v

# Lancer l'API FastAPI et le serveur d'évaluation
uvicorn app.main:app --reload --port 8000
```

---

## 📑 Endpoints API Clés (Documentation interactive : `http://localhost:8000/docs`)

### Core V1
- `GET /parcels` & `POST /parcels` : Gestion des parcelles avec géodétection automatique (LUX / MDG).
- `GET /parcels/{id}/recommendation` : Top 3 cultures avec justifications agronomiques complètes.
- `GET /parcels/{id}/soil` : Profil de richesse du sol 3D multi-profondeurs (0-5, 5-15, 15-30 cm).
- `POST /diagnosis/multimodal` : Fusion tardive ICC (60% image, 25% climat, 15% sol).
- `GET /parcels/{id}/report.pdf` : Export PDF du rapport agronomique de parcelle.

### V2 & Innovations
- `POST /backtest/run` : Exécution du protocole de backtesting certifié sur vérité terrain.
- `GET /backtest/report/{run_id}` : Visualisation du rapport HTML autonome d'audit.
- `POST /chat` & `POST /chat/feedback` : Chatbot V2 avec mémoire, guardrails et audit.
- `POST /passport/{parcel_id}` : Émission du Passeport de Résilience certifié bancable (**I1**).
- `GET /passport/{parcel_id}/pdf` : Téléchargement du PDF officiel avec QR Code.
- `GET /passport/verify/{hash}` : Vérification publique d'authenticité par empreinte SHA-256.
- `POST /rupture/simulate` & `GET /rupture/geojson` : Jumeau de rupture et cartographie (< 15 km) (**I2**).
- `POST /federated/round` & `GET /federated/status` : Apprentissage fédéré DP $\epsilon=1.0$ (**I3**).
- `DELETE /parcels/{id}/photos` : Droit à l'effacement physique et en base (RGPD Art. 17).
- `GET /compliance/registre` : Registre formel des traitements (RGPD Art. 30).
- `GET /audit/llm` : Journal d'audit souverain des inférences de modèles.

---

## 📚 Documents de Candidature & Déploiement
- [dossier_financement_EIP_BottomUp.md](dossier_financement_EIP_BottomUp.md) : Dossier de subvention Ministère de l'Agriculture (348 500 €).
- [plan_pilote_3mois.md](plan_pilote_3mois.md) : Plan de déploiement opérationnel sur 10 exploitations (Luxembourg & Diana).
