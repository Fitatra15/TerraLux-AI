"""
TerraLux AI — Générateur de Rapport Agronomique PDF (ReportLab)
Niveau 3 : Export PDF téléchargeable pour agriculteurs et institutions.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from sqlalchemy.orm import Session

from app.models import Parcel
from app.engine import get_recommendation
from app.soil_intelligence import get_soil_profile

def generate_parcel_pdf(parcel_id: str, db: Session) -> bytes:
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise ValueError("Parcelle introuvable.")

    soil_data = get_soil_profile(parcel_id, db)
    recs = get_recommendation(parcel_id, db)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1a4d2e')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#e67e22')
    )
    heading_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1a4d2e'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2c3e50')
    )

    elements = []

    # Header
    elements.append(Paragraph("TerraLux AI — Rapport d'Aide à la Décision", title_style))
    elements.append(Paragraph("Système expert agronomique explicable, multimodal et contextuel", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a4d2e'), spaceAfter=15))

    # Parcel Info Table
    info_data = [
        [Paragraph("<b>Identifiant :</b>", body_style), Paragraph(parcel.id, body_style),
         Paragraph("<b>Pays / Région :</b>", body_style), Paragraph(f"{parcel.country or 'MDG'} ({parcel.region or 'Diana'})", body_style)],
        [Paragraph("<b>Coordonnées GPS :</b>", body_style), Paragraph(f"[{parcel.latitude:.4f}, {parcel.longitude:.4f}]", body_style),
         Paragraph("<b>Superficie :</b>", body_style), Paragraph(f"{parcel.area_ha or 1.0} ha", body_style)]
    ]
    t_info = Table(info_data, colWidths=[90, 160, 90, 160])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fbf9f4')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e0ce99')),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 15))

    # Section 1 : Soil
    elements.append(Paragraph("1. Profil & Indice de Richesse du Sol (SoilGrids v2.0)", heading_style))
    soil_props = soil_data.get("properties", {})
    soil_rows = [
        ["Classification WRB", "Indice de Richesse", "pH (0-5cm)", "Carbone SOC", "Azote Total"],
        [
            soil_data.get("wrb_class", "Ferralsol"),
            f"{soil_data.get('richness_index', 74)}/100 ({soil_data.get('richness_label', 'Bon')})",
            str(soil_props.get("ph", {}).get("value", 5.8)),
            f"{soil_props.get('soc', {}).get('value', 21.4)} g/kg",
            f"{soil_props.get('nitrogen', {}).get('value', 1.6)} g/kg"
        ]
    ]
    t_soil = Table(soil_rows, colWidths=[130, 110, 80, 90, 90])
    t_soil.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a4d2e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_soil)
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"<b>Interprétation :</b> {soil_data.get('interpretation', '')}", body_style))
    elements.append(Spacer(1, 15))

    # Section 2 : Top 3 Crops
    elements.append(Paragraph("2. Top 3 Recommandations de Cultures (FAO ECOCROP + NASA POWER)", heading_style))
    for idx, crop in enumerate(recs):
        crop_title = f"<b>#{idx+1} {crop.name}</b> ({crop.scientific_name}) — <b>Score : {crop.score}/100</b>"
        elements.append(Paragraph(crop_title, body_style))
        pos_txt = " • ".join(crop.reasons.positive[:2])
        elements.append(Paragraph(f"<i>Justifications :</i> {pos_txt}", body_style))
        if crop.reasons.rotation:
            elements.append(Paragraph(f"<i>Rotation :</i> {crop.reasons.rotation}", body_style))
        elements.append(Spacer(1, 6))

    # Footer note
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#bdc3c7'), spaceAfter=10))
    elements.append(Paragraph(
        "Ce rapport est généré automatiquement par le moteur TerraLux AI à partir des observations satellitaires NASA POWER, "
        "des bases ISRIC SoilGrids et des règles de rotation agronomiques. Document sous licence open-source.",
        ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7, textColor=colors.gray)
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
