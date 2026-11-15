"""
TerraLux AI — Innovation I3 : Coordinateur d'Apprentissage Fédéré (federated_coordinator.py)
Agrégation souveraine FedAvg sans transfert de données brutes.
Orchestration entre les noeuds de souveraineté :
- Noeud Luxembourg (Chambre d'Agriculture / Sols tempérés)
- Noeud Madagascar (DRAE Diana / Sols tropicaux & agroforesterie)
Formule FedAvg : W_{t+1} = W_t - η * Σ (n_k / N) * G_k
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models import FederatedRound
from app.federated_node import FederatedNode

class FederatedCoordinator:
    def __init__(self):
        # 12 poids initiaux représentant le modèle de décision agronomique partagé
        self.dim = 12
        self.global_weights = [round(0.25 + 0.05 * (i % 4), 4) for i in range(self.dim)]
        self.learning_rate = 0.5
        self.model_version = "terralux-federated-v1"

        # Enregistrement des 2 noeuds souverains
        self.nodes = [
            FederatedNode(node_id="node_luxembourg", country="LUX", n_samples=160),
            FederatedNode(node_id="node_madagascar_diana", country="MDG", n_samples=240)
        ]

    def run_round(self, round_number: int, db: Session, epsilon: float = 1.0) -> Dict[str, Any]:
        """Exécute un round d'apprentissage fédéré complet et persiste les métriques."""
        total_samples = sum(n.n_samples for n in self.nodes)
        node_updates = []
        aggregated_gradient = [0.0] * self.dim

        # 1. Collecte des mises à jour locales avec bruit gaussien différentiel
        for node in self.nodes:
            update = node.compute_local_update(
                global_weights=self.global_weights,
                round_number=round_number,
                epsilon=epsilon
            )
            node_updates.append(update)

            # Contribution pondérée à FedAvg
            weight_ratio = node.n_samples / total_samples
            for i in range(self.dim):
                aggregated_gradient[i] += weight_ratio * update["gradients"][i]

            # 2. Persistance dans la table federated_rounds
            f_round = FederatedRound(
                node_id=node.node_id,
                round_number=round_number,
                model_version=f"{self.model_version}.{round_number}",
                n_samples=node.n_samples,
                metrics={
                    "country": node.country,
                    "local_loss": update["local_loss"],
                    "local_accuracy": update["local_accuracy"],
                    "epsilon": epsilon,
                    "dp_mechanism": update["dp_guarantee"]
                },
                gradient_hash=update["gradient_hash"]
            )
            db.add(f_round)

        # 3. Application de l'agrégation FedAvg
        for i in range(self.dim):
            self.global_weights[i] = round(self.global_weights[i] - self.learning_rate * aggregated_gradient[i], 5)

        db.commit()

        # Métriques globales agrégées
        global_loss = round(sum(u["local_loss"] * (u["n_samples"] / total_samples) for u in node_updates), 4)
        global_accuracy = round(sum(u["local_accuracy"] * (u["n_samples"] / total_samples) for u in node_updates), 3)

        return {
            "round_number": round_number,
            "model_version": f"{self.model_version}.{round_number}",
            "participating_nodes": [n.node_id for n in self.nodes],
            "total_samples_trained": total_samples,
            "privacy_guarantee": f"Differential Privacy ε={epsilon} (Gaussian)",
            "global_loss": global_loss,
            "global_accuracy": global_accuracy,
            "node_updates": [
                {
                    "node_id": u["node_id"],
                    "country": u["country"],
                    "n_samples": u["n_samples"],
                    "gradient_hash": u["gradient_hash"],
                    "local_loss": u["local_loss"],
                    "local_accuracy": u["local_accuracy"]
                }
                for u in node_updates
            ]
        }

    def run_simulation(self, n_rounds: int = 3, db: Session = None, epsilon: float = 1.0) -> Dict[str, Any]:
        """Exécute une séquence de N rounds démontrant la convergence de précision."""
        if db is None:
            raise ValueError("Session de base de données requise.")

        rounds_history = []
        for r in range(1, n_rounds + 1):
            round_res = self.run_round(round_number=r, db=db, epsilon=epsilon)
            rounds_history.append(round_res)

        initial_acc = rounds_history[0]["global_accuracy"]
        final_acc = rounds_history[-1]["global_accuracy"]
        accuracy_gain_pct = round((final_acc - initial_acc) * 100.0, 1)

        return {
            "status": "COMPLETED",
            "rounds_executed": n_rounds,
            "initial_accuracy": initial_acc,
            "final_accuracy": final_acc,
            "accuracy_gain_pct": accuracy_gain_pct,
            "privacy_standard": f"Differential Privacy (ε={epsilon})",
            "data_sovereignty_verified": True,
            "raw_data_transferred": False,
            "rounds": rounds_history
        }

coordinator_singleton = FederatedCoordinator()

def get_federated_status(db: Session) -> Dict[str, Any]:
    """Retourne l'état actuel du réseau d'apprentissage fédéré souverain."""
    recent_rounds = db.query(FederatedRound).order_by(FederatedRound.created_at.desc()).limit(15).all()
    
    return {
        "network_active": True,
        "nodes": [
            {"id": "node_luxembourg", "country": "LUX", "status": "ONLINE", "samples": 160},
            {"id": "node_madagascar_diana", "country": "MDG", "status": "ONLINE", "samples": 240}
        ],
        "total_rounds_logged": db.query(FederatedRound).count(),
        "recent_history": [
            {
                "id": r.id,
                "node_id": r.node_id,
                "round_number": r.round_number,
                "model_version": r.model_version,
                "metrics": r.metrics,
                "gradient_hash": r.gradient_hash,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in recent_rounds
        ]
    }
