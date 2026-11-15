# Guide d'Architecture et de Déploiement Souverain Européen
## TerraLux AI — Garanties Anti-Cloud Act et Hébergement Européen

### 1. Pourquoi la souveraineté est un actif stratégique pour le Luxembourg
Dans les domaines spatiaux et agricoles, la dépendance envers les géants américains du cloud (Hyperscalers : AWS, Microsoft Azure, Google Cloud) expose les gouvernements et exploitants au **US Cloud Act (Clarifying Lawful Overseas Use of Data Act)**, permettant aux autorités judiciaires américaines d'ordonner la saisie de données stockées à l'étranger dès lors que l'opérateur est de droit américain.

TerraLux AI adopte une doctrine de **Souveraineté Intégrale by Design** :
- **Opérateurs d'infrastructure 100% européens :** Scaleway (France/Pays-Bas), Exoscale (Luxembourg Betzdorf/Bissen et Suisse), ou OVHcloud (France/Allemagne).
- **Inférence LLM locale :** Utilisation du modèle open-source Qwen2.5 (7B) ou LLaMA 3 exécuté au sein d'une instance conteneurisée Ollama sur GPU/CPU souverain.
- **Stockage d'objets indépendant :** Utilisation de MinIO déployé sur volumes chiffrés locaux, sans dépendance AWS S3.
- **Auditabilité cryptographique :** Chaque inférence et recommandation est tracée via empreinte SHA-256 dans la table `llm_audit`.

---

### 2. Matrice d'Architecture Souveraine

```
┌────────────────────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE SOUVERAINE EUROPÉENNE                      │
│        (Scaleway Datacenter Paris / Exoscale Luxembourg Bissen)        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   ┌───────────────────────────────────────────────────────────────┐    │
│   │  Proxy Inverse TLS 1.3 / Certificats Let's Encrypt            │    │
│   │  (Port 443 HTTPS - HSTS activé)                               │    │
│   └───────────────────────────────┬───────────────────────────────┘    │
│                                   │                                    │
│   ┌───────────────────────────────▼───────────────────────────────┐    │
│   │  API Backend FastAPI (Port 8000)                              │    │
│   │  - Moteur de décision agronomique (engine.py)                 │    │
│   │  - Passeport de Résilience certifié (passport_generator.py)   │    │
│   │  - Jumeau de Rupture territorial (rupture_twin.py)            │    │
│   │  - Journalisation souveraine SHA-256 (llm_audit)              │    │
│   └──────┬────────────────────────┬───────────────────────┬───────┘    │
│          │                        │                       │            │
│   ┌──────▼──────┐          ┌──────▼──────┐         ┌──────▼──────┐     │
│   │  PostgreSQL │          │   MinIO     │         │   Ollama    │     │
│   │  + PostGIS  │          │  (Stockage  │         │  (Inférence │     │
│   │  (Port 5432)│          │   Local S3) │         │   Locale)   │     │
│   │  Chiffrement│          │  Port 9000  │         │  Port 11434 │     │
│   │  au repos   │          │             │         │             │     │
│   └─────────────┘          └─────────────┘         └─────────────┘     │
│                                                                        │
│   ❌ AUCUN APPEL VERS DES API CLOUD US (ZÉRO OPENAI, ZÉRO AWS)          │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 3. Procédure de Déploiement en Production

#### Étape 1 : Provisionnement d'une instance souveraine
- Commander une instance `PRO2-M` ou `RENDER-S` chez **Scaleway** ou **Exoscale** (Région `lu-bissen` ou `fr-par-1`).
- Système d'exploitation : Ubuntu 22.04 LTS Sovereign Hardened.

#### Étape 2 : Déploiement de la pile Docker Compose Souveraine
```bash
git clone https://github.com/terralux-consortium/terralux-ia.git
cd terralux-ia

# Copier le fichier d'environnement souverain
cp .env.example .env

# Démarrer l'infrastructure complète
docker compose -f docker-compose.eu.yml up -d
```

#### Étape 3 : Téléchargement du modèle de langage local
```bash
docker exec -it terralux-eu-llm ollama pull qwen2.5:7b-instruct
```

#### Étape 4 : Vérification de la conformité souveraine
Exécuter la vérification du registre Art. 30 et des logs d'audit :
```bash
curl -s http://localhost:8000/compliance/registre | jq .hebergement_souverain
curl -s http://localhost:8000/audit/llm | jq .
```
Résultat attendu :
```json
{
  "fournisseur": "Scaleway / Exoscale / OVHcloud (Datacenter Luxembourg / EU)",
  "certification": "SecNumCloud / ISO 27001",
  "transfert_hors_ue": "Aucun (Zéro transfert US Cloud Act)"
}
```
