import os
from dotenv import load_dotenv
import resend
load_dotenv()
from markupsafe import escape
from supabase import create_client
from flask import Flask, render_template, request, redirect, session
from flask import send_from_directory
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)
resend.api_key = os.environ.get("RESEND_API_KEY")

COTTAGES = [
    {"location": "Levi", "apartment": "Aruudenia M", "week": 8, "type": "2mh+parvi", "beds": "6", "rent": 780, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Rakkavaara Club1 A1", "week": 8, "type": "2mh", "beds": "4+2", "rent": 690, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "13C2", "week": 8, "type": "1mh+parvi", "beds": "4+2", "rent": 890, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "2A2", "week": 8, "type": "2mh+parvi", "beds": "6", "rent": 1150, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "17C1", "week": 8, "type": "2mh", "beds": "4+2", "rent": 920, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "13B5", "week": 8, "type": "1mh+parvi", "beds": "4+2", "rent": 890, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "6A2", "week": 11, "type": "2mh+parvi", "beds": "6", "rent": 850, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Rakkavaara Club1 B1", "week": 11, "type": "1mh+parvi", "beds": "4+2", "rent": 730, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Rakkavaara Club LTD H4", "week": 13, "type": "1mh+parvi", "beds": "6", "rent": 720, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Aruudenia K", "week": 14, "type": "2mh+parvi", "beds": "6", "rent": 780, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Abcott D", "week": 14, "type": "2mh+parvi", "beds": "6", "rent": 800, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Rakkavaara Club1 B1", "week": 14, "type": "1mh+parvi", "beds": "4+2", "rent": 750, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Rakkavaara Club LTD H4", "week": 15, "type": "1mh+parvi", "beds": "6", "rent": 720, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Levi", "apartment": "Aruudenia M", "week": 15, "type": "2mh+parvi", "beds": "6", "rent": 750, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "13E1", "week": 27, "type": "1mh+parvi", "beds": "4+2", "rent": 720, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "20C11", "week": 27, "type": "2mh", "beds": "4", "rent": 720, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "10A1", "week": 28, "type": "1mh+parvi", "beds": "4", "rent": 750, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "12A2", "week": 28, "type": "3mh+parvi", "beds": "8", "rent": 1250, "sale": "", "extra": "Keila", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "13C5", "week": 29, "type": "1mh+parvi", "beds": "4+2", "rent": 750, "sale": "", "extra": "", "status": "Varattu"},
    {"location": "Katinkulta", "apartment": "12A2", "week": 29, "type": "3mh+parvi", "beds": "8", "rent": 1250, "sale": "", "extra": "", "status": "Varattu"},
    {"location": "Katinkulta", "apartment": "7A1", "week": 30, "type": "2mh+parvi", "beds": "6", "rent": 950, "sale": "", "extra": "14 Kylpylä", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "8F1", "week": 30, "type": "1mh+parvi", "beds": "4", "rent": 780, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "9I1", "week": 30, "type": "1mh+parvi", "beds": "4", "rent": 780, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "9C4", "week": 31, "type": "1mh+parvi", "beds": "4", "rent": 720, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "1D2", "week": 31, "type": "3mh+parvi", "beds": "8", "rent": 1250, "sale": "", "extra": "Keila", "status": "Varattu"},
    {"location": "Katinkulta", "apartment": "20B3", "week": 31, "type": "1mh", "beds": "2+2", "rent": 720, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "3F2", "week": 31, "type": "1mh+parvi", "beds": "4", "rent": 750, "sale": "", "extra": "", "status": "Vapaa"},
    {"location": "Katinkulta", "apartment": "14l1", "week": 52, "type": "", "beds": "", "rent": 750, "sale": "", "extra": "", "status": "Vapaa"},
]

DEFAULT_CONTACT = {"email": "lomaviikot@outlook.com"}

@app.route("/")
def home():

    # Vanhat koodissa olevat mökit
    old_cottages = [
        {**cottage, "contact": cottage.get("contact", DEFAULT_CONTACT)}
        for cottage in COTTAGES
    ]

    # Supabasessa olevat julkaistut mökit
    result = (
        supabase
        .table("cottages")
        .select("*")
        .eq("published", True)
        .eq("payment_status", "paid")
        .execute()
    )

    new_cottages = []

    for cottage in result.data:

        new_cottages.append({
            "location": cottage.get("location", ""),
            "apartment": cottage.get("apartment", ""),
            "week": cottage.get("week"),
            "type": cottage.get("type", ""),
            "beds": cottage.get("beds", ""),
            "rent": cottage.get("rent"),
            "sale": cottage.get("sale", ""),
            "extra": cottage.get("extra", ""),
            "status": cottage.get("status", "Vapaa"),

            "contact": {
                "name": cottage.get("contact_name"),
                "email": cottage.get("contact_email"),
                "phone": cottage.get("contact_phone")
            }
        })

    # Yhdistetään vanhat ja uudet
    cottages = old_cottages + new_cottages

    return render_template(
        "index.html",
        cottages=cottages
    )

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml")

@app.route("/lisaa-mokki", methods=["GET", "POST"])
def lisaa_mokki():

    if request.method == "POST":

        # Luodaan turvallinen satunnainen muokkaustunniste
        edit_token = secrets.token_urlsafe(32)

        cottage = {
            "location": request.form.get("location"),
            "apartment": request.form.get("apartment"),
            "week": int(request.form["week"]) if request.form.get("week") else None,
            "type": request.form.get("type"),
            "beds": request.form.get("beds"),
            "rent": float(request.form["rent"]) if request.form.get("rent") else None,
            "sale": request.form.get("sale"),
            "extra": request.form.get("extra"),
            "status": request.form.get("status") or "Vapaa",

            "contact_name": request.form.get("contact_name"),
            "contact_email": request.form.get("contact_email"),
            "contact_phone": request.form.get("contact_phone"),

            # Uusi ilmoitus odottaa ensin maksua
            "payment_status": "pending",
            "published": False,

            # Asiakas tarvitsee tämän myöhemmin ilmoituksen muokkaamiseen
            "edit_token": edit_token
        }

        result = supabase.table("cottages").insert(cottage).execute()

        if result.data:

            cottage_id = result.data[0]["id"]

            # Luodaan asiakkaalle helposti tunnistettava maksutunnus
            payment_code = "MOKKI-" + secrets.token_hex(3).upper()

            # Tallennetaan maksutunnus Supabaseen
            supabase.table("cottages").update({
                "payment_code": payment_code
            }).eq("id", cottage_id).execute()

            return render_template(
                "payment.html",
                cottage_id=cottage_id,
                payment_code=payment_code,
                cottage=cottage
            )

        return "Mökin tallentaminen epäonnistui."

    return render_template("add_cottage.html")

@app.route("/admin/mokit")
def admin_mokit():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    result = (
        supabase
        .table("cottages")
        .select("*")
        .eq("payment_status", "pending")
        .order("created_at", desc=True)
        .execute()
    )

    cottages = result.data

    return render_template(
        "admin_mokit.html",
        cottages=cottages
    )


@app.route("/admin/hyvaksy/<int:cottage_id>", methods=["POST"])
def hyvaksy_mokki(cottage_id):

    # Haetaan mökki
    result = (
        supabase
        .table("cottages")
        .select("*")
        .eq("id", cottage_id)
        .single()
        .execute()
    )

    cottage = result.data

    if not cottage:
        return "Mökkiä ei löytynyt.", 404

    # Julkaistaan mökki
    (
        supabase
        .table("cottages")
        .update({
            "payment_status": "paid",
            "published": True
        })
        .eq("id", cottage_id)
        .execute()
    )

    # Muokkauslinkki
    edit_link = (
        "http://127.0.0.1:5000/"
        "muokkaa-mokkia/"
        + cottage["edit_token"]
    )

    # Lähetetään sähköposti
    try:

        resend.Emails.send({
            "from": "Viikkolomat <no-reply@viikkolomat.com>",
            "to": cottage["contact_email"],
            "subject": "Mökkisi on julkaistu – Viikkolomat",
            "html": f"""
            <!DOCTYPE html>
            <html lang="fi">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>

            <body style="
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
            ">

                <div style="
                    max-width: 600px;
                    margin: 30px auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                ">

                    <div style="
                        padding: 30px;
                        text-align: center;
                        background: #111827;
                        color: white;
                    ">

                        <h1 style="margin: 0;">
                            Viikkolomat
                        </h1>

                        <p style="margin-bottom: 0;">
                            Mökkisi on julkaistu
                        </p>

                    </div>

                    <div style="padding: 30px;">

                        <h2>
                            Hei {escape(cottage["contact_name"] or "asiakas")}!
                        </h2>

                        <p>
                            Maksusi on vastaanotettu ja mökkisi on nyt
                            julkaistu Viikkolomat-sivustolla.
                        </p>

                        <div style="
                            background: #f3f4f6;
                            padding: 20px;
                            border-radius: 8px;
                            margin: 25px 0;
                        ">

                            <h3 style="margin-top: 0;">
                                {escape(cottage["apartment"])}
                            </h3>

                            <p>
                                <strong>Sijainti:</strong>
                                {escape(cottage["location"])}
                            </p>

                            <p>
                                <strong>Viikko:</strong>
                                {escape(cottage["week"] or "-")}
                            </p>

                            <p>
                                <strong>Vuokra:</strong>
                                {escape(cottage["rent"] or "-")} €
                            </p>

                        </div>

                        <p>
                            Voit myöhemmin muuttaa ilmoituksesi tietoja
                            tämän henkilökohtaisen linkin kautta:
                        </p>

                        <div style="text-align: center; margin: 30px 0;">

                            <a href="{edit_link}"
                            style="
                                display: inline-block;
                                padding: 14px 24px;
                                background: #111827;
                                color: white;
                                text-decoration: none;
                                border-radius: 8px;
                                font-weight: bold;
                            ">
                                Muokkaa ilmoitusta
                            </a>

                        </div>

                        <p style="font-size: 14px; color: #666;">
                            Säilytä tämä sähköposti. Linkki on henkilökohtainen
                            ja sen avulla voit muokata ilmoitustasi.
                        </p>

                        <hr style="
                            border: 0;
                            border-top: 1px solid #ddd;
                            margin: 30px 0;
                        ">

                        <p style="
                            font-size: 13px;
                            color: #777;
                            text-align: center;
                        ">
                            Viikkolomat<br>
                            Tämä on automaattisesti lähetetty viesti.
                        </p>

                    </div>

                </div>

            </body>
            </html>
            """
        })

    except Exception as e:

        return f"""
            <h1>Mökki julkaistiin, mutta sähköposti epäonnistui.</h1>
            <p>{e}</p>
        """, 500

    return redirect("/admin/mokit")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form.get("password")

        if password == os.environ.get("ADMIN_PASSWORD"):

            session["admin_logged_in"] = True

            return redirect("/admin/mokit")

        return "Väärä salasana", 401

    return render_template("admin_login.html")

@app.route("/muokkaa-mokkia/<edit_token>", methods=["GET", "POST"])
def muokkaa_mokkia(edit_token):

    # Haetaan mökki tokenin perusteella
    result = (
        supabase
        .table("cottages")
        .select("*")
        .eq("edit_token", edit_token)
        .single()
        .execute()
    )

    cottage = result.data

    if not cottage:
        return "Ilmoitusta ei löytynyt.", 404

    # Kun asiakas tallentaa muutokset
    if request.method == "POST":

        updates = {
            "location": request.form.get("location"),
            "apartment": request.form.get("apartment"),
            "week": int(request.form["week"]) if request.form.get("week") else None,
            "type": request.form.get("type"),
            "beds": request.form.get("beds"),
            "rent": float(request.form["rent"]) if request.form.get("rent") else None,
            "sale": request.form.get("sale"),
            "extra": request.form.get("extra"),
            "status": request.form.get("status"),
            "contact_name": request.form.get("contact_name"),
            "contact_email": request.form.get("contact_email"),
            "contact_phone": request.form.get("contact_phone")
        }

        (
            supabase
            .table("cottages")
            .update(updates)
            .eq("edit_token", edit_token)
            .execute()
        )

        return "Muutokset tallennettu!"

    return render_template(
        "edit_cottage.html",
        cottage=cottage
    )

@app.route("/test-email")
def test_email():

    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "heinoseveri@gmail.com",
            "subject": "Viikkolomat – testiviesti",
            "html": """
                <h1>Testi onnistui!</h1>
                <p>Viikkolomat-sivuston sähköpostien lähetys toimii.</p>
            """
        })

        return "Sähköposti lähetetty!"

    except Exception as e:
        return f"Sähköpostin lähetys epäonnistui: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)