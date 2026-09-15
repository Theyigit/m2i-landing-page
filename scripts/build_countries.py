#!/usr/bin/env python3
"""
Builds src/data/country-guides.json: one "Moving to Ireland from X" guide per
country, from the facts table in scripts/countries/facts.py and the editorial
passages in scripts/countries/prose.json.

These guides are website-only (they are not bundled in the app), so the site
publishes them in full rather than behind the app gate. The nine in-depth
country guides that ARE in the app (US, UK, India, ...) come from
build_content.py like every other guide; this script skips any country that
already has one of those.

    python3 scripts/build_countries.py
"""

import json
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "countries"))
from facts import COUNTRIES, REGIONS  # noqa: E402

OUT = HERE.parent / "src/data/country-guides.json"
PROSE = json.loads((HERE / "countries/prose.json").read_text(encoding="utf-8"))
APP_GUIDES = json.loads((HERE.parent / "src/data/guides.json").read_text(encoding="utf-8"))
IN_APP = {
    a["slug"] for c in APP_GUIDES["categories"] if c["slug"] == "moving-from" for a in c["articles"]
}

# Figures shared with the hand-written country guides in the app; keep in step.
CSEP_MIN = "40,904 euro"
CSEP_OTHER = "68,911 euro"
GEP_MIN = "36,605 euro"
PERMIT_DATE = "1 March 2026"
IRP_FEE = "300 euro"
NDLS_FEE = "65 euro"

# Countries whose residents commonly face exchange controls on taking money out.
EXCHANGE_CONTROLS = {
    "algeria", "angola", "argentina", "bangladesh", "china", "cuba", "egypt", "ethiopia",
    "ghana", "iran", "lebanon", "morocco", "myanmar", "nepal", "pakistan", "sri-lanka",
    "tunisia", "venezuela", "zimbabwe", "uzbekistan", "turkmenistan", "belarus", "russia",
}


def p(text: str) -> str:
    return f"<p>{text}</p>"


def h2(text: str) -> str:
    return f"<h2>{escape(text)}</h2>"


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def table(rows: list[tuple[str, str]], head: tuple[str, str]) -> str:
    body = f"<tr><td><strong>{head[0]}</strong></td><td><strong>{head[1]}</strong></td></tr>"
    body += "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td></tr>" for a, b in rows)
    return f'<div class="scroll-x"><table>{body}</table></div>'


def link(href: str, text: str) -> str:
    return f'<a href="{href}" rel="nofollow noopener" target="_blank">{escape(text)}</a>'


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def build(c: dict) -> dict:
    name, adj, cur = c["name"], c["adjective"], c["currency"]
    Name = cap(name)  # "the Netherlands" at the start of a sentence
    prose = PROSE[c["slug"]]
    eea = c["visa"] == "eea"
    ukraine = c["visa"] == "ukraine"
    free = c["visa"] == "free"
    required = c["visa"] == "required"
    blocks: list[tuple[str, str]] = []  # (kind, html)

    def add(kind: str, html: str) -> None:
        blocks.append((kind, html))

    # --- Intro and quick facts --------------------------------------------
    add("p", p(prose["intro"]))

    visa_cell = (
        "No: EU free movement" if eea
        else "No, up to 90 days" if free
        else "No for biometric passport holders" if ukraine
        else "Yes, long stay D visa"
    )
    stay_cell = (
        "No permit or registration needed" if eea
        else "Temporary protection or a permit" if ukraine
        else "Yes, needs a permit or scheme, then an IRP"
    )
    licence_cell = (
        "Drive on it, swap it when it expires" if c["licence"] == "eu"
        else "Yes, exchange without a test" if c["licence"] == "exchange"
        else "Yes, under temporary protection rules" if c["licence"] == "ukraine"
        else "No"
    )
    dta_cell = "Yes" if c["dta"] == 1 else "Signed, partly suspended by Russia" if c["dta"] == "suspended" else "No"
    ssa_cell = "Yes, via EU rules" if eea else ("Yes, bilateral agreement" if c["ssa"] else "No")
    rows = [
        ("Visa to enter", visa_cell),
        ("Permission to stay beyond 90 days", stay_cell),
        (f"{adj} licence exchangeable", licence_cell),
        ("Double taxation agreement", dta_cell),
        ("Social security agreement", ssa_cell),
    ]
    if c["wha"]:
        rows.append(("Working Holiday Authorisation", "Yes"))
    rows.append((
        "Pets",
        "EU pet passport" if c["pets"] == "eu"
        else "Listed country, no blood test" if c["pets"] == "listed"
        else "Unlisted country, rabies blood test",
    ))
    add("table", table(rows, ("Quick facts", f"{Name} to Ireland")))

    # --- Visa -------------------------------------------------------------
    add("h", h2("Do you need a visa?"))
    if eea:
        who = "Swiss citizens have the same rights under the EU–Swiss agreement" if c["slug"] == "switzerland" else (
            "EEA citizens have the same rights as EU citizens" if c["slug"] in ("norway", "iceland") else
            "as an EU citizen you have the right to free movement"
        )
        add("p", p(
            f"No. {cap(who)}: you can enter Ireland with a passport or national identity card, look for work, take a job, "
            f"study or set up a business without a visa, an employment permit or any registration with immigration. "
            f"There is no Irish Residence Permit for EU, EEA and Swiss citizens. After three months you are expected to be "
            f"working, self-employed, studying, or able to support yourself, but nobody checks at a desk; it only comes up "
            f"if you later apply for something like citizenship."
        ))
        add("p", p(
            f"The picture changes for family. A spouse, partner or dependent parent who is not an EU, EEA or Swiss citizen "
            f"can join you under <strong>EU Treaty Rights</strong>: they may need a visa to enter, and once here they apply to "
            f"Immigration Service Delivery for a residence card (form EU1) within their first months, which gives them "
            f"<strong>Stamp 4 EU FAM</strong> and the right to work. Applying early matters because the card can take months."
        ))
        add("p", p(
            f"If you have an Irish parent or grandparent you may already be entitled to Irish citizenship through the "
            f"<strong>Foreign Births Register</strong>. It changes nothing about your right to live here, but an Irish "
            f"passport is handy for family members and for voting."
        ))
    elif ukraine:
        add("p", p(
            f"Ukrainian citizens with a biometric passport can enter Ireland without a visa. Most people who have arrived "
            f"since 2022 are here under the <strong>EU Temporary Protection Directive</strong>, which Ireland applies in "
            f"full: registration at the airport or at a Department of Justice centre gives you a <strong>Stamp 4</strong> "
            f"style permission with the right to work, study and access public services, currently extended by the EU to "
            f"March 2027. You do not need an employment permit while under temporary protection."
        ))
        add("p", p(
            f"If you are moving for a job rather than under protection, the ordinary routes apply: a <strong>Critical Skills "
            f"Employment Permit</strong> for roles on the critical skills list (minimum salary {CSEP_MIN} from {PERMIT_DATE}, "
            f"or {CSEP_OTHER} for other eligible roles), a <strong>General Employment Permit</strong> (minimum {GEP_MIN}), "
            f"a study permission (Stamp 2), or family routes. Register for an <strong>Irish Residence Permit</strong> "
            f"({IRP_FEE}) within 90 days of arriving."
        ))
    else:
        if free:
            add("p", p(
                f"{adj} citizens are <strong>not visa required</strong>, so you can enter Ireland for up to 90 days without "
                f"applying for anything. Staying longer is a different matter: you need an immigration permission before "
                f"the 90 days run out, and you cannot turn a visit into a job from inside the country except through a "
                f"handful of schemes. Get the permit or the college place sorted first, then travel. Ireland has added "
                f"visa requirements for several countries since 2022, so check the current list on irishimmigration.ie "
                f"before you book."
            ))
        else:
            add("p", p(
                f"Yes. {adj} citizens are <strong>visa required</strong>, so you need an Irish visa before you travel and "
                f"then an immigration permission to stay. For a move the visa is a <strong>long stay D visa</strong>, "
                f"applied for online through AVATS and submitted with your passport and documents to the Irish embassy "
                f"or visa office that covers {name}, or through its VFS partner where one is used. Allow at least eight "
                f"weeks. The visa gets you to the border; your permission to live here comes from the permit, course or "
                f"family relationship behind it. You cannot enter on a short stay C visa and switch to a work permission "
                f"from inside Ireland."
            ))
        routes = [
            f"<strong>Critical Skills Employment Permit</strong> for jobs on the critical skills list (from {PERMIT_DATE} "
            f"the minimum salary is {CSEP_MIN}, or {CSEP_OTHER} for other eligible roles). Spouses and partners can join you "
            f"and work on Stamp 1G without their own permit, and you can apply for Stamp 4 after two years.",
            f"<strong>General Employment Permit</strong> for most other jobs, minimum salary {GEP_MIN} from {PERMIT_DATE}, "
            f"usually after the employer runs a labour market needs test. Healthcare assistants, home carers, chefs and "
            f"construction trades come in on this permit.",
            "<strong>Stamp 2 study permission</strong> for a degree or a recognised English language course, with the "
            "right to work 20 hours a week in term time (40 in the holidays). Graduates of Irish degrees get the "
            "<strong>Third Level Graduate Programme</strong> (Stamp 1G) to look for work for one to two years.",
            "<strong>Family</strong> routes if you are joining an Irish citizen, an EU citizen exercising treaty rights, "
            "or a permit holder.",
        ]
        if c["wha"]:
            routes.insert(2,
                f"<strong>Working Holiday Authorisation</strong>: Ireland has a working holiday agreement with {name}, "
                f"which lets young {adj} citizens (typically 18 to 30 or 35) live and work in Ireland for up to 12 months "
                f"without a job offer. Apply through the Irish embassy that covers {name}; places are limited each year."
            )
        if free:
            routes.append(
                "<strong>Stamp 0</strong> for retirees and people of independent means, with income of around 50,000 euro "
                "a year per person and private medical insurance, and no right to work."
            )
        add("ul", ul(routes))
        add("p", p(
            f"Whichever route you take, you must register for an <strong>Irish Residence Permit</strong> ({IRP_FEE}) "
            f"within 90 days of arriving: online in Dublin, or at the local Garda immigration office elsewhere. If you have an "
            f"Irish born parent or grandparent, check the <strong>Foreign Births Register</strong> first, because once "
            f"registered you are an Irish citizen and none of the above applies."
        ))

    # --- Work and qualifications -----------------------------------------
    add("h", h2("Finding work and getting your qualifications recognised"))
    add("p", p(prose["language"]))
    if eea:
        add("p", p(
            "You can apply for jobs from home and start the week you land. Irish CVs run to two pages, carry no photo "
            "and no date of birth, and lead with what you did rather than your job title. Most hiring runs through "
            "LinkedIn, IrishJobs, Jobs.ie and the employers' own sites, with recruitment agencies strong in tech, "
            "finance and pharma. EU qualifications are recognised under EU rules, so a nurse, doctor, teacher or "
            "engineer registers with the Irish body without re-qualifying, though registration itself takes weeks to months."
        ))
    else:
        add("p", p(
            "Because most routes need a job offer first, the search happens from home. Irish CVs run to two pages, "
            "carry no photo and no date of birth, and lead with what you did rather than your job title. Most hiring "
            "runs through LinkedIn, IrishJobs, Jobs.ie and the employers' own sites; agencies are strong in tech, "
            "finance, pharma and healthcare, and employers used to sponsoring permits say so in the advert. "
            "Get your degree assessed by <strong>NARIC Ireland</strong> (free, through QQI) before you apply; it maps a "
            f"{adj} qualification onto the Irish framework and employers recognise the letter. Regulated professions "
            "register with their own body: nurses with NMBI, doctors with the Medical Council, teachers with the "
            "Teaching Council, engineers with Engineers Ireland, and physiotherapists, radiographers and social workers "
            "with CORU. Those bodies, not employers, are the ones that ask for an English test."
        ))

    # --- Driving licence ---------------------------------------------------
    add("h", h2("Your driving licence"))
    if c["licence"] == "eu":
        add("p", p(
            f"A full {adj} licence is an EU or EEA licence, so you can keep driving on it in Ireland for as long as it is "
            f"valid; there is no exchange deadline. Most people swap it for an Irish licence when it expires or when they "
            f"want a local card for identification, which the NDLS does without a test for {NDLS_FEE}. Apply online at "
            f"ndls.ie with a Public Services Card and MyGovID, or book an NDLS centre appointment with the licence, proof "
            f"of your PPS number, proof of address and photo ID. Once you exchange it, Irish rules apply: a lifetime "
            f"licence becomes a ten year one, and category B does not include the trailers or motorcycles it may have "
            f"covered at home."
        ))
    elif c["licence"] == "exchange":
        add("p", p(
            f"{Name} is on the <strong>NDLS list of recognised states</strong>, so a full {adj} licence can be exchanged "
            f"for an Irish one without a theory or driving test. You can drive on the {adj} licence for up to 12 months "
            f"after becoming resident, then you must exchange it. Apply online at ndls.ie if you have a Public Services "
            f"Card and MyGovID, or book an NDLS centre appointment. Bring the licence, a certified English translation if "
            f"it is not in English, proof of your PPS number, proof of address and photo ID; you may also need a letter "
            f"of entitlement from the issuing authority. The fee is {NDLS_FEE}, and the exchanged licence covers the "
            f"categories that match Irish ones."
        ))
    elif c["licence"] == "ukraine":
        add("p", p(
            "Ukraine is not on the ordinary NDLS list of recognised states, but under the temporary protection "
            "arrangements Ukrainian licence holders can exchange a full Ukrainian licence for an Irish one without a "
            "test, with a certified translation. If you are here on an employment permit rather than temporary "
            "protection, check with the NDLS whether the exchange applies to you; otherwise you can drive for up to 12 "
            "months as a visitor and then go through the Irish process of theory test, learner permit, Essential "
            "Driver Training and driving test."
        ))
    else:
        add("p", p(
            f"{Name} is <strong>not on the NDLS list of recognised states</strong>, so you cannot swap a {adj} licence "
            f"for an Irish one. You can drive on your {adj} licence for up to 12 months as a visitor, ideally with an "
            f"International Driving Permit, but once you are resident you must go through the Irish process: pass the "
            f"driver theory test, get a learner permit, complete Essential Driver Training and pass the driving test. "
            f"The good news is that experienced foreign licence holders only need <strong>6 EDT lessons instead of 12</strong> "
            f"and can skip the usual six month wait before the test. Learner permit holders must be accompanied by a "
            f"full licence holder, which is the part that catches people out. Remember that Ireland drives on the left."
        ))

    # --- Tax, pensions and money ------------------------------------------
    add("h", h2("Tax, pensions and money"))
    if c["dta"] == 1:
        add("p", p(
            f"Ireland and {name} have a <strong>double taxation agreement</strong>, so income taxed in one country is "
            f"generally credited in the other and the treaty decides which country taxes what. You become Irish tax "
            f"resident after 183 days in a tax year (or 280 days over two years), and from then Ireland taxes your "
            f"worldwide income, with credit for {adj} tax under the treaty. Register with Revenue through myAccount as "
            f"soon as you have a PPS number so your employer taxes you correctly, and tell the {adj} tax authority that "
            f"you are leaving."
        ))
    elif c["dta"] == "suspended":
        add("p", p(
            f"Ireland and Russia signed a double taxation agreement, but in August 2023 Russia suspended key articles of "
            f"its treaties with countries it lists as unfriendly, including Ireland. Take professional advice before you "
            f"rely on any treaty relief. You become Irish tax resident after 183 days in a tax year (or 280 days over two "
            f"years), and from then Ireland taxes your worldwide income; register with Revenue through myAccount as soon "
            f"as you have a PPS number."
        ))
    else:
        add("p", p(
            f"Ireland and {name} have <strong>no double taxation agreement</strong>. For most people this matters less "
            f"than it sounds: once you become Irish tax resident (183 days in a tax year, or 280 over two) and your job is "
            f"here, Irish PAYE applies to your salary and your {adj} tax obligations usually end with your residence "
            f"there. It matters if you keep {adj} income, such as rent or a business, which could be taxed in both "
            f"countries; Revenue may grant unilateral relief for foreign tax paid, and a tax adviser is worth it in that "
            f"case. Register with Revenue through myAccount as soon as you have a PPS number."
        ))
    if eea:
        add("p", p(
            f"Social security follows the <strong>EU coordination rules</strong>. You pay into one system at a time, your "
            f"{adj} contribution record and Irish PRSI record are combined to qualify for a state pension in either "
            f"country, and each country pays its share when you retire. If your employer is posting you to Ireland "
            f"temporarily, an A1 certificate keeps you in the {adj} system. Occupational and private pensions can "
            f"generally stay where they are."
        ))
    elif c["ssa"]:
        add("p", p(
            f"There is a <strong>bilateral social security agreement</strong> between Ireland and {name}. It lets you "
            f"combine {adj} contributions with Irish PRSI to qualify for a state pension in either country, protects "
            f"workers posted temporarily from paying into both systems, and allows pensions to be paid abroad. "
            f"Occupational and private pensions can generally stay where they are; transfers to Irish schemes are "
            f"possible but need advice."
        ))
    else:
        add("p", p(
            f"There is <strong>no social security agreement</strong> between Ireland and {name}, so the two records stand "
            f"alone. You need at least 520 paid PRSI contributions (ten years) to qualify for any Irish State Pension "
            f"(Contributory), and the full rate takes 40 years of contributions. Check whether your {adj} state pension "
            f"can be paid to you in Ireland, and whether you can keep contributing voluntarily from abroad."
        ))
    money = (
        f"Your credit history does not follow you. Irish lenders only see the Central Credit Register, so expect to "
        f"build a record from scratch before a mortgage or car loan. "
    )
    if c["currency"] != "the euro":
        money += (
            f"Moving money from {cur} into euro is cheapest through a specialist transfer provider rather than a bank; "
            f"open the Irish account first, because you need an Irish IBAN to receive salary. "
        )
    else:
        money += "Being in the euro area spares you exchange costs, and SEPA transfers from home arrive the next day. "
    if c["slug"] in EXCHANGE_CONTROLS:
        money += (
            f"{Name} has exchange controls, so check what you are allowed to take out and the paperwork needed before "
            f"you leave, and bring evidence of the source of funds for the Irish bank."
        )
    add("p", p(money.strip()))

    # --- Healthcare -------------------------------------------------------
    add("h", h2("Healthcare"))
    if eea:
        add("p", p(
            f"Your European Health Insurance Card covers you as a visitor, not as a resident. Once you are ordinarily "
            f"resident (living in Ireland or intending to for at least a year) you use public hospitals as a public "
            f"patient, and inpatient charges were abolished in April 2023. The HSE is not free at the point of use the way "
            f"many {adj} services are: a GP visit costs roughly 50 to 70 euro unless you qualify for a medical card or GP "
            f"visit card on income grounds (children under 8 and people over 70 get GP visits free), and prescriptions "
            f"are paid for up to a monthly cap under the Drugs Payment Scheme. If your employer is posting you here on an "
            f"A1, an S1 form registers you with the HSE at {adj} expense."
        ))
    else:
        add("p", p(
            f"Ireland has a public system run by the HSE, but it is not free at the point of use. Once you are ordinarily "
            f"resident (living in Ireland or intending to for at least a year) you use public hospitals as a public "
            f"patient, and inpatient charges were abolished in April 2023. A GP visit costs roughly 50 to 70 euro unless "
            f"you qualify for a medical card or GP visit card on income grounds (children under 8 get GP visits free), "
            f"and prescriptions are paid for up to a monthly cap under the Drugs Payment Scheme. Emergency departments "
            f"charge 100 euro without a GP referral. Students, Stamp 0 holders and most visa applicants must show private "
            f"medical insurance, so many people arrive with a policy already."
        ))
    add("p", p(
        "Around half the population holds private health insurance from VHI, Laya or Irish Life Health, mainly to "
        "shorten waiting lists. If you are 35 or older, buy it within 9 months of arriving to avoid a Lifetime Community "
        "Rating loading. Register with a GP as soon as you have an address; practices in Dublin often have closed lists, "
        "so ask several."
    ))

    # --- Things and pets --------------------------------------------------
    add("h", h2("Bringing your things and your pet"))
    if eea:
        add("p", p(
            f"Goods move freely inside the EU, so a removals van from {name} clears no customs. A car registered in "
            f"{name} must be registered for Vehicle Registration Tax within 30 days of arrival; VRT relief applies if you "
            f"owned and used the car for at least 6 months abroad and are moving your normal residence to Ireland, and "
            f"you then need Irish insurance, motor tax and an NCT."
        ))
        add("p", p(
            "Pets travel on an <strong>EU pet passport</strong>: a microchip, a rabies vaccination given at least 21 "
            "days before travel, and for dogs a tapeworm treatment by a vet 24 to 120 hours before arrival, which "
            "Ireland requires because it is free of the tapeworm. Ferries and airlines carry pets on set routes, and "
            "the animal is checked on arrival."
        ))
    else:
        add("p", p(
            f"Goods arriving from {name} are imports from outside the EU. You can bring your household belongings free of "
            f"duty and VAT under <strong>Transfer of Residence relief</strong> if you have lived outside the EU for at "
            f"least 12 months and owned the goods for at least 6 months; your removals company files the declaration and "
            f"you cannot sell the goods for a year. A car qualifies for VRT relief on the same terms, but shipping a car "
            f"from {name} rarely makes sense once freight, registration and Irish insurance are added up."
        ))
        if c["pets"] == "listed":
            add("p", p(
                f"{Name} is a <strong>listed country</strong> under the EU pet rules, so no rabies blood test is needed. "
                f"Your dog, cat or ferret needs a microchip, a rabies vaccination given at least 21 days before travel, an "
                f"EU animal health certificate issued by an official vet within 10 days of travel, and for dogs a tapeworm "
                f"treatment 24 to 120 hours before arrival. Pets from outside the EU must arrive as manifest cargo or with "
                f"an approved airline on an approved route (Dublin Airport handles most), and are checked on arrival."
            ))
        else:
            add("p", p(
                f"{Name} is an <strong>unlisted country</strong> under the EU pet rules, which adds a blood test. Your dog, "
                f"cat or ferret needs a microchip, then a rabies vaccination, then a rabies antibody titre test at least 30 "
                f"days after the vaccination at an EU approved laboratory, and then a <strong>three month wait</strong> from "
                f"the date of the blood sample before travel. Add an EU animal health certificate issued within 10 days of "
                f"travel and, for dogs, a tapeworm treatment 24 to 120 hours before arrival. Pets must arrive as manifest "
                f"cargo or with an approved airline on an approved route (Dublin Airport handles most). Start the process "
                f"at least four months before you fly."
            ))

    # --- Community and daily life ----------------------------------------
    add("h", h2("Settling in: community and daily life"))
    add("p", p(prose["community"]))
    add("p", p(prose["contrast"]))
    if c["direct"]:
        flights = (
            f"Getting home is straightforward: there are direct flights between Dublin and {name}"
            + (", and Cork and Shannon add more routes in summer." if eea else ".")
        )
    else:
        hubs = {
            "europe": "London, Frankfurt, Vienna, Istanbul or Warsaw",
            "mena": "London, Paris, Istanbul, Doha or Dubai",
            "africa": "London, Paris, Amsterdam, Istanbul, Addis Ababa, Doha or Dubai",
            "asia": "Dubai, Doha, Abu Dhabi, Istanbul, London or Amsterdam",
            "oceania": "Dubai, Doha, Singapore or Los Angeles",
            "americas": "London, Madrid, Lisbon, Paris, Amsterdam or a North American hub",
            "eu": "a European hub",
        }[c["region"]]
        flights = (
            f"There are no regular direct flights between Dublin and {name}, so getting home usually means one stop, "
            f"most often via {hubs}; budget for the time as well as the fare."
        )
    add("p", p(flights))

    # --- Checklist --------------------------------------------------------
    add("h", h2("First 30 days checklist"))
    steps = ["Apply for a PPS number through MyWelfare.ie with your passport and proof of Irish address."]
    if eea:
        steps.append("No IRP is needed. Register with Revenue myAccount once you have a PPS number so your employer can tax you correctly.")
    elif ukraine:
        steps.append("Register for temporary protection on arrival if that is your route, or book your IRP registration within 90 days if you are on a permit.")
        steps.append("Register with Revenue myAccount once you have a PPS number.")
    else:
        steps.append(f"Register for your Irish Residence Permit within 90 days ({IRP_FEE}); book the appointment the week you land because slots fill up.")
        steps.append("Register with Revenue myAccount once you have a PPS number so your employer can tax you correctly.")
    steps.append("Open an Irish bank account; a utility bill, tenancy agreement or employer letter usually counts as proof of address.")
    steps.append("Register with a GP and, if you want it, buy private health insurance within 9 months.")
    if c["licence"] == "eu":
        steps.append("Get a Leap card for public transport; your licence needs nothing until it expires.")
    elif c["licence"] in ("exchange", "ukraine"):
        steps.append("Get a Leap card for public transport and book your licence exchange at the NDLS before the 12 months are up.")
    else:
        steps.append("Get a Leap card for public transport and book the driver theory test if you plan to drive.")
    if c["pets"] == "unlisted":
        steps.append("If a pet is following later, get its rabies blood test done now so the three month clock is running.")
    add("ul", ul(steps))

    # --- Links ------------------------------------------------------------
    add("h", h2("★ Useful links"))
    links = []
    if eea:
        links.append(link("https://www.citizensinformation.ie/en/moving-country/moving-to-ireland/rights-of-residence-in-ireland/residence-rights-eu-nationals/", "Citizens Information: residence rights of EU nationals"))
        links.append(link("https://www.irishimmigration.ie/coming-to-join-family-in-ireland/joining-an-eea-or-swiss-national/", "Immigration Service Delivery: family members of EU citizens"))
    else:
        links.append(link("https://www.irishimmigration.ie/", "Immigration Service Delivery: visas and permissions"))
        links.append(link("https://enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/", "Employment permits"))
        links.append(link("https://www.qqi.ie/what-we-do/qualifications-recognition", "NARIC Ireland: qualification recognition"))
    links.append(link("https://www.ndls.ie/", "National Driver Licence Service"))
    links.append(link("https://www.revenue.ie/en/life-events-and-personal-circumstances/moving-to-or-from-ireland/index.aspx", "Revenue: moving to Ireland"))
    if c["ssa"] or eea:
        links.append(link("https://www.gov.ie/en/publication/2ab84-bilateral-social-security-agreements/", "Bilateral social security agreements and EU rules"))
    links.append(link("https://www.gov.ie/en/service/1b1e5-bringing-your-pet-to-ireland/", "Department of Agriculture: bringing your pet to Ireland"))
    links.append(link("https://www.hia.ie/", "Health Insurance Authority"))
    add("ul", ul(links))

    # --- Assemble ---------------------------------------------------------
    html = "\n".join(b[1] for b in blocks)
    text_blocks = [re.sub(r"<[^>]+>", "", b[1]) for b in blocks]
    plain = "\n\n".join(t.strip() for t in text_blocks if t.strip())
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    sections = [re.sub(r"<[^>]+>", "", b[1]) for b in blocks if b[0] == "h"]

    facts = []
    facts.append(
        "EU free movement, no visa or permit" if eea
        else "visa-free entry then a permit" if free
        else "temporary protection or a permit" if ukraine
        else "D visa and a permit"
    )
    facts.append(
        "licence valid as is" if c["licence"] == "eu"
        else "licence exchange" if c["licence"] in ("exchange", "ukraine")
        else "no licence exchange"
    )
    facts.append("tax treaty" if c["dta"] == 1 else "no tax treaty")
    facts.append("pension agreement" if (c["ssa"] or eea) else "no pension agreement")
    if c["wha"]:
        facts.append("working holiday route")
    note = cap(", ".join(facts)) + "."
    # Like the app guides: the opening of the article, cut at a word near 155 chars.
    intro_text = re.sub(r"\s+", " ", prose["intro"]).strip()
    description = intro_text if len(intro_text) <= 155 else intro_text[:155].rsplit(" ", 1)[0].rstrip(",;:") + "\u2026"

    return {
        "slug": f"moving-to-ireland-from-{c['slug']}",
        "title": f"Moving to Ireland from {name}",
        "appTitle": f"Moving to Ireland from {name}",
        "note": note,
        "audience": [],
        "description": description,
        "wordCount": words,
        "readMinutes": max(1, round(words / 220)),
        "previewWordCount": words,
        "previewShare": 1,
        "previewHtml": html,
        "gatedHtml": "",
        "plainText": plain,
        "sections": sections,
        "inApp": False,
        "region": c["region"],
        "regionName": REGIONS[c["region"]],
        "country": name,
    }


def main() -> None:
    missing = [c["slug"] for c in COUNTRIES if c["slug"] not in PROSE]
    if missing:
        sys.exit(f"no prose for: {', '.join(missing)}")
    articles = []
    for c in COUNTRIES:
        if f"moving-to-ireland-from-{c['slug']}" in IN_APP:
            continue
        articles.append(build(c))
    words = sum(a["wordCount"] for a in articles)
    OUT.write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "articleCount": len(articles),
                "wordCount": words,
                "regions": REGIONS,
                "articles": articles,
            },
            ensure_ascii=False,
            indent=1,
        ) + "\n",
        encoding="utf-8",
    )
    lo = min(a["wordCount"] for a in articles)
    hi = max(a["wordCount"] for a in articles)
    print(f"wrote {OUT.name}: {len(articles)} country guides, {words:,} words ({lo}–{hi} per guide)")


if __name__ == "__main__":
    main()
