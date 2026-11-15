# Registre des Activités de Traitement (Article 30 RGPD)
## Système TerraLux AI — Fiche d'Enregistrement Officielle

**Organisme responsable du traitement :** Consortium TerraLux AI (Luxembourg & Madagascar)  
**Adresse légale :** 2, Avenue de l'Université, L-4365 Esch-sur-Alzette, Luxembourg  
**Contact DPO :** `dpo@terralux.lu`  
**Dernière mise à jour :** 15 Novembre 2026  

---

### Fiche n° 1 : Recommandation de Cultures et Passeport de Résilience
- **Finalité du traitement :** Calcul scientifique des cultures les plus résilientes, évaluation des points de rupture agronomique et émission du Passeport de Résilience certifié pour les banques et assurances.
- **Base légale :** Exécution d'un contrat de service agronomique (Art. 6.1.b RGPD) et intérêt légitime pour la transition écologique (Art. 6.1.f RGPD).
- **Catégories de personnes concernées :** Exploitants agricoles, coopératives céréalières et cacaoyères, agronomes régionaux.
- **Catégories de données personnelles :**
  - Nom, prénom, adresse électronique de l'exploitant
  - Identifiant unique de parcelle et coordonnées GPS (centroïde)
  - Caractéristiques chimiques du sol (pH, SOC, azote)
  - Historique des assolements sur 3 ans
- **Destinataires des données :**
  - L'exploitant titulaire de la parcelle
  - Les organismes financiers et assureurs partenaires (uniquement sur présentation du QR Code / SHA-256 certifié par l'exploitant)
  - Les ministères de tutelle (données agrégées sous forme statistique anonyme)
- **Transferts hors Espace Économique Européen :** Aucun. Les données malgaches sont traitées sur le noeud local souverain de Diana dans le cadre du partenariat d'apprentissage fédéré.
- **Délais d'effacement :** Durée d'exploitation active de la parcelle + 3 ans d'archivage comptable et réglementaire.
- **Mesures de sécurité techniques :** Chiffrement de la base PostgreSQL au repos (AES-256), communications HTTPS (TLS 1.3), scellement cryptographique SHA-256 des passeports émis.

---

### Fiche n° 2 : Diagnostic Foliaire par Imagerie Multimodale
- **Finalité du traitement :** Détection précoce des maladies foliaires (mildiou, rouille, pyriculariose) par modèle de vision et fusion de contexte sol/météo.
- **Base légale :** Consentement explicite de l'utilisateur (Art. 6.1.a RGPD).
- **Catégories de données traitées :**
  - Clichés photographiques de feuilles de cultures
  - Horodatage et identifiant de parcelle rattachée
- **Délais d'effacement :** Rétention de 24 mois maximum. Droit d'effacement immédiat disponible via l'API `DELETE /parcels/{id}/photos`.
- **Mesures de sécurité :** Suppression automatique des métadonnées EXIF, stockage en volume privé protégé par RBAC.

---

### Fiche n° 3 : Dialogue Conversationnel Factuel (Chatbot Agronomique)
- **Finalité du traitement :** Assistance technique interactive, justification explicable des choix de culture et alertes agro-climatiques.
- **Base légale :** Consentement de l'utilisateur (Art. 6.1.a RGPD).
- **Catégories de données traitées :**
  - Historique textuel des échanges (10 derniers messages en mémoire de session)
  - Empreinte cryptographique SHA-256 de chaque prompt et réponse (table `llm_audit`)
- **Délais d'effacement :** Purge des sessions inactives après 90 jours.
- **Mesures de sécurité :** Inférence locale via modèle souverain Qwen2.5 hébergé en conteneur européen isolé. Zéro transfert vers des tiers (OpenAI, Anthropic, Google Cloud externe).

---

### Fiche n° 4 : Apprentissage Fédéré Transnational (Innovation I3)
- **Finalité du traitement :** Entraînement collaboratif des modèles agro-écologiques entre le Luxembourg et Madagascar sans transfert de données brutes.
- **Base légale :** Intérêt légitime et recherche scientifique (Art. 6.1.f et Art. 89 RGPD).
- **Catégories de données traitées :** Gradients locaux perturbés par bruit gaussien (Confidentialité différentielle $\epsilon=1.0$).
- **Garantie de non-réversibilité :** Le bruit différentiel rend mathématiquement impossible la reconstruction d'une quelconque parcelle individuelle ou de données nominatives.
