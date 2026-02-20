import streamlit as st
import ollama
import random
import string
import re
import os
import qrcode
import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF
from datetime import datetime
import html
import tempfile
import shutil
from pathlib import Path

# --- CONSTANTS ---
TAX_RATE = 0.0825
GEEK_SQUAD_PRICE = 99.99
APPLECARE_PRICE = 199.00
LOGO_WIDTH = 15
LOGO_Y_POS = 5
BARCODE_WIDTH = 50
QR_CODE_WIDTH = 16
PDF_THERMAL_WIDTH = 80
PDF_DIGITAL_WIDTH = 210
PDF_HEIGHT = 240
FONT_SIZE = 8
LINE_HEIGHT = 3.2
MARGIN = 5

# --- DATASET ---
STORES = {
    "Best Buy": {
        "asset": "bby_logo.png",
        "url": "https://www.bestbuy.com/returns",
        "locations": {
            "5133 Richmond Ave, Houston, TX 77056": "Store #0241",
            "660 W 34th St, New York, NY 10001": "Store #1503",
            "1000 W Sunset Blvd, Los Angeles, CA 90046": "Store #0789"
        },
        "policy": "15-day return window. 15% restocking fee may apply. Original packaging required.",
        "phone": "1-888-BEST-BUY",
        "header": "BEST BUY"
    },
    "Newegg": {
        "asset": "newegg_logo.png",
        "url": "https://kb.newegg.com/returns",
        "locations": {
            "18045 Castleton St, City of Industry, CA 91748": "Warehouse - WH-West-01",
            "1055 S Gateway Dr, Edison, NJ 08817": "Warehouse - WH-East-01",
            "1250 N McDowell Blvd, Petaluma, CA 94954": "Warehouse - WH-North-01"
        },
        "policy": "30-day Hassle-Free Returns. Replacement or refund available. Restocking fee may apply for opened items.",
        "phone": "1-800-390-1119",
        "header": "NEWEGG.COM",
        "customer_service": "service@newegg.com",
        "order_prefix": "NG"
    },
    "Apple Store": {
        "asset": "apple_logo.png",
        "url": "https://www.apple.com/returns",
        "locations": {
            "767 5th Ave, New York, NY 10153": "Store #R001",
            "1 Stockton St, San Francisco, CA 94108": "Store #R423",
            "820 N Michigan Ave, Chicago, IL 60611": "Store #R275"
        },
        "policy": "14-day return window. Original condition required. No restocking fee.",
        "phone": "1-800-MY-APPLE",
        "header": "APPLE STORE"
    },
    "NetPro Tools": {
        "asset": "netpro_logo.png",
        "url": "https://www.netprotools.com/support/returns",
        "locations": {
            "9500 Great Hills Trail, Austin, TX 78759": "Corporate Headquarters",
            "1 New York Plaza, New York, NY 10004": "Regional Office - Northeast",
            "555 California St, San Francisco, CA 94104": "Regional Office - West Coast"
        },
        "policy": "45-day return window for unopened items. 20% restocking fee for opened software. Enterprise licensing non-refundable.",
        "phone": "1-855-NETPRO1",
        "header": "NETPRO TOOLS - ENTERPRISE NETWORK SOLUTIONS",
        "customer_service": "enterprise@netprotools.com",
        "tech_support": "support@netprotools.com",
        "order_prefix": "NPT",
        "vendor_id": "NET-PRO-2024"
    }
}

def validate_items_format(items_text):
    """Validate that items text follows expected format."""
    if not items_text or not items_text.strip():
        return False, "Items text cannot be empty"
    
    pattern = r'(?:(\d+)x\s+)?[^$]*\$\s?\d{1,5}\.\d{2}'
    matches = re.findall(pattern, items_text)
    if not matches:
        return False, "No valid items found. Expected format: '1x Item Name $99.99'"
    
    return True, ""

def calculate_totals(items_text, discount_perc=0, gs=False, ac=False, trade_in=0.0):
    pattern = r'(?:(\d+)x\s+)?.*?(?:\$\s?| )(\d{1,5}\.\d{2})'
    matches = re.findall(pattern, items_text)
    subtotal = sum((int(q) if q else 1) * float(p) for q, p in matches)
    if gs: subtotal += GEEK_SQUAD_PRICE
    if ac: subtotal += APPLECARE_PRICE
    subtotal -= trade_in
    d_amt = subtotal * (discount_perc / 100)
    tax = (subtotal - d_amt) * TAX_RATE
    return subtotal, d_amt, tax, subtotal - d_amt + tax

def format_items_table(items_text, serials, store_name):
    """
    Convert raw items input and serial numbers into a formatted table.
    Different formatting for different stores.
    """
    lines = []
    
    if store_name == "NetPro Tools":
        # NetPro Tools - Enterprise B2B format
        lines.append("PART #     ITEM DESCRIPTION                     LICENSE    QTY   UNIT PRICE    EXTENDED")
        lines.append("-" * 85)
        pattern = r'(?:(\d+)x\s+)?(.*?)\s+\$(\d{1,5}\.\d{2})'
        for i, (qty, desc, price) in enumerate(re.findall(pattern, items_text)):
            qty = qty or '1'
            part_num = f"NPT-{random.randint(1000, 9999)}"
            license_type = "Perpetual" if "License" in desc else "N/A"
            serial = serials[i] if i < len(serials) else 'N/A'
            item_total = float(price) * int(qty)
            line = f"{part_num:<10} {desc:<35} {license_type:<10} {qty:>3}  ${float(price):>10.2f}  ${item_total:>11.2f}"
            lines.append(line)
            if serial != 'N/A':
                lines.append(f"           License Key: {serial}")
        lines.append("-" * 85)
    elif store_name == "Newegg":
        # Newegg format - more detailed
        lines.append("SKU         Item Description                     Qty   Price      Total")
        lines.append("-" * 70)
        pattern = r'(?:(\d+)x\s+)?(.*?)\s+\$(\d{1,5}\.\d{2})'
        for i, (qty, desc, price) in enumerate(re.findall(pattern, items_text)):
            qty = qty or '1'
            sku = f"NE{i+1:06d}"
            serial = serials[i] if i < len(serials) else 'N/A'
            item_total = float(price) * int(qty)
            line = f"{sku:<10} {desc:<35} {qty:>3}  ${float(price):>8.2f}  ${item_total:>8.2f}"
            lines.append(line)
            if serial != 'N/A':
                lines.append(f"           Serial: {serial}")
        lines.append("-" * 70)
    elif store_name == "Apple Store":
        # Apple format - minimalist
        lines.append("Item                              Qty  Price")
        lines.append("-" * 45)
        pattern = r'(?:(\d+)x\s+)?(.*?)\s+\$(\d{1,5}\.\d{2})'
        for i, (qty, desc, price) in enumerate(re.findall(pattern, items_text)):
            qty = qty or '1'
            serial = serials[i] if i < len(serials) else 'N/A'
            line = f"{desc:<33} {qty:>2}  ${float(price):>8.2f}"
            lines.append(line)
        lines.append("-" * 45)
    else:
        # Best Buy format - original
        lines.append("Item Description                 Qty Price    Serial")
        lines.append("-" * 50)
        pattern = r'(?:(\d+)x\s+)?(.*?)\s+\$(\d{1,5}\.\d{2})'
        for i, (qty, desc, price) in enumerate(re.findall(pattern, items_text)):
            qty = qty or '1'
            serial = serials[i] if i < len(serials) else 'N/A'
            line = f"{i+1:<3} {desc:<25} {qty:<3} ${float(price):>7.2f}  {serial}"
            lines.append(line)
        lines.append("-" * 50)
    
    return "\n".join(lines)

def safe_image_load(pdf, image_path, x, y, w):
    """Safely load an image with error handling."""
    try:
        if image_path and os.path.exists(image_path):
            # Check if file is readable
            with open(image_path, 'rb') as f:
                f.read(1)  # Test read
            pdf.image(image_path, x=x, y=y, w=w)
            return True
    except (IOError, OSError, Exception) as e:
        st.warning(f"Could not load image {image_path}: {str(e)}")
    return False

def create_pdf_bytes(text, format_type, logo_path=None, qr_path=None, barcode_path=None):
    width = PDF_THERMAL_WIDTH if format_type == "Thermal Paper" else PDF_DIGITAL_WIDTH
    pdf = FPDF(unit='mm', format=(width, PDF_HEIGHT))
    pdf.add_page()

    # Logo at top center
    if logo_path:
        safe_image_load(pdf, logo_path, x=(width/2 - LOGO_WIDTH/2), y=LOGO_Y_POS, w=LOGO_WIDTH)

    # Receipt text starts below logo
    pdf.set_font("Courier", size=FONT_SIZE)
    pdf.set_xy(MARGIN, 20)
    pdf.multi_cell(0, LINE_HEIGHT, txt=text, align='L' if format_type == "Thermal Paper" else 'C')

    # Bottom section: barcode & QR
    bottom_y = pdf.get_y() + 5
    if barcode_path:
        safe_image_load(pdf, barcode_path, x=(width/2 - BARCODE_WIDTH/2), y=bottom_y, w=BARCODE_WIDTH)
    if qr_path:
        qr_y = bottom_y + 20 if barcode_path else bottom_y
        safe_image_load(pdf, qr_path, x=(width/2 - QR_CODE_WIDTH/2), y=qr_y, w=QR_CODE_WIDTH)

    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(page_title="Manifest Engine", layout="wide")

with st.sidebar:
    st.header("Admin Controls")
    receipt_type = st.radio("Format", ["Thermal Paper", "Digital Email"])
    discount = st.slider("Discount (%)", 0, 50, 0)
    trade_in_val = st.number_input("Trade-In Credit ($)", 0.0, 2000.0, 0.0)
    add_gs = st.checkbox("Add Geek Squad")
    add_ac = st.checkbox("Add AppleCare+")
    include_sig = st.checkbox("Include Signature", value=True)
    show_points = st.checkbox("Show Rewards", value=True)

col1, col2 = st.columns(2)
with col1:
    store_name = st.selectbox("Retailer", list(STORES.keys()))
    address = st.selectbox("Location", list(STORES[store_name]["locations"].keys()))
with col2:
    pay_method = st.selectbox("Payment", ["Visa", "Mastercard", "Amex", "Apple Pay"])
    dt = st.date_input("Date", datetime.now())
    items = st.text_area("Items (e.g., '1x Nikon D850 $2799.00')", "1x Nikon D850 $2799.00")

if st.button("Generate Final Manifest", type="primary"):
    # Validate input first
    is_valid, error_msg = validate_items_format(items)
    if not is_valid:
        st.error(f"Invalid items format: {error_msg}")
        st.stop()
    
    # Create temporary directory for generated files
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Generate invoice/order number
        if store_name == "Newegg":
            inv_raw = ''.join(random.choices(string.digits, k=9))
            inv_pretty = f"{STORES[store_name]['order_prefix']}{inv_raw}"
        elif store_name == "NetPro Tools":
            inv_raw = ''.join(random.choices(string.digits + string.ascii_uppercase, k=8))
            inv_pretty = f"{STORES[store_name]['order_prefix']}-{inv_raw[:4]}-{inv_raw[4:]}"
        else:
            inv_raw = ''.join(random.choices(string.digits, k=10))
            inv_pretty = f"{inv_raw[:4]}-{inv_raw[4:7]}-{inv_raw[7:]}"

        # Generate barcode
        barcode_path = os.path.join(temp_dir, "current_barcode")
        CODE128 = barcode.get_barcode_class('code128')
        my_barcode = CODE128(inv_raw, writer=ImageWriter())
        my_barcode.save(barcode_path)

        # Calculate totals
        sub, d_amt, tax, grand = calculate_totals(items, discount, add_gs, add_ac, trade_in_val)

        # Generate QR code
        qr_path = os.path.join(temp_dir, "current_qr.png")
        qr = qrcode.make(STORES[store_name]['url'])
        qr.save(qr_path)

        # Get serial numbers from Ollama
        try:
            # Check if Ollama is available and model exists
            ollama.list()
            res = ollama.chat(
                model='receipt-bot',
                messages=[{
                    'role': 'user',
                    'content': f"List items: {items}. Return only serial numbers, one per line, for each hardware item. No extra text."
                }]
            )
            serials = res['message']['content'].strip().split('\n')
        except (ConnectionError, TimeoutError, Exception) as e:
            st.warning(f"Could not connect to Ollama service: {str(e)}. Using generated serial numbers.")
            # Count actual items correctly
            pattern = r'(?:(\d+)x\s+)?[^$]*\$\s?\d{1,5}\.\d{2}'
            item_count = len(re.findall(pattern, items))
            serials = [f"SN-{random.randint(1000,9999)}" for _ in range(item_count)]

    # Build receipt body
    if store_name == "NetPro Tools":
        # NetPro Tools specific header - Enterprise B2B format
        header = f"{STORES[store_name]['header']}\n{address}\n{STORES[store_name]['locations'][address]}\n" + "="*85 + f"\nPURCHASE ORDER: {inv_pretty}\nDATE: {dt.strftime('%m/%d/%Y')}  TIME: {datetime.now().strftime('%H:%M:%S')}\nACCOUNT REP: {random.choice(['Anderson', 'Chen', 'Rodriguez', 'Kim'])}\nVENDOR ID: {STORES[store_name]['vendor_id']}\n" + "="*85 + "\n"
    elif store_name == "Newegg":
        # Newegg specific header
        header = f"{STORES[store_name]['header']}\n{address}\n{STORES[store_name]['locations'][address]}\n" + "="*70 + f"\nORDER NUMBER: {inv_pretty}\nDATE: {dt.strftime('%m/%d/%Y')}  TIME: {datetime.now().strftime('%H:%M:%S')}\nCUSTOMER SERVICE: {STORES[store_name]['phone']}\n" + "="*70 + "\n"
    elif store_name == "Apple Store":
        # Apple specific header
        header = f"{STORES[store_name]['header']}\n{address}\n{STORES[store_name]['locations'][address]}\n" + "-"*45 + f"\nReceipt #: {inv_pretty}\nDate: {dt.strftime('%m/%d/%y')}  Time: {datetime.now().strftime('%H:%M')}\n" + "-"*45 + "\n"
    else:
        # Best Buy format (original)
        header = f"{store_name.upper()}\n{address}\n{STORES[store_name]['locations'][address]}\n" + "-"*50 + f"\nVAL#: {inv_pretty}\nDATE: {dt.strftime('%m/%d/%y')}  TIME: {datetime.now().strftime('%H:%M')}\n" + "-"*50 + "\n"

    items_table = format_items_table(items, serials, store_name)

    # Store-specific rewards and footer
    if store_name == "NetPro Tools":
        pts_str = f"NETPRO REWARDS: {int(grand * 5)} points\nSUPPORT LEVEL: {random.choice(['Gold', 'Platinum', 'Enterprise'])}\n" if show_points else ""
        sig_str = f"\n\n{'='*85}\nAUTHORIZED SIGNATURE: _________________________\nTITLE: _________________________\n" if include_sig else ""
        footer = f"\n" + "="*85 + f"\nSUBTOTAL:                           ${sub:>10,.2f}\nTAX ({TAX_RATE*100:.2f}%):                      ${tax:>10,.2f}\nTOTAL:                              ${grand:>10,.2f}\n" + "="*85 + f"\nPAYMENT TERMS: NET 30\nPAYMENT METHOD: {pay_method}\n{pts_str}RETURN POLICY: {STORES[store_name]['policy']}\nTECHNICAL SUPPORT: {STORES[store_name]['tech_support']}\nACCOUNT MANAGEMENT: {STORES[store_name]['customer_service']}\n{sig_str}\n"
    elif store_name == "Newegg":
        pts_str = f"NEWEGG PREMIER REWARDS: {int(grand * 10)} points\nMEMBER SINCE: 20{random.randint(10, 22)}\n" if show_points else ""
        sig_str = f"\n\n{'='*70}\nCUSTOMER SIGNATURE: _________________________\n" if include_sig else ""
        footer = f"\n" + "="*70 + f"\nSUBTOTAL:                 ${sub:>9,.2f}\nTAX ({TAX_RATE*100:.2f}%):            ${tax:>9,.2f}\nTOTAL:                    ${grand:>9,.2f}\n" + "="*70 + f"\nPAYMENT METHOD: {pay_method}\n{pts_str}RETURN POLICY: {STORES[store_name]['policy']}\nQUESTIONS: {STORES[store_name]['customer_service']}\n{sig_str}\n"
    elif store_name == "Apple Store":
        pts_str = f"APPLE REWARDS: {int(grand)} points\n" if show_points else ""
        sig_str = f"\n\n{'='*45}\nSignature\n" if include_sig else ""
        footer = f"\n" + "-"*45 + f"\nSubtotal: ${sub:>8,.2f}\nTax:      ${tax:>8,.2f}\nTotal:    ${grand:>8,.2f}\n" + "-"*45 + f"\nPaid with: {pay_method}\n{pts_str}{STORES[store_name]['policy']}{sig_str}\n"
    else:
        # Best Buy format (original)
        pts_str = f"REWARDS POINTS EARNED: {int(grand)}\nTOTAL BALANCE: {random.randint(2000, 5000)}\n" if show_points else ""
        sig_str = f"\n\nX______________________________\nCUSTOMER SIGNATURE\n" if include_sig else ""
        footer = f"\n" + "-"*50 + f"\nSUBTOTAL:      ${sub:>9,.2f}\nTAX (8.25%):   ${tax:>9,.2f}\nTOTAL:         ${grand:>9,.2f}\n" + "-"*50 + f"\nPAYMENT: {pay_method}\n{pts_str}{STORES[store_name]['policy']}{sig_str}\n"

    full_receipt = header + items_table + footer

    st.session_state['editable_content'] = full_receipt
    st.session_state['current_logo'] = STORES[store_name]["asset"]
    st.session_state['current_inv'] = inv_pretty
    st.session_state['temp_dir'] = temp_dir
    st.session_state['barcode_path'] = barcode_path + ".png"
    st.session_state['qr_path'] = qr_path
        
except Exception as e:
    st.error(f"Error generating receipt: {str(e)}")
    # Clean up temp directory on error
    if 'temp_dir' in locals() and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    st.stop()

if 'editable_content' in st.session_state:
    edited = st.text_area("Edit Receipt Text", st.session_state['editable_content'], height=400)
    
    try:
        pdf_bytes = create_pdf_bytes(
            edited,
            receipt_type,
            st.session_state.get('current_logo'),
            st.session_state.get('qr_path'),
            st.session_state.get('barcode_path')
        )
        
        st.download_button(
            "🖨️ Download PDF",
            pdf_bytes,
            f"Manifest_{st.session_state['current_inv']}.pdf"
        )

        # Safe HTML rendering with sanitization
        sanitized_content = html.escape(edited).replace('\n', '<br>')
        st.markdown(
            f'<div style="background:white; color:black; padding:15px; font-family:monospace; border:1px solid #ddd; width:300px; line-height:1.2; font-size:11px;">{sanitized_content}</div>',
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
    finally:
        # Clean up temporary files
        if 'temp_dir' in st.session_state and os.path.exists(st.session_state['temp_dir']):
            shutil.rmtree(st.session_state['temp_dir'], ignore_errors=True)
            del st.session_state['temp_dir']
