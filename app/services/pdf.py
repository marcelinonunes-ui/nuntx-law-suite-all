from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import io, os, datetime as dt
from ..config import settings
def _draw_header(c, firm_logo_path: str | None):
    width, height = A4
    if firm_logo_path and os.path.exists(firm_logo_path):
        try:
            img = ImageReader(firm_logo_path)
            c.drawImage(img, 15*mm, height-30*mm, width=40*mm, preserveAspectRatio=True, mask='auto')
        except Exception: pass
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width-15*mm, height-20*mm, settings.FIRM_NAME)
    c.setFont("Helvetica", 9)
    y = height-26*mm
    for line in filter(None, [settings.FIRM_ADDRESS, settings.FIRM_EMAIL, settings.FIRM_PHONE]):
        c.drawRightString(width-15*mm, y, line); y -= 5*mm
    c.setStrokeColor(colors.HexColor("#0f766e")); c.setFillColor(colors.HexColor("#0f766e"))
    c.setLineWidth(2); c.line(15*mm, height-32*mm, width-15*mm, height-32*mm); c.setFillColor(colors.black)
def generate_pdf(kind: str, number: str, client: dict, lines: list[dict], totals: dict, firm_logo_path: str | None = None):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=A4); width, height = A4
    _draw_header(c, firm_logo_path)
    title_map = {"invoice": "Fatura", "quote": "Orçamento", "receipt": "Recibo"}
    c.setFont("Helvetica-Bold", 16); c.drawString(15*mm, height-40*mm, f"{title_map.get(kind, kind).upper()}  #{number}")
    c.setFont("Helvetica", 10)
    c.drawString(15*mm, height-50*mm, f"Cliente: {client.get('name')}")
    c.drawString(15*mm, height-56*mm, f"NIF/NIPC: {client.get('tax_id','')}")
    c.drawString(15*mm, height-62*mm, f"Data: {dt.date.today().isoformat()}")
    c.setFont("Helvetica-Bold", 9)
    y = height-75*mm; headers = ["Descrição", "Qtd", "Preço", "IVA %", "Total"]
    colx = [15*mm, 105*mm, 125*mm, 150*mm, 170*mm]
    for i,h in enumerate(headers): c.drawString(colx[i], y, h)
    y -= 7*mm; c.setFont("Helvetica", 9)
    for ln in lines:
        line_total = round(ln["qty"]*ln["price"]*(1+ln["vat"]/100), 2)
        vals = [ln["desc"], str(ln["qty"]), f"{ln['price']:.2f} €", str(ln["vat"]), f"{line_total:.2f} €"]
        for i,v in enumerate(vals): c.drawString(colx[i], y, v)
        y -= 7*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width-15*mm, y-10*mm, f"Subtotal: {totals['subtotal']:.2f} €")
    c.drawRightString(width-15*mm, y-16*mm, f"IVA: {totals['vat']:.2f} €")
    c.drawRightString(width-15*mm, y-22*mm, f"Total: {totals['total']:.2f} €")
    c.showPage(); c.save(); buf.seek(0); return buf.getvalue()
