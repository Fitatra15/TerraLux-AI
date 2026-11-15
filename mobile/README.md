# Intégration TFLite Embarquée pour Application Mobile (React Native)

Ce document décrit la procédure de déploiement du modèle de diagnostic foliaire TerraLux AI sur mobile sans connexion internet (edge inference).

## 1. Caractéristiques du Modèle TFLite

- **Format** : TensorFlow Lite int8 quantifié (`terralux_leaf_int8.tflite`)
- **Taille** : ~14.8 Mo (Strictement inférieur au seuil de 30 Mo)
- **Entrée** : Tenseur RGB normalisé `(1, 224, 224, 3)`
- **Sortie** : Probabilités Softmax pour 6 classes de maladies (Mildiou, Pyriculariose, Mosaïque, Rouille jaune, Alternariose, Feuille saine)
- **Latence moyenne** : 42 ms sur smartphone Android d'entrée de gamme

---

## 2. Intégration dans React Native

Utiliser la bibliothèque `@tensorflow/tfjs-react-native` ou `react-native-fast-tflite` :

```bash
npm install react-native-fast-tflite
```

### Exemple d'inférence locale :

```typescript
import { loadTensorflowModel } from 'react-native-fast-tflite';

const model = await loadTensorflowModel(
  require('../assets/models/terralux_leaf_int8.tflite')
);

export async function runLocalDiagnosis(imageBuffer: Uint8Array) {
  const output = await model.run([imageBuffer]);
  const scores = output[0];
  // Récupération de la classe dominante
  return parseTopPrediction(scores);
}
```

---

## 3. Double Confiance et Synchronisation

Sur le terrain (Madagascar Diana ou zones rurales du Luxembourg) :
1. L'application calcule immédiatement la confiance image locale.
2. Dès qu'un réseau 2G/3G ou Wi-Fi est disponible, la requête est transmise à l'endpoint `POST /parcels/{id}/diagnose` pour exécuter la **fusion multimodale** avec les données NASA POWER et SoilGrids.
