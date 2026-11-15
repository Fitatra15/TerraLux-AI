# TerraLux AI 🌍🌾

> **Système d'aide à la décision agronomique explicable, multimodal et contextuel.**
> Développé pour le Luxembourg (climat tempéré) et Madagascar (région tropicale de Diana).

---

## 🚀 Quickstart avec Docker Compose

Lancer l'ensemble des services (FastAPI + PostgreSQL 15 / PostGIS 3.4) :

```bash
# 1. Cloner et configurer
cp .env.example .env

# 2. Démarrer les conteneurs
docker compose up -d --build

# 3. Vérifier la santé du service
curl http://localhost:8000/health
# {"status":"ok","version":"1.0.0"}
```

Documentation interactive OpenAPI disponible sur : **http://localhost:8000/docs**

---

## 🛠️ Développement Local (sans Docker)

```bash
# 1. Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\activate  # Sous Windows
# source venv/bin/activate # Sous Linux/macOS

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer les tests
pytest -v

# 4. Lancer le serveur API
uvicorn app.main:app --reload --port 8000
```

---

## 📦 Points de démonstration pré-cachés

| Emplacement | Région / Pays | Latitude | Longitude |
| :--- | :--- | :--- | :--- |
| **Luxembourg-ville** | Gutland, LUX | `49.6116` | `6.1319` |
| **Esch-sur-Alzette** | Minett, LUX | `49.4958` | `5.9806` |
| **Antsiranana** | Diana, MDG | `-12.2794` | `49.2914` |
| **Nosy Be** | Diana, MDG | `-13.3167` | `48.2667` |
| **Ambanja** | Diana, MDG | `-13.6786` | `48.4522` |
| **Ambilobe** | Diana, MDG | `-13.2000` | `49.0500` |

---

## 🏛️ Architecture Technique

```
┌─────────────────────────────────────────────────────────┐
│  FRONTEND (React + Vite + Leaflet + Tailwind)           │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────┐
│  BACKEND (FastAPI)                                      │
│  - /auth, /parcels, /crops, /alerts, /stats, /chat     │
│  - Moteur agronomique explicable (engine.py)            │
│  - Module Richesse des Sols 3D (soil_intelligence.py)  │
│  - Fusion multimodale & late fusion (context_fusion.py)  │
│  - Chatbot grounded à function calling (chat_agent.py) │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────┐              ┌──────────────┐
│ PostgreSQL   │              │ Cache NASA   │
│ + PostGIS    │              │ & SoilGrids  │
└──────────────┘              └──────────────┘
```
