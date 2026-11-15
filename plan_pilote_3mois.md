# Plan de Déploiement Pilote sur 3 Mois (Roadmap Opérationnelle)
## TerraLux AI — Validation Terrain Luxembourg & Madagascar (Région Diana)

---

### Objectif Global du Pilote
Prouver en conditions réelles d'exploitation l'adhésion des agriculteurs, la précision agronomique (>85% Top-3), l'efficacité des guardrails du chatbot, et l'utilisabilité financière du Passeport de Résilience auprès des partenaires institutionnels.

---

### Mois 1 : Déploiement Terrain & Enrôlement des 10 Exploitations Pilotes

#### Semaine 1 : Sélection et contractualisation des exploitations
- **Luxembourg (5 parcelles test) :**
  1. Canton Capellen (Polyculture céréales / colza)
  2. Gutland Sud - Roeser (Grandes cultures limoneuses)
  3. Vallée de l'Alzette - Bettembourg (Bordure hydrographique / risque inondation)
  4. Canton Remich (Coteaux / stress hydrique prononcé)
  5. Minett - Esch-sur-Alzette (Sols argilo-calcaires lourds)
- **Madagascar - Diana (5 parcelles test) :**
  1. Antsiranana I (Riziculture pluviale de plaine)
  2. Sakaramy (Pied de montagne / maraîchage vivrier)
  3. Ambanja Haut (Agroforesterie Cacao Sambirano)
  4. Ambanja Bas (Système mixte Cacao / Vanille)
  5. Ambilobe (Plaine alluviale Maïs / Manioc)

#### Semaine 2 : Configuration des accès et installation
- Déploiement de l'instance souveraine européenne (`docker-compose.eu.yml`).
- Configuration des comptes utilisateurs RBAC (`farmer`, `government`, `ngo`).
- Formation initiale de 2 heures des agriculteurs à l'application web mobile PWA.

#### Semaines 3 et 4 : Première collecte in-situ
- Importation des centroïdes GPS précis.
- Ingestion des analyses de terre des exploitants et corrélation avec SoilGrids.
- Première passe de photos foliaires pour test du diagnostic MobileNetV3 / DINOv2.

---

### Mois 2 : Stress Testing, Jumeau de Rupture et Cycle Fédéré

#### Semaines 5 et 6 : Évaluation conversationnelle et feedback
- Utilisation quotidienne du chatbot agronomique par les exploitants.
- Mesure du taux de recours aux guardrails (refus strict des pesticides et médecine).
- Collecte des évaluations utilisateur via `POST /chat/feedback` (cible > 90% de satisfaction).

#### Semaine 7 : Simulation Jumeau de Rupture en conditions réelles
- Lancement de simulations de rupture sur la vallée de l'Alzette (Luxembourg) sous hypothèse de sécheresse de 45 jours.
- Lancement de simulations de submersion cyclonique sur le bassin de la Sambirano (Ambanja).
- Validation sur le terrain de la pertinence des contre-mesures agro-écologiques proposées.

#### Semaine 8 : Exécution du premier cycle d'Apprentissage Fédéré Transnational
- Synchronisation du noeud Luxembourg (Chambre d'Agriculture) et du noeud Diana (DRAE).
- 3 rounds FedAvg avec bruit gaussien différentiel ($\epsilon=1.0$).
- Preuve d'absence de fuite de données et publication des empreintes SHA-256 dans le journal d'audit souverain.

---

### Mois 3 : Certification Financière, Audit RGPD et Soutenance

#### Semaines 9 et 10 : Émission des premiers Passeports de Résilience
- Calcul du score global des 10 parcelles pilotes.
- Génération des 10 Passeports de Résilience PDF scellés avec QR Code et empreinte SHA-256.
- Présentation d'un cas réel à deux institutions financières partenaires (Spuerkeess / BGL BNP Paribas) pour validation de la bancabilité de l'actif.

#### Semaine 11 : Audit de conformité RGPD et Souveraineté
- Vérification du registre Art. 30 par le DPO.
- Test de suppression des données par l'exploitant (`DELETE /parcels/{id}/photos`).
- Vérification des logs d'inférence locale (`GET /audit/llm`).

#### Semaine 12 : Soutenance ministérielle et passage à l'échelle
- Présentation des résultats au Ministère de l'Agriculture du Luxembourg (programme EIP-Bottom-Up) et à la DRAE Diana.
- KPI finaux : Top-3 Accuracy > 87 %, Taux de satisfaction exploitants > 92 %, 100 % d'immunité Cloud Act.
- Décision d'extension du pilote à 100 exploitations pour la saison 2027.
