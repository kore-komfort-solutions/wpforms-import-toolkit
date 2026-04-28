"""
NextStep Bath Intake — WPForms JSON v4 — built against actual WPForms 1.10 schema
captured from Mike's install (export dated 2026-04-28).

Key fixes vs v1-v3:
  - Added required closing pagebreak (position: bottom) — likely v3 crash cause
  - Top pagebreak now has progress_text and nav_align keys
  - Radio/checkbox/select choices now include icon/icon_style
  - Radio fields include other_size, other_placeholder, choices_icons_* keys
  - Checkbox includes choice_limit
  - File-upload removed entirely — requires complex camera keys; we add in UI
  - HTML field uses label_disable instead of label
  - Phone uses format: "smart" (not "us")
  - Conditional logic uses operator "e" (empty/exists) for show-when-not-empty,
    "i" (is) for equality match, "c" (contains) for checkbox-contains
  - Full themes block included
  - All form-level settings present: anti_spam, antispam_v3, store_spam_entries,
    purge_entries_days, form_tags, providers
  - Notifications include enable, template, file_upload_*, entry_csv_*
  - Confirmations include name, page_url_parameters, message_entry_preview_style
  - Each field includes search_terms at form level

Trade-offs:
  - File upload fields (headshot, logo) — added manually in UI after import (5 min)
  - Save & Resume — configured manually in UI
"""

import json
from collections import OrderedDict

GREEN = "#7CB342"
ADMIN_EMAIL = "mike@korekomfortsolutions.com"
OUT = "/home/claude/NextStep_Intake_WPForms_Import_v4.json"

fields = OrderedDict()
_next_id = 1

def _id():
    global _next_id
    fid = _next_id
    _next_id += 1
    return str(fid)

# --- Field builders matching WPForms 1.10 schema exactly ---

def add_text(label, description="", placeholder="", default="", input_mask=""):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "text",
        "label": label, "description": description,
        "size": "medium", "placeholder": placeholder,
        "limit_count": "1", "limit_mode": "characters",
        "default_value": default, "input_mask": input_mask, "css": "",
    }
    return fid

def add_textarea(label, description="", placeholder="", size="medium"):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "textarea",
        "label": label, "description": description,
        "size": size, "placeholder": placeholder,
        "limit_count": "1", "limit_mode": "characters",
        "default_value": "", "css": "",
    }
    return fid

def add_email(label, description=""):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "email",
        "label": label, "description": description,
        "size": "medium", "placeholder": "",
        "default_value": "", "css": "",
    }
    return fid

def add_phone(label, description=""):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "phone",
        "label": label, "format": "smart",
        "description": description,
        "size": "medium", "placeholder": "",
        "default_value": "", "css": "",
    }
    return fid

def add_url(label, description=""):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "url",
        "label": label, "description": description,
        "size": "medium", "placeholder": "",
        "default_value": "", "css": "",
    }
    return fid

def _choices(options):
    """Match the actual schema: each choice has icon and icon_style."""
    return {str(i): {
        "label": opt, "value": "", "image": "",
        "icon": "face-smile", "icon_style": "regular",
    } for i, opt in enumerate(options, start=1)}

def add_radio(label, options, description=""):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "radio",
        "label": label,
        "choices": _choices(options),
        "other_size": "medium",
        "other_placeholder": "",
        "choices_images_style": "modern",
        "choices_icons_color": GREEN,
        "choices_icons_size": "large",
        "choices_icons_style": "default",
        "description": description,
        "input_columns": "",
        "dynamic_choices": "",
        "css": "",
    }
    return fid

def add_checkbox(label, options, description=""):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "checkbox",
        "label": label,
        "choices": _choices(options),
        "choices_images_style": "modern",
        "choices_icons_color": GREEN,
        "choices_icons_size": "large",
        "choices_icons_style": "default",
        "description": description,
        "input_columns": "",
        "choice_limit": "",
        "dynamic_choices": "",
        "css": "",
    }
    return fid

def add_pagebreak_top():
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "pagebreak",
        "position": "top",
        "indicator": "progress",
        "indicator_color": GREEN,
        "progress_text": "Step {current_page} of {last_page}",
        "title": "",
        "nav_align": "left",
        "css": "",
    }
    return fid

def add_pagebreak(title, next_label="Next", prev_label="Back"):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "pagebreak",
        "position": "",
        "title": title,
        "next": next_label,
        "prev": prev_label,
        "css": "",
    }
    return fid

def add_pagebreak_bottom():
    """REQUIRED — multi-page forms need a closing bottom pagebreak."""
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "pagebreak",
        "position": "bottom",
        "prev": "",
    }
    return fid

def add_html(code):
    fid = _id()
    fields[fid] = {
        "id": fid, "type": "html",
        "name": "", "code": code,
        "label_disable": "1",
        "css": "",
    }
    return fid

def make_conditional(field_id, watch_field_id, value, show=True):
    """Conditional: show this field when watch_field_id is value.
       Operator 'i' = is, 'c' = contains (for checkbox)."""
    fields[field_id]["conditional_logic"] = "1"
    fields[field_id]["conditional_type"] = "show" if show else "hide"
    fields[field_id]["conditionals"] = [[
        {"field": watch_field_id, "operator": "i", "value": value}
    ]]

def make_conditional_contains(field_id, watch_field_id, value):
    """For checkbox-contains conditions."""
    fields[field_id]["conditional_logic"] = "1"
    fields[field_id]["conditional_type"] = "show"
    fields[field_id]["conditionals"] = [[
        {"field": watch_field_id, "operator": "c", "value": value}
    ]]

def make_conditional_or(field_id, conditions):
    """conditions: list of (watch_field, operator, value) tuples — OR'd together."""
    fields[field_id]["conditional_logic"] = "1"
    fields[field_id]["conditional_type"] = "show"
    fields[field_id]["conditionals"] = [
        [{"field": w, "operator": op, "value": v}] for w, op, v in conditions
    ]


# ===========================================================================
# Build form
# ===========================================================================

add_pagebreak_top()

add_html(
    '<div style="padding:20px;background:#F3F4F6;border-left:4px solid #7CB342;'
    'border-radius:4px;">'
    '<h2 style="margin-top:0;color:#1F2937;">Website Rebuild Intake</h2>'
    '<p>Paul - this is the intake we need to build the new NextStepBath.com '
    'to the Growth Package standard and start earning rankings in Columbus, '
    'Grove City, Pataskala, Galloway, and Plain City.</p>'
    '<p>The more specific and honest your answers, the better the site will perform. '
    "Generic answers produce generic pages, and Google ignores those.</p>"
    "<p><strong>Time required:</strong> About 30-45 minutes if you have your "
    "license, insurance, and review numbers handy. If a question doesn't apply, "
    "write &quot;N/A&quot; or pick the closest option - don't skip it.</p>"
    "</div>"
)

# -------- PAGE 2: About You --------
add_pagebreak("About You")
q1 = add_text("Full legal name (and any nickname you go by professionally)")
add_text("Year you started in the trades", "Any trade, not just this business.")
add_text("Year you founded NextStep Bath Solutions")
add_textarea(
    "Your story - in your own words, why did you start NextStep Bath Solutions?",
    description=("Was there a personal moment? A family member? A gap in the market "
                 "you saw? This is the single most important answer in the whole form. "
                 "AI engines and real homeowners both reward authenticity here."),
    size="large",
)
add_textarea(
    "What's different about how you do this work compared to the big national "
    "franchises (Bath Fitter, Re-Bath, etc.)?"
)
add_url("LinkedIn profile URL",
        "The one Mike found you on. We'll pull what we can from it.")
q7 = add_radio(
    "Do you have a longer bio written anywhere we can use as a starting point?",
    [
        "Yes - on my LinkedIn About section (and it's more than the headline)",
        "Yes - somewhere else (please tell us where below)",
        "No - but I can write 200-400 words about my background if you give me a prompt",
        "No - and I'd rather you interview me by phone and write it for me",
    ],
)
q7a = add_text("If somewhere else - paste the URL or describe where to find it")
make_conditional(q7a, q7,
                 "Yes - somewhere else (please tell us where below)")
add_text("Personal website, blog, podcast appearance, or news article you've "
         "been featured in?")
add_radio(
    "Headshot photo - do you have a professional or semi-professional one we can use?",
    [
        "Yes - I'll send a high-resolution file",
        "No - but I can take one this week (phone photo against a plain wall is fine)",
        "I'd rather you send a photographer or just use stock",
    ],
)

# -------- PAGE 3: Credentials --------
add_pagebreak("Credentials and Trust")
q11 = add_radio(
    "Are you a Certified Aging-in-Place Specialist (CAPS)?",
    ["Yes", "No"],
    "The CAPS designation is from the National Association of Home Builders.",
)
q11a = add_text("Year certified and certificate number (if you have it)")
make_conditional(q11a, q11, "Yes")
add_textarea(
    "List any other certifications, manufacturer authorizations, or "
    "professional memberships you hold",
    description=("Examples: NAHB, NARI, NKBA, BBB Accredited Business, "
                 "CleanCut Authorized Installer, Bestbath Dealer, Safe Step Authorized, "
                 "Independent Living Specialist. Include year of each."),
)
add_text(
    "Ohio contractor license number (and license type)",
    description=("If Ohio doesn't require a state-level license for your specific "
                 "work, list any city/county registrations."),
)
add_text("General liability insurance carrier and policy limit")
add_text("Workers' comp policy or exempt status")
add_text("Bonded? If yes, amount and surety company")
add_radio(
    "BBB (Better Business Bureau) status",
    ["Accredited - A+ rating", "Accredited - other rating",
     "Listed but not accredited", "Not listed yet"],
)
q18 = add_checkbox(
    "Discount programs you offer (or want to offer) - check all that apply",
    [
        "Military veteran discount",
        "Active-duty military discount",
        "First responder discount (police, fire, EMS, dispatch)",
        "Senior discount (65+)",
        "AARP member discount",
        "Disability / SSI / SSDI discount",
        "Multi-service / bundled-job discount",
        "Referral discount (existing customer refers a new one)",
        "None currently - but I'd consider adding one",
        "None - and I don't want to offer discounts",
    ],
    description=(
        "Each one we list on the site is a trust signal AND a search-volume capture: "
        "people search for things like 'walk-in tub veterans discount Columbus' "
        "as distinct queries."
    ),
)
q18a = add_textarea(
    "For each one you checked, what's the discount amount or percentage?",
)
# Show q18a if any actual discount option is checked (not the two None options)
make_conditional_or(q18a, [
    (q18, "c", "Military veteran discount"),
    (q18, "c", "Active-duty military discount"),
    (q18, "c", "First responder discount (police, fire, EMS, dispatch)"),
    (q18, "c", "Senior discount (65+)"),
    (q18, "c", "AARP member discount"),
    (q18, "c", "Disability / SSI / SSDI discount"),
    (q18, "c", "Multi-service / bundled-job discount"),
    (q18, "c", "Referral discount (existing customer refers a new one)"),
])
q19 = add_radio(
    "Are you yourself a veteran?",
    ["Yes", "No"],
    description=("If yes we can add a veteran-owned business badge - a real "
                 "ranking factor for veterans searching for accessibility contractors."),
)
q19a = add_text("Branch and years of service (only as much as you want to share publicly)")
make_conditional(q19a, q19, "Yes")

# -------- PAGE 4: Operations --------
add_pagebreak("Operations and Online Presence")
q20 = add_radio(
    "Business address situation",
    [
        "I have a public commercial address customers can visit",
        "I have a home office I'd rather not list publicly",
        "Service-area-only - I'd like the GBP set up without a street address",
    ],
)
q20a = add_textarea("Full street address, suite, city, state, ZIP")
make_conditional(q20a, q20,
                 "I have a public commercial address customers can visit")
add_phone("Primary business phone (will be displayed on every page)")
add_email("Primary business email",
          "This is the email used for confirmation copies - make sure it's correct.")
add_text("Business hours",
         "Default is Mon-Fri 8AM-5PM - change if different.")
add_textarea(
    "Google Business Profile - Mike already has access and is updating it. "
    "Anything specific you want to make sure ends up there, or anything currently "
    "there you want changed/removed?"
)
add_text("Roughly how many Google reviews do you have right now?",
         "A rough number is fine.")
add_textarea(
    "Are you on any of these other review platforms? Mark which and how many "
    "reviews on each.",
    description=("Angi, BBB, Houzz, HomeAdvisor, Yelp, Facebook, GuildQuality, "
                 "Nextdoor, AARP, Eldercare Locator, etc."),
)
q27 = add_radio(
    "Do you use any field service / booking software?",
    ["Jobber", "Housecall Pro", "ServiceTitan",
     "Square Appointments / Calendly / similar",
     "Nothing - phone, email, and a notebook", "Other"],
    description="The Growth Package includes booking-widget integration if you use one.",
)
q27a = add_text("Other booking software")
make_conditional(q27a, q27, "Other")
add_html(
    '<div style="padding:14px;background:#F0FDF4;border-left:3px solid #7CB342;'
    'margin:10px 0;">'
    '<strong>Facebook Page Management</strong> - Mike is including Facebook '
    'page setup and ongoing posting at no additional charge as part of your package. '
    'The next four questions get us what we need to do that.'
    '</div>'
)
add_url("Facebook Business Page URL",
        "Paste the URL or write 'don't have one' if there isn't a page yet.")
add_radio(
    "Facebook page admin access",
    [
        "I'll add Mike (mike@korekomfortsolutions.com) as a Page admin via Meta Business Suite",
        "I'll send Mike my login credentials (less preferred - we'd rather use proper admin access)",
        "I don't know how to grant access - I'll need help walking through it",
        "There's no page yet - Mike should create one from scratch",
    ],
)
add_radio(
    "How active do you want NextStep's Facebook to be?",
    [
        "Frequent - 3+ posts per week, project photos, tips, community engagement",
        "Steady - 1-2 posts per week, mostly project photos and customer wins",
        "Light - 2-4 posts per month, just enough to look alive",
        "I trust your judgment - pick a cadence that fits the goal",
    ],
)
add_textarea(
    "Anything off-limits on Facebook?",
    description=("Topics, opinions, photos, or content styles you do NOT want "
                 "associated with NextStep Bath Solutions. Politics, religion, "
                 "specific competitors, certain product brands, anything personal "
                 "- call it out now so we don't post something you'd want pulled later."),
)

# -------- PAGE 5: Services --------
add_pagebreak("What You Sell")
q32 = add_checkbox(
    "Services you currently offer (check all that apply)",
    [
        "Grab bar installation (single-point or full-room)",
        "Tub-to-shower conversions",
        "Step-in tub conversions (CleanCut or similar inserts)",
        "Full walk-in tub installations (replacement tubs, not inserts)",
        "Curbless / barrier-free shower installations",
        "Comfort-height (ADA) toilet installation",
        "Bidet seat or full bidet installation",
        "Bathroom flooring (slip-resistant)",
        "Stair lifts / chair lifts",
        "Ramps (interior or exterior)",
        "Doorway widening for wheelchair access",
        "Bathroom lighting upgrades for low-vision homeowners",
        "Full bathroom remodels (beyond accessibility)",
        "Kitchen accessibility modifications",
        "Whole-home aging-in-place assessments",
        "Other",
    ],
    description=("The current site shows three. We need to know if that's the full "
                 "menu or if we're leaving money on the table."),
)
q32a = add_text("Other services not listed above")
make_conditional_contains(q32a, q32, "Other")
add_text("Which service brings you the most revenue per job?")
add_text("Which service has the best lead-to-close ratio?")
add_text("Which service do you most want to grow over the next 12 months?")
q36 = add_radio("Do you offer free in-home consultations?", ["Yes", "No"])
q36a = add_textarea("Any conditions or restrictions on free consultations?")
make_conditional(q36a, q36, "Yes")
q37 = add_radio(
    "Financing options you offer",
    [
        "In-house financing or payment plan",
        "Third-party financing partner - name them below",
        "Credit card only",
        "Cash/check only - no financing",
    ],
)
q37a = add_text("Financing partner names",
                "Synchrony, GreenSky, Hearth, etc.")
make_conditional_or(q37a, [
    (q37, "i", "In-house financing or payment plan"),
    (q37, "i", "Third-party financing partner - name them below"),
])
add_textarea(
    "Typical price ranges you're comfortable publishing on the site",
    description=("Most homeowners want a range. Examples: 'Tub-to-shower conversion: "
                 "$X,XXX to $X,XXX', 'Grab bar installation: $XXX per bar, "
                 "$XXX for full bathroom'. If you'd rather not publish prices, "
                 "write 'NO PRICES'."),
)
add_textarea(
    "Warranty terms - labor warranty and product warranty separately"
)

# -------- PAGE 6: Cities --------
add_pagebreak("Target Cities")
CITY_OPTIONS = [
    "Yes - many jobs",
    "Yes - a few jobs",
    "No, but I'd take work there",
    "No - and not currently set up to",
]
def add_city_block(city):
    add_html(f'<h3 style="color:#7CB342;border-bottom:2px solid #7CB342;'
             f'padding-bottom:6px;margin-top:20px;">{city}</h3>')
    add_radio(f"Have you completed work in {city} in the last 24 months?",
              CITY_OPTIONS)
    add_text(f"Roughly how many jobs in {city} in the last 24 months?",
             "A number is fine.")
    add_textarea(
        f"Notable senior communities, 55+ neighborhoods, or care facilities in "
        f"{city} you've worked in or near"
    )
    add_textarea(
        f"Local landmarks or neighborhoods a {city} resident would recognize",
        "Town Center, parks, main streets, school districts, churches.",
    )
    add_textarea(f"Your main competitors actually doing this work in {city}")

for city in ["Columbus", "Grove City", "Pataskala", "Galloway", "Plain City"]:
    add_city_block(city)

# -------- PAGE 7: Assets and Goals --------
add_pagebreak("Assets and Goals")
add_radio(
    "Project photos (before/during/after)",
    [
        "I have 50+ photos with signed releases - ready to send",
        "I have 10-50 photos but no formal releases - homeowners would probably consent",
        "I have a handful of phone photos",
        "I have nothing usable - we'll need to plan a photo session",
    ],
)
add_radio(
    "Customer testimonials / reviews you can quote on the site",
    [
        "Yes - I have 10+ written testimonials with the customer's first name and city",
        "Yes - I have several Google reviews we can use",
        "A few here and there",
        "None I can put my hands on right now",
    ],
)
add_radio(
    "Logo files you have access to",
    [
        "Vector files (.ai, .eps, .svg, or layered .pdf) - the originals",
        "High-res PNG only",
        "Just whatever's on the current website",
        "I'm not sure - I'll check with whoever made it",
    ],
)
add_textarea(
    "Social media accounts other than Facebook (which we covered above)",
    description=("Instagram handle, TikTok, YouTube, Nextdoor, LinkedIn company page. "
                 "Note which you actually update vs. which exist but are dormant."),
)
add_text("Roughly how many qualified leads are you getting per month right now?")
add_text("What's your average completed job value?")
add_text("Realistic 90-day goal - leads per month you'd like to be getting")
add_text("Realistic 12-month goal - annual revenue target")
add_textarea(
    "If you could outrank ONE competitor in Google search results in Columbus, "
    "who is it and why?",
    "This tells us who to study and where to find rankable gaps.",
)
add_textarea(
    "Anything else you want me to know?",
    description=("Pet peeves about your old marketing, things you absolutely don't "
                 "want on the new site, words/phrases you do or don't want associated "
                 "with NextStep, ideal customer descriptions, etc."),
)

# REQUIRED — closing pagebreak (this was missing in v1-v3)
add_pagebreak_bottom()

# ===========================================================================
# Settings — full WPForms 1.10 schema
# ===========================================================================

theme_json = {
    "themeName": "", "isCustomTheme": "", "wpformsTheme": "default",
    "customCss": "", "containerPadding": "0", "containerBorderStyle": "none",
    "containerBorderWidth": "1", "containerBorderRadius": "3",
    "containerShadowSize": "none", "containerBorderColor": "#000000",
    "fieldSize": "medium", "fieldBorderStyle": "solid", "fieldBorderRadius": "3",
    "fieldBorderSize": "1", "fieldBackgroundColor": "#ffffff",
    "fieldBorderColor": "rgba(0, 0, 0, 0.25)",
    "fieldTextColor": "rgba(0, 0, 0, 0.7)", "fieldMenuColor": "#ffffff",
    "pageBreakColor": GREEN, "labelSize": "medium",
    "labelColor": "rgba(0, 0, 0, 0.85)",
    "labelSublabelColor": "rgba(0, 0, 0, 0.55)", "labelErrorColor": "#d63637",
    "buttonSize": "medium", "buttonBorderStyle": "none", "buttonBorderSize": "1",
    "buttonBorderRadius": "3", "buttonBackgroundColor": GREEN,
    "buttonBorderColor": GREEN, "buttonTextColor": "#ffffff",
    "backgroundColor": "rgba(0, 0, 0, 0)", "backgroundPosition": "center center",
    "backgroundUrl": "url()", "backgroundRepeat": "no-repeat",
    "backgroundSize": "cover", "backgroundSizeMode": "cover",
    "backgroundWidth": "100", "backgroundHeight": "100",
    "backgroundImage": "none",
}

form = {
    "fields": fields,
    "id": "1",
    "field_id": _next_id,
    "search_terms": "",
    "settings": {
        "themes": {
            "wpformsTheme": "default",
            "isCustomTheme": "",
            "themeName": "",
            "fieldSize": "medium",
            "fieldBorderStyle": "solid",
            "fieldBorderSize": "1",
            "fieldBorderRadius": "3",
            "fieldBackgroundColor": "#ffffff",
            "fieldBorderColor": "rgba(0, 0, 0, 0.25)",
            "fieldTextColor": "rgba(0, 0, 0, 0.7)",
            "labelSize": "medium",
            "labelColor": "rgba(0, 0, 0, 0.85)",
            "labelSublabelColor": "rgba(0, 0, 0, 0.55)",
            "labelErrorColor": "#d63637",
            "buttonSize": "medium",
            "buttonBorderStyle": "none",
            "buttonBorderSize": "1",
            "buttonBorderRadius": "3",
            "buttonBackgroundColor": GREEN,
            "buttonBorderColor": GREEN,
            "buttonTextColor": "#ffffff",
            "containerPadding": "0",
            "containerBorderStyle": "none",
            "containerBorderWidth": "1",
            "containerBorderRadius": "3",
            "containerBorderColor": "#000000",
            "containerShadowSize": "none",
            "backgroundColor": "rgba(0, 0, 0, 0)",
            "backgroundImage": "none",
            "backgroundSize": "cover",
            "backgroundUrl": "url()",
            "fieldMenuColor": "#ffffff",
            "pageBreakColor": GREEN,
            "customCss": "",
            "copyPasteJsonValue": json.dumps(theme_json),
        },
        "form_title": "NextStep Bath Solutions - Website Rebuild Intake",
        "form_desc": "",
        "submit_text": "Submit My Intake",
        "submit_text_processing": "Sending...",
        "form_class": "",
        "submit_class": "",
        "ajax_submit": "1",
        "purge_entries_days": "365",
        "notification_enable": "1",
        "notifications": {
            "1": {
                "enable": "1",
                "notification_name": "Default Notification",
                "email": ADMIN_EMAIL,
                "subject": "NextStep Bath Intake - New Submission",
                "sender_name": "NextStep Intake Form",
                "sender_address": "{admin_email}",
                "replyto": "",
                "message": "{all_fields}",
                "template": "",
                "file_upload_attachment_fields": [],
                "entry_csv_attachment_entry_information": [],
                "entry_csv_attachment_file_name": "entry-details",
            },
        },
        "confirmations": {
            "1": {
                "name": "Default Confirmation",
                "type": "message",
                "message": (
                    "<p><strong>Thanks Paul - your intake came through.</strong></p>"
                    "<p>I have everything I need to start the rebuild. A copy of your "
                    "answers has been emailed to you for your records.</p>"
                    "<p>Watch for an email from me within 5 business days with the "
                    "rebuilt About page, schema and trust-signal upgrades to your "
                    "service pages, and a draft of the Columbus city page for your "
                    "approval.</p>"
                    "<p>- Mike</p>"
                ),
                "message_scroll": "1",
                "page": "previous_page",
                "page_url_parameters": "",
                "redirect": "",
                "message_entry_preview_style": "basic",
            },
        },
        "antispam_v3": "1",
        "store_spam_entries": "1",
        "anti_spam": {
            "time_limit": {"enable": "1", "duration": "2"},
            "filtering_store_spam": "1",
            "country_filter": {
                "action": "allow",
                "country_codes": [],
                "message": "Sorry, this form does not accept submissions from your country.",
            },
            "keyword_filter": {
                "message": "Sorry, your message can't be submitted because it contains prohibited words.",
            },
        },
        "form_tags": [],
    },
    "providers": {"constant-contact-v3": []},
    "meta": {"template": "blank"},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump([form], f, indent=2, ensure_ascii=True)

print(f"Wrote: {OUT}")
print(f"Total fields: {len(fields)}")
print(f"Field types: {sorted(set(v['type'] for v in fields.values()))}")

# Verify we have a top and bottom pagebreak (was the missing piece)
positions = [f.get('position') for f in fields.values() if f['type'] == 'pagebreak']
print(f"Pagebreak positions: {positions}")
print(f"Has top: {'top' in positions}, Has bottom: {'bottom' in positions}")
