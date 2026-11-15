# Analyse d'Impact relative à la Protection des Données (DPIA) — Version Simplifiée
## Système TerraLux AI — Infrastructure de Décision Agronomique Souveraine

**Date de réalisation :** 15 Novembre 2026  
**Responsable du traitement :** Consortium TerraLux AI (Luxembourg & Madagascar)  
**Autorité de contrôle compétente :** CNPD (Commission Nationale pour la Protection des Données, Luxembourg)  
**Conformité légale :** Règlement (UE) 2016/679 (RGPD) & Loi luxembourgeoise du 1er août 2018  

---

### 1. Description du Traitement Envisagé

#### 1.1 Nature et portée du système
TerraLux AI est un système expert d'aide à la décision agronomique croisant des données satellitaires (NASA POWER), des relevés pédologiques (ISRIC SoilGrids), des historiques culturaux et des photos de feuilles végétales pour émettre des recommandations de résilience et délivrer un Passeport de Résilience certifié bancable.

#### 1.2 Catégories de données collectées
- **Données géographiques et parcellaires :** Coordonnées GPS (latitude, longitude), superficie, région, code pays.
- **Données agronomiques :** Précédents culturaux (espèces plantées, années), caractéristiques physico-chimiques du sol (pH, azote, SOC, CEC), régimes pluviométriques et températures.
- **Données d'imagerie foliaire :** Photographies de feuilles et de plants malades téléversées par les exploitants.
- **Données d'utilisateurs :** Adresse email professionnelle, nom/prénom, hachage de mot de passe (Argon2id), rôle (farmer, government, ngo).
- **Traces de conversation :** Requêtes textuelles adressées à l'agent conversationnel, identifiants de session et empreintes SHA-256.

> [!NOTE]
> **Aucune donnée hautement sensible au sens de l'Article 9 du RGPD** (données biométriques, données de santé humaine, opinions politiques) n'est collectée ni traitée.

---

### 2. Évaluation de la Nécessité et de la Proportionnalité

| Principe RGPD | Mesures mises en œuvre dans TerraLux AI |
| :--- | :--- |
| **Licéité du traitement (Art. 6)** | Consentement explicite de l'exploitant (case à cocher lors de l'enregistrement de parcelle) + Exécution de contrat (certification et conseil agronomique). |
| **Minimisation des données (Art. 5.1.c)** | Les coordonnées GPS sont limitées au centroïde de parcelle. Les photographies de feuilles sont dépouillées de leurs métadonnées EXIF (géolocalisation de l'appareil photo purgée). |
| **Limitation de conservation (Art. 5.1.e)** | Rétention des photos plafonnée à 24 mois. Droit à l'effacement immédiat sur simple appel API (`DELETE /parcels/{id}/photos`). Sessions chatbot purgées après 90 jours d'inactivité. |
| **Exactitude des données (Art. 5.1.d)** | Croisement systématique des données déclaratives avec les observations satellitaires NASA POWER et les bases ISRIC SoilGrids. |

---

### 3. Gestion des Risques pour les Droits et Libertés des Personnes

#### Risque 1 : Ré-identification indirecte d'un exploitant via les coordonnées GPS de sa parcelle
- **Gravité initiale :** Modérée | **Probabilité :** Modérée
- **Mesures de remédiation :** 
  - Restriction d'accès RBAC (les autres exploitants ne peuvent pas visualiser les parcelles privées).
  - Agrégation statistique anonymisée dans le tableau de bord institutionnel (`GET /stats/overview`).
  - Dans l'apprentissage fédéré (Innovation I3), application d'un bruit gaussien de confidentialité différentielle ($\epsilon=1.0$) garantissant mathématiquement l'impossibilité de désanonymisation.
- **Risque résiduel :** Faible.

#### Risque 2 : Présence accidentelle d'un visage ou d'une personne sur une photo de feuille malade
- **Gravité initiale :** Élevée | **Probabilité :** Faible
- **Mesures de remédiation :** 
  - Détection automatique et rejet côté client de toute image présentant un ratio de cadrage non végétal.
  - Purge irréversible et immédiate à la demande via l'endpoint dédié de droit à l'oubli.
- **Risque résiduel :** Négligeable.

#### Risque 3 : Transfert illicite de données vers des juridictions tierces (Cloud Act américain)
- **Gravité initiale :** Critique | **Probabilité :** Nulle par conception
- **Mesures de remédiation :**
  - **Souveraineté by Design :** Hébergement exclusif sur infrastructure européenne certifiée (Scaleway / OVHcloud / Exoscale Luxembourg).
  - Aucun sous-traitant américain dans la chaîne d'inférence. Le modèle LLM (Qwen2.5) est exécuté localement en conteneur sécurisé (Ollama) sans aucun appel API vers OpenAI, Anthropic ou Google Cloud externe.
- **Risque résiduel :** Nul.

---

### 4. Avis du Délégué à la Protection des Données (DPO)
Le traitement présente des garanties techniques et organisationnelles d'un niveau exemplaire. La souveraineté des données est assurée dès la conception (Privacy by Design & by Default). Le système est validé pour déploiement pilote dans le Grand-Duché de Luxembourg et dans la région Diana (Madagascar).
