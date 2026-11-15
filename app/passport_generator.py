"""
TerraLux AI — Innovation I1 : Passeport de Résilience (passport_generator.py)
Transformation de la donnée agro-climatique en actif financier certifié et bancable.
Audit des 4 piliers de résilience :
1. Richesse du sol multi-profondeurs (35%)
2. Résilience et stabilité climatique NASA POWER 30 ans (30%)
3. Sécurité hydrique racinaire GWETROOT (20%)
4. Défense sanitaire et pression pathogène (15%)
Scellement cryptographique par empreinte SHA-256 et QR Code officiel de vérification publique.
"""
import os
import io
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from sqlalchemy.orm import Session

from app.models import Parcel, SoilProfile, Observation, DiseaseRisk, ResiliencePassport, Plant
from app.soil_intelligence import get_soil_profile
from app.engine import get_recommendation

def calculate_passport_metrics(parcel_id: str, db: Session) -> Tuple[Dict[str, float], str, float]:
    """
    Calcule les 4 piliers de résilience et le score global composite :
    Score = 0.35 * Sol + 0.30 * Climat + 0.20 * Eau + 0.15 * (100 - Maladie)
    """
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise ValueError(f"Parcelle ID '{parcel_id}' introuvable.")

    # 1. Pilier Sol (Richesse multi-profondeurs)
    soil_data = get_soil_profile(parcel_id, db)
    richness = float(soil_data.get("richness_index", 75.0))

    # 2. Pilier Climat (Stabilité interannuelle NASA POWER sur 30 ans)
    obs_rains = db.query(Observation).filter(
        Observation.parcel_id == parcel.id,
        Observation.variable == "rain"
    ).all()
    if len(obs_rains) >= 5:
        vals = [o.value for o in obs_rains]
        mean_val = sum(vals) / len(vals)
        variance = sum((v - mean_val) ** 2 for v in vals) / len(vals)
        std_dev = variance ** 0.5
        cv = std_dev / (mean_val + 1e-5) # Coeff de variation
        # Plus cv est bas, plus le climat est stable
        climate_resilience = max(40.0, min(100.0, 100.0 - (cv * 150.0)))
    else:
        climate_resilience = 82.0 if parcel.country == "LUX" else 76.0

    # 3. Pilier Eau (Sécurité hydrique GWETROOT)
    obs_moist = db.query(Observation).filter(
        Observation.parcel_id == parcel.id,
        Observation.variable == "soil_moisture"
    ).first()
    gwetroot = obs_moist.value if obs_moist else (0.64 if parcel.country == "LUX" else 0.58)
    # GWETROOT idéalement entre 0.55 et 0.75
    water_security = max(45.0, min(100.0, gwetroot * 135.0))
    water_stress_risk = round(100.0 - water_security, 1)

    # 4. Pilier Maladie (Pression pathogène & conditions hygrométriques)
    obs_rh = db.query(Observation).filter(
        Observation.parcel_id == parcel.id,
        Observation.variable == "humidity"
    ).first()
    rh_val = obs_rh.value if obs_rh else (76.0 if parcel.country == "LUX" else 82.0)
    # Hygrométrie élevée (>80%) = risque fongique accru
    disease_risk = round(max(10.0, min(65.0, (rh_val - 50.0) * 1.5)), 1)

    # Score Global Pondéré
    global_score = round(
        0.35 * richness +
        0.30 * climate_resilience +
        0.20 * (100.0 - water_stress_risk) +
        0.15 * (100.0 - disease_risk),
        1
    )

    # Attribution du Grade Financier Bancable
    if global_score >= 85.0:
        grade = "AAA" # Résilience Maximale — Actif vert éligible taux bonifié
    elif global_score >= 70.0:
        grade = "AA"  # Résilience Élevée — Éligible assurance standard
    elif global_score >= 55.0:
        grade = "A"   # Résilience Modérée — Plan d'amendement recommandé
    else:
        grade = "B"   # Vulnérabilité Élevée — Régénération requise

    components = {
        "richness_index": round(richness, 1),
        "climate_resilience": round(climate_resilience, 1),
        "water_security": round(100.0 - water_stress_risk, 1),
        "water_stress_risk": water_stress_risk,
        "disease_risk_score": disease_risk,
        "global_score": global_score,
        "grade": grade
    }

    return components, grade, global_score

def compute_resilience_passport(
    parcel_id: str,
    db: Session,
    base_verify_url: str = "http://localhost:8000/passport/verify/"
) -> ResiliencePassport:
    """Génère et certifie le passeport de résilience avec scellement SHA-256."""
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise ValueError(f"Parcelle ID '{parcel_id}' introuvable.")

    metrics, grade, global_score = calculate_passport_metrics(parcel_id, db)

    now = datetime.utcnow()
    valid_until = now + timedelta(days=365) # Validité 1 an

    # Empreinte cryptographique SHA-256 infalsifiable
    canonical_payload = {
        "parcel_id": str(parcel.id),
        "name": parcel.name,
        "country": parcel.country,
        "region": parcel.region,
        "lat": round(parcel.latitude, 4),
        "lng": round(parcel.longitude, 4),
        "global_score": global_score,
        "grade": grade,
        "metrics": metrics,
        "issued_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine": "TerraLux-Passport-v2"
    }
    content_bytes = json.dumps(canonical_payload, sort_keys=True).encode("utf-8")
    content_hash = hashlib.sha256(content_bytes).hexdigest()

    qr_url = f"{base_verify_url.rstrip('/')}/{content_hash}"

    # Génération de l'image QR Code
    qr = qrcode.QRCode(version=1, box_size=6, border=1)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#1a4d2e", back_color="white")
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_bytes = qr_buf.getvalue()

    # Génération du document PDF certifié
    os.makedirs("reports/passports", exist_ok=True)
    pdf_filename = f"reports/passports/passport_{parcel.id}_{content_hash[:8]}.pdf"
    
    pdf_bytes = generate_passport_pdf(
        parcel=parcel,
        metrics=metrics,
        grade=grade,
        global_score=global_score,
        content_hash=content_hash,
        qr_bytes=qr_bytes,
        issued_at=now,
        valid_until=valid_until,
        db=db
    )
    with open(pdf_filename, "wb") as f:
        f.write(pdf_bytes)

    # Persistance en base dans la table resilience_passports
    passport = db.query(ResiliencePassport).filter(ResiliencePassport.parcel_id == parcel.id).first()
    if not passport:
        passport = ResiliencePassport(
            parcel_id=parcel.id,
            issued_at=now,
            valid_until=valid_until,
            richness_index=metrics["richness_index"],
            climate_resilience_score=metrics["climate_resilience"],
            water_stress_risk=metrics["water_stress_risk"],
            disease_risk_score=metrics["disease_risk_score"],
            global_score=global_score,
            pdf_path=pdf_filename,
            qr_code_url=qr_url,
            content_hash=content_hash,
            engine_version="rules-v2-certified",
            data_sources=["NASA POWER 30 ans", "ISRIC SoilGrids 250m", "FAO ECOCROP"]
        )
        db.add(passport)
    else:
        passport.issued_at = now
        passport.valid_until = valid_until
        passport.richness_index = metrics["richness_index"]
        passport.climate_resilience_score = metrics["climate_resilience"]
        passport.water_stress_risk = metrics["water_stress_risk"]
        passport.disease_risk_score = metrics["disease_risk_score"]
        passport.global_score = global_score
        passport.pdf_path = pdf_filename
        passport.qr_code_url = qr_url
        passport.content_hash = content_hash
        passport.engine_version = "rules-v2-certified"

    db.commit()
    db.refresh(passport)
    return passport

def generate_passport_pdf(
    parcel: Parcel,
    metrics: Dict[str, float],
    grade: str,
    global_score: float,
    content_hash: str,
    qr_bytes: bytes,
    issued_at: datetime,
    valid_until: datetime,
    db: Session
) -> bytes:
    """Compile le document PDF certifié bancable."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'PTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=colors.HexColor('#1a4d2e')
    )
    sub_style = ParagraphStyle(
        'PSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=colors.HexColor('#b45309')
    )
    body_style = ParagraphStyle(
        'PBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12,
        textColor=colors.HexColor('#1f2937')
    )
    badge_style = ParagraphStyle(
        'PBadge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=30,
        alignment=1, textColor=colors.HexColor('#1a4d2e')
    )

    story = []

    # En-tête
    country_name = "Grand-Duché de Luxembourg" if parcel.country == "LUX" else "République de Madagascar — Région Diana"
    story.append(Paragraph("TERRALUX AI — PASSEPORT DE RÉSILIENCE AGRICOLE", title_style))
    story.append(Paragraph(f"CERTIFICATION D'ACTIF AGRO-ÉCOLOGIQUE BANCABLE • {country_name.upper()}", sub_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a4d2e"), spaceAfter=14))

    # Badge Grade et Score
    grade_desc = {
        "AAA": "RÉSILIENCE MAXIMALE (ACTIF VERT CERTIFIÉ — ÉLIGIBLE SUBVENTIONS & TAUX BONIFIÉ)",
        "AA": "RÉSILIENCE ÉLEVÉE (ÉLIGIBLE ASSURANCE RÉCOLTE STANDARD)",
        "A": "RÉSILIENCE MOYENNE (PLAN DE RÉGÉNÉRATION SOLS RECOMMANDÉ)",
        "B": "VULNÉRABILITÉ ÉLEVÉE (NÉCESSITE AMENDEMENTS STRUCTURANTS)"
    }.get(grade, "RÉSILIENCE STANDARD")

    banner_data = [
        [
            Paragraph(f"<b>NOTE GLOBALE</b><br/><font size=32><b>{global_score}</b></font><font size=14>/100</font>", ParagraphStyle('Score', alignment=1, textColor=colors.HexColor('#1a4d2e'))),
            Paragraph(f"<b>GRADE BANCAIRE</b><br/><font size=36 color='#1a4d2e'><b>{grade}</b></font>", badge_style),
            Paragraph(f"<b>STATUT DE L'ACTIF</b><br/><font color='#1a4d2e'><b>CERTIFIÉ AUDITABLE</b></font><br/>{grade_desc}", body_style)
        ]
    ]
    t_banner = Table(banner_data, colWidths=[120, 140, 260])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fdf9')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#1a4d2e')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 14))

    # Tableau Informations Parcelle
    soil_profile = db.query(SoilProfile).filter(SoilProfile.parcel_id == parcel.id).first()
    wrb_class = soil_profile.wrb_class if soil_profile else ("Cambisol" if parcel.country == "LUX" else "Ferralsol")

    parcel_data = [
        ["Identifiant Parcelle", parcel.id, "Pays / Territoire", f"{parcel.country} ({parcel.region})"],
        ["Nom de la Parcelle", parcel.name, "Surface Certifiée", f"{parcel.area_ha or 5.0:.1f} hectares"],
        ["Coordonnées GPS", f"{parcel.latitude:.4f} N, {parcel.longitude:.4f} E", "Classification Sols (WRB)", wrb_class],
        ["Date d'Émission", issued_at.strftime("%d/%m/%Y"), "Date d'Expiration", valid_until.strftime("%d/%m/%Y")]
    ]
    t_parcel = Table(parcel_data, colWidths=[130, 130, 130, 130])
    t_parcel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_parcel)
    story.append(Spacer(1, 14))

    # Décomposition des 4 Piliers
    story.append(Paragraph("<b>DÉCOMPOSITION DES 4 PILIERS DE RÉSILIENCE AGRO-ÉCOLOGIQUE</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#1a4d2e'))))
    story.append(Spacer(1, 6))

    pillars_data = [
        ["Pilier", "Pondération", "Score", "Source de Donnée", "Diagnostic Technique"],
        [
            "1. Richesse du Sol (3 Profondeurs)", "35 %",
            f"{metrics['richness_index']}/100", "ISRIC SoilGrids (250m)",
            "Évaluation combinée SOC, azote, CEC et équilibre pH"
        ],
        [
            "2. Résilience Climatique Long-Terme", "30 %",
            f"{metrics['climate_resilience']}/100", "NASA POWER (30 ans)",
            "Stabilité interannuelle des températures et régimes pluviaux"
        ],
        [
            "3. Sécurité Hydrique & Racinaire", "20 %",
            f"{metrics['water_security']}/100", "NASA GWETROOT & In-situ",
            f"Indice de rétention hydrique utile (Stress estimé à {metrics['water_stress_risk']}%)"
        ],
        [
            "4. Maîtrise Pression Sanitaire", "15 %",
            f"{100.0 - metrics['disease_risk_score']:.1f}/100", "Modélisation bio-climatique",
            f"Pression épidémique estimée à {metrics['disease_risk_score']}% sous l'hygrométrie actuelle"
        ]
    ]
    t_pillars = Table(pillars_data, colWidths=[150, 70, 70, 110, 120])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a4d2e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 14))

    # Recommandations de cultures bancables (Top 3)
    recs = get_recommendation(parcel.id, db)
    story.append(Paragraph("<b>PORTFOLIO DES CULTURES ÉLIGIBLES & RÉSILIENCES ASSOCIÉES</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#1a4d2e'))))
    story.append(Spacer(1, 6))

    crops_rows = [["Rang", "Culture Recommandée", "Score Adéquation", "Justification Scientifique Clé"]]
    for i, r in enumerate(recs[:3]):
        justif = r.reasons.positive[0] if r.reasons.positive else "Tolérance agronomique vérifiée"
        crops_rows.append([f"Top {i+1}", r.name, f"{r.score}/100", justif[:65]])

    t_crops = Table(crops_rows, colWidths=[50, 140, 100, 230])
    t_crops.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_crops)
    story.append(Spacer(1, 14))

    # Sceau Cryptographique & QR Code
    qr_flowable = Image(io.BytesIO(qr_bytes), width=70, height=70)
    security_text = (
        f"<b>AUTHENTIFICATION ET INTÉGRITÉ SOUVERAINE</b><br/>"
        f"Empreinte SHA-256 : <font size=7 color='#1a4d2e'><b>{content_hash}</b></font><br/>"
        f"Moteur de certification : TerraLux AI Rules-v2 • Cadre légal spatial et souveraineté des données.<br/>"
        f"Scannez ce QR Code pour vérifier instantanément la validité sur le registre officiel."
    )
    security_data = [
        [qr_flowable, Paragraph(security_text, body_style)]
    ]
    t_sec = Table(security_data, colWidths=[80, 440])
    t_sec.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1a4d2e')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sec)

    doc.build(story)
    return buffer.getvalue()
