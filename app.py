from flask import Flask, send_file, render_template, redirect, url_for, Response
import qrcode
import io

app = Flask(__name__)

CONTACT_DATA = {
    "name": "Sai Jarugula",
    "phone": "+1 (203)570-2728",
    "company": "Suthra Technologies"
}

def generate_vcard_text():
    return f"""BEGIN:VCARD
VERSION:3.0
FN:{CONTACT_DATA['name']}
ORG:{CONTACT_DATA['company']}
TEL;TYPE=CELL:{CONTACT_DATA['phone']}
END:VCARD
"""

@app.route("/")
def home():
    # Redirect root to the default contact page (prevents 404 on /)
    return redirect(url_for("contact_page", id=1))

@app.route("/contact")
def contact_redirect():
    return redirect(url_for("contact_page", id=1))


@app.route("/contact/<id>")
def contact_page(id):
    return render_template("contact.html", name=CONTACT_DATA['name'])

@app.route("/download_vcf/<id>")
def download_vcf(id):
    # Generate vCard in memory and stream it
    vcard_text = generate_vcard_text()
    vcard_bytes = vcard_text.encode("utf-8")
    vcard_io = io.BytesIO(vcard_bytes)
    vcard_io.seek(0)

    # As discussed: as_attachment=False so most phones open the contact preview
    # Use mimetype that works well across Android/iOS
    return send_file(
        vcard_io,
        as_attachment=False,
        download_name="contact.vcf",
        mimetype="text/x-vcard"
    )

from flask import request

@app.route("/generate_qr")
def generate_qr():
    base_url = request.host_url.rstrip("/")
    url = f"{base_url}/contact/1"

    qr = qrcode.make(url)
    qr_io = io.BytesIO()
    qr.save(qr_io, "PNG")
    qr_io.seek(0)
    return send_file(qr_io, mimetype="image/png")

@app.route("/qr")
def qr_page():
    return render_template("qr.html")






