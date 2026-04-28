# NextStep Bath Intake — WPForms Build Spec

A field-by-field guide for building the intake form in WPForms Plus on KoreKomfortSolutions.com. Estimated build time: **30–45 minutes** if you keep this open side-by-side.

---

## Pre-Build Setup

### Create the host page first

1. **Pages → Add New** → Title: `NextStep Bath Intake`
2. **Permalink:** `/nextstep-intake/`
3. **Visibility:** Public, but...
4. **SEO (Rank Math or Yoast or whatever you have):** set to **`noindex, nofollow`** so it doesn't surface in search
5. **Don't add to any menu.** You'll send Paul the direct URL.
6. Leave the page body empty for now — we'll embed the form here once it's built.

### Create the form shell

1. **WPForms → Add New**
2. **Template:** Blank Form
3. **Form Name:** `NextStep Bath Intake — Paul Knox`
4. **Description:** `Website rebuild intake — Growth Package`

---

## Form-Level Settings

Before adding fields, configure these under **Settings** in the form builder.

### General

| Setting | Value |
|---|---|
| Form Title | NextStep Bath Solutions — Website Rebuild Intake |
| Form Description | (leave blank — we'll put the intro in an HTML field) |
| Submit Button Text | `Submit My Intake` |
| Submit Button Processing Text | `Sending — one moment…` |
| Enable AJAX form submission | ✅ ON |
| Disable storing entry information | ❌ OFF (we want entries saved in DB) |

### Anti-Spam and Security

| Setting | Value |
|---|---|
| Enable anti-spam protection (honeypot) | ✅ ON |
| Enable Akismet anti-spam protection | ✅ ON if Akismet is active on the site |
| reCAPTCHA / hCAPTCHA | ❌ OFF — adds friction, not needed for a private intake URL |

### Notifications (Email to Mike)

Click **Notifications → Default Notification**:

| Setting | Value |
|---|---|
| Send To Email Address | `mike@korekomfortsolutions.com` |
| Email Subject | `NextStep Bath Intake — {field_id="2"} — {date format="m/d/Y"}` |
| From Name | `NextStep Intake Form` |
| From Email | `{admin_email}` |
| Reply-To | `{field_id="X"}` *(set to whatever ID becomes Paul's email — Q21)* |
| Message | `{all_fields}` |

### Add a SECOND notification (Confirmation Copy to Paul)

Click **Add New Notification** → name it `Copy to Paul`:

| Setting | Value |
|---|---|
| Send To Email Address | `{field_id="X"}` *(Paul's email — Q21)* |
| Email Subject | `Your NextStep Bath Intake — Copy for Your Records` |
| From Name | `Mike Warner — Kore Komfort Solutions` |
| From Email | `mike@korekomfortsolutions.com` |
| Message | See template below |

**Confirmation email body for Paul:**

```
Paul,

Thanks for filling this out. I have everything I need to start the rebuild.

A copy of your answers is below for your records. I'll be in touch within
5 business days with the rebuilt About page, the schema/trust upgrades to
your service pages, and a draft of the first city page (Columbus) for
your approval. The other four cities will follow on a weekly cadence
after that.

If anything changes between now and then — new certification, new
review platform, new project worth photographing — just reply to this
email and let me know.

Mike Warner
Kore Komfort Solutions
mike@korekomfortsolutions.com

---

YOUR ANSWERS:

{all_fields}
```

### Confirmations

Click **Confirmations → Default Confirmation**:

| Setting | Value |
|---|---|
| Confirmation Type | Message |
| Confirmation Message | See below |

**Confirmation message:**

```
Thanks Paul — your intake came through.

I have everything I need to start the rebuild. A copy of your answers
has been emailed to you for your records.

Watch for an email from me within 5 business days with:
  • The rebuilt About page
  • Schema and trust-signal upgrades to your service pages
  • A draft of the Columbus city page for your approval

— Mike
```

---

## Field Build — Page by Page

The form is built as a **multi-page form**. After each section, insert a **Page Break** field (Fancy Fields → Page Break). The progress bar at the top will show Paul where he is.

### Page Break configuration (use this for ALL page breaks)

| Setting | Value |
|---|---|
| Progress Indicator | Progress Bar |
| Progress Bar Color | `#7CB342` (NextStep green) |
| First Page Title | `Welcome` |
| Next Button Label | `Next →` |
| Previous Button Label | `← Back` |

---

## PAGE 1 — Welcome / Intro

**Field 1: HTML field** (Fancy Fields → HTML)
- **Label:** (leave blank)
- **Code:**

```html
<div style="padding:20px;background:#F3F4F6;border-left:4px solid #7CB342;border-radius:4px;">
<h2 style="margin-top:0;color:#1F2937;">Website Rebuild Intake</h2>
<p>Paul — this is the intake we need to build the new NextStepBath.com to the Growth Package standard and start earning rankings in Columbus, Grove City, Pataskala, Galloway, and Plain City.</p>
<p>The more specific and honest your answers, the better the site will perform. Generic answers produce generic pages, and Google ignores those.</p>
<p><strong>Time required:</strong> About 30–45 minutes if you have your license, insurance, and review numbers handy. If a question doesn't apply, write "N/A" or pick the closest option — don't skip it.</p>
<p style="color:#6B7280;font-size:14px;"><em>Note: WPForms Plus doesn't have save-and-resume, so try to do this in one sitting. If you have to leave, your browser may keep your answers if you don't close the tab.</em></p>
</div>
```

**→ Insert Page Break** (Title: `About You`)

---

## PAGE 2 — Section 1: About You

| # | Field Type | Label | Description | Required | Notes |
|---|---|---|---|---|---|
| 1 | Single Line Text | Full legal name (and any nickname you go by professionally) | | ✅ | |
| 2 | Single Line Text | Year you started in the trades | Any trade, not just this business. | ✅ | |
| 3 | Single Line Text | Year you founded NextStep Bath Solutions | | ✅ | |
| 4 | Paragraph Text | Your story — in your own words, why did you start NextStep Bath Solutions? | Was there a personal moment? A family member? A gap in the market you saw? This is the single most important answer in the whole form. AI engines and real homeowners both reward authenticity here. | ✅ | Field size: Large |
| 5 | Paragraph Text | What's different about how you do this work compared to the big national franchises (Bath Fitter, Re-Bath, etc.)? | | ✅ | |
| 6 | URL | LinkedIn profile URL | The one Mike found you on. We'll pull what we can from it. | | |
| 7 | Multiple Choice | Do you have a longer bio written anywhere we can use as a starting point? | | ✅ | Options below |
| 7a | Single Line Text | If "somewhere else" — paste the URL or describe where to find it | | | **Conditional:** Show this field only if Q7 = "Yes — somewhere else" |
| 8 | Single Line Text | Personal website, blog, podcast appearance, or news article you've been featured in? | | | |
| 9 | Multiple Choice | Headshot photo — do you have a professional or semi-professional one we can use? | | ✅ | Options below |
| 10 | File Upload | Upload your headshot if you have one ready | JPG, PNG, or HEIC. Up to 10 MB. | | **Conditional:** Show only if Q9 = "Yes — I'll send a high-resolution file". Allowed extensions: jpg,jpeg,png,heic |

**Q7 options:**
- Yes — on my LinkedIn 'About' section (and it's more than the headline)
- Yes — somewhere else (please tell us where below)
- No — but I can write 200–400 words about my background if you give me a prompt
- No — and I'd rather you interview me by phone and write it for me

**Q9 options:**
- Yes — I'll send a high-resolution file
- No — but I can take one this week (phone photo against a plain wall is fine)
- I'd rather you send a photographer or just use stock

**→ Insert Page Break** (Title: `Credentials`)

---

## PAGE 3 — Section 2: Credentials & Trust Signals

| # | Field Type | Label | Description | Required | Notes |
|---|---|---|---|---|---|
| 11 | Multiple Choice | Are you a Certified Aging-in-Place Specialist (CAPS)? | The CAPS designation is from the National Association of Home Builders. | ✅ | Options: Yes / No |
| 11a | Single Line Text | Year certified and certificate number (if you have it) | | | **Conditional:** Show only if Q11 = "Yes" |
| 12 | Paragraph Text | List any other certifications, manufacturer authorizations, or professional memberships you hold | Examples: NAHB, NARI, NKBA, BBB Accredited Business, CleanCut Authorized Installer, Bestbath Dealer, Safe Step Authorized, Independent Living Specialist. Include year of each. | | |
| 13 | Single Line Text | Ohio contractor license number (and license type) | If Ohio doesn't require a state-level license for your specific work, list any city/county registrations. | | |
| 14 | Single Line Text | General liability insurance carrier and policy limit | | ✅ | |
| 15 | Single Line Text | Workers' comp policy or exempt status | | | |
| 16 | Single Line Text | Bonded? If yes, amount and surety company | | | |
| 17 | Multiple Choice | BBB (Better Business Bureau) status | | | Options below |
| 18 | Checkboxes | Discount programs you offer (or want to offer) — check all that apply | Each one we list on the site is a trust signal AND a search-volume capture: people search 'walk-in tub veterans discount Columbus' and 'senior discount tub-to-shower' as distinct queries. | | Options below |
| 18a | Paragraph Text | For each one you checked, what's the discount amount or percentage? | | | **Conditional:** Show only if Q18 has any answer EXCEPT "None — and I don't want to offer discounts" |
| 19 | Multiple Choice | Are you yourself a veteran? | If yes we can add a veteran-owned business badge — a real ranking factor for veterans searching for accessibility contractors. | ✅ | Options: Yes / No |
| 19a | Single Line Text | Branch and years of service (only as much as you want to share publicly) | | | **Conditional:** Show only if Q19 = "Yes" |

**Q17 options:**
- Accredited — A+ rating
- Accredited — other rating
- Listed but not accredited
- Not listed yet

**Q18 options:**
- Military veteran discount
- Active-duty military discount
- First responder discount (police, fire, EMS, dispatch)
- Senior discount (65+)
- AARP member discount
- Disability / SSI / SSDI discount
- Multi-service / bundled-job discount
- Referral discount (existing customer refers a new one)
- None currently — but I'd consider adding one
- None — and I don't want to offer discounts

**→ Insert Page Break** (Title: `Operations`)

---

## PAGE 4 — Section 3: Business Operations & Online Presence

| # | Field Type | Label | Description | Required | Notes |
|---|---|---|---|---|---|
| 20 | Multiple Choice | Business address situation | | ✅ | Options below |
| 20a | Address (or Paragraph Text) | Full street address, suite, city, state, ZIP | | | **Conditional:** Show only if Q20 = "I have a public commercial address" |
| 21 | Phone | Primary business phone (will be displayed on every page) | | ✅ | Default: (614) 365-1522 — Paul confirms or changes |
| 22 | Email | Primary business email | | ✅ | This is the email used for confirmation copies — make sure it's correct |
| 23 | Single Line Text | Business hours | Default is Mon–Fri 8AM–5PM — change if different. | | |
| 24 | Paragraph Text | Google Business Profile — Mike already has access and is updating it. Anything specific you want to make sure ends up there, or anything currently there you want changed/removed? | | | |
| 25 | Single Line Text | Roughly how many Google reviews do you have right now? | A rough number is fine. | | |
| 26 | Paragraph Text | Are you on any of these other review platforms? Mark which and how many reviews on each. | Angi, BBB, Houzz, HomeAdvisor, Yelp, Facebook, GuildQuality, Nextdoor, AARP, Eldercare Locator, etc. | | |
| 27 | Multiple Choice | Do you use any field service / booking software? | The Growth Package includes booking-widget integration if you use one. | | Options below |
| 27a | Single Line Text | Other booking software | | | **Conditional:** Show only if Q27 = "Other" |

**Q20 options:**
- I have a public commercial address customers can visit
- I have a home office I'd rather not list publicly
- Service-area-only — I'd like the GBP set up without a street address

**Q27 options:**
- Jobber
- Housecall Pro
- ServiceTitan
- Square Appointments / Calendly / similar
- Nothing — phone, email, and a notebook
- Other

### Facebook Page Management Block

Drop an **HTML field** here for the section break:

```html
<div style="padding:14px;background:#F0FDF4;border-left:3px solid #7CB342;margin:10px 0;">
<strong>Facebook Page Management</strong> — Mike is including Facebook page setup and ongoing posting at no additional charge as part of your package. The next four questions get us what we need to do that.
</div>
```

| # | Field Type | Label | Description | Required | Notes |
|---|---|---|---|---|---|
| 28 | URL | Facebook Business Page URL | Paste the URL or write 'don't have one' if there isn't a page yet. | | |
| 29 | Multiple Choice | Facebook page admin access | | ✅ | Options below |
| 30 | Multiple Choice | How active do you want NextStep's Facebook to be? | | ✅ | Options below |
| 31 | Paragraph Text | Anything off-limits on Facebook? | Topics, opinions, photos, or content styles you do NOT want associated with NextStep Bath Solutions. Politics, religion, specific competitors, certain product brands, anything personal — call it out now so we don't post something you'd want pulled later. | | |

**Q29 options:**
- I'll add Mike (mike@korekomfortsolutions.com) as a Page admin via Meta Business Suite
- I'll send Mike my login credentials (less preferred — we'd rather use proper admin access)
- I don't know how to grant access — I'll need help walking through it
- There's no page yet — Mike should create one from scratch

**Q30 options:**
- Frequent — 3+ posts per week, project photos, tips, community engagement
- Steady — 1–2 posts per week, mostly project photos and customer wins
- Light — 2–4 posts per month, just enough to look alive
- I trust your judgment — pick a cadence that fits the goal

**→ Insert Page Break** (Title: `Services`)

---

## PAGE 5 — Section 4: What You Actually Sell

| # | Field Type | Label | Description | Required | Notes |
|---|---|---|---|---|---|
| 32 | Checkboxes | Services you currently offer (check all that apply) | The current site shows three. We need to know if that's the full menu or if we're leaving money on the table. | ✅ | Options below |
| 32a | Single Line Text | Other services not listed above | | | **Conditional:** Show only if Q32 = "Other" |
| 33 | Single Line Text | Which service brings you the most revenue per job? | | | |
| 34 | Single Line Text | Which service has the best lead-to-close ratio? | | | |
| 35 | Single Line Text | Which service do you most want to grow over the next 12 months? | | | |
| 36 | Multiple Choice | Do you offer free in-home consultations? | | ✅ | Options: Yes / No |
| 36a | Paragraph Text | Any conditions or restrictions on free consultations? | | | **Conditional:** Show only if Q36 = "Yes" |
| 37 | Multiple Choice | Financing options you offer | | | Options below |
| 37a | Single Line Text | Financing partner names | Synchrony, GreenSky, Hearth, etc. | | **Conditional:** Show only if Q37 = "In-house" or "Third-party financing partner" |
| 38 | Paragraph Text | Typical price ranges you're comfortable publishing on the site | Most homeowners want a range. Examples: 'Tub-to-shower conversion: $X,XXX–$X,XXX', 'Grab bar installation: $XXX per bar, $XXX for full bathroom'. If you'd rather not publish prices, write 'NO PRICES'. | ✅ | |
| 39 | Paragraph Text | Warranty terms — labor warranty and product warranty separately | | | |

**Q32 options (the full service list):**
- Grab bar installation (single-point or full-room)
- Tub-to-shower conversions
- Step-in tub conversions (CleanCut® or similar inserts)
- Full walk-in tub installations (replacement tubs, not inserts)
- Curbless / barrier-free shower installations
- Comfort-height (ADA) toilet installation
- Bidet seat or full bidet installation
- Bathroom flooring (slip-resistant)
- Stair lifts / chair lifts
- Ramps (interior or exterior)
- Doorway widening for wheelchair access
- Bathroom lighting upgrades for low-vision homeowners
- Full bathroom remodels (beyond accessibility)
- Kitchen accessibility modifications
- Whole-home aging-in-place assessments
- Other

**Q37 options:**
- In-house financing or payment plan
- Third-party financing partner — name them below
- Credit card only
- Cash/check only — no financing

**→ Insert Page Break** (Title: `Target Cities`)

---

## PAGE 6 — Section 5: The Five Target Cities

This is the most important page for ranking quality. **Build it as five identical sub-blocks.** I'd recommend grouping each city under a Layout/Section Divider field if your version of WPForms has it, otherwise just use HTML field separators.

For each city below, repeat the same five questions. **Total: 25 fields on this page** (5 cities × 5 questions).

### Repeat this block for each city

Insert an HTML field as the city header:

```html
<h3 style="color:#7CB342;border-bottom:2px solid #7CB342;padding-bottom:6px;margin-top:20px;">[CITY NAME]</h3>
```

| Sub-Q | Field Type | Label | Description | Required |
|---|---|---|---|---|
| a | Multiple Choice | Have you completed work in [city] in the last 24 months? | | ✅ |
| b | Single Line Text | Roughly how many jobs in [city] in the last 24 months? | A number is fine. | |
| c | Paragraph Text | Notable senior communities, 55+ neighborhoods, or care facilities in [city] you've worked in or near | | |
| d | Paragraph Text | Local landmarks or neighborhoods a [city] resident would recognize | Town Center, parks, main streets, school districts, churches. | |
| e | Paragraph Text | Your main competitors actually doing this work in [city] | | |

**Sub-Q a options (same for every city):**
- Yes — many jobs
- Yes — a few jobs
- No, but I'd take work there
- No — and not currently set up to

### The five cities, in order:

1. **Columbus**
2. **Grove City**
3. **Pataskala**
4. **Galloway**
5. **Plain City**

After all five city blocks → **Insert Page Break** (Title: `Assets & Goals`)

---

## PAGE 7 — Section 6 + 7: Marketing Assets & Goals

(Combining the last two short sections on one page.)

| # | Field Type | Label | Description | Required | Notes |
|---|---|---|---|---|---|
| 65 | Multiple Choice | Project photos (before/during/after) | | ✅ | Options below |
| 66 | Multiple Choice | Customer testimonials / reviews you can quote on the site | | ✅ | Options below |
| 67 | Multiple Choice | Logo files you have access to | | ✅ | Options below |
| 68 | File Upload | Upload your logo file if you have it ready | AI, EPS, SVG, or PDF preferred. Up to 10 MB. | | **Conditional:** Show only if Q67 = "Vector files". Allowed extensions: ai,eps,svg,pdf,png |
| 69 | Paragraph Text | Social media accounts other than Facebook (which we covered above) | Instagram handle, TikTok, YouTube, Nextdoor, LinkedIn company page. Note which you actually update vs. which exist but are dormant. | | |
| 70 | Single Line Text | Roughly how many qualified leads are you getting per month right now? | | | |
| 71 | Single Line Text | What's your average completed job value? | | | |
| 72 | Single Line Text | Realistic 90-day goal — leads per month you'd like to be getting | | | |
| 73 | Single Line Text | Realistic 12-month goal — annual revenue target | | | |
| 74 | Paragraph Text | If you could outrank ONE competitor in Google search results in Columbus, who is it and why? | This tells us who to study and where to find rankable gaps. | | |
| 75 | Paragraph Text | Anything else you want me to know? | Pet peeves about your old marketing, things you absolutely don't want on the new site, words/phrases you do or don't want associated with NextStep, ideal customer descriptions, etc. | | |

**Q65 options:**
- I have 50+ photos with signed releases — ready to send
- I have 10–50 photos but no formal releases — homeowners would probably consent
- I have a handful of phone photos
- I have nothing usable — we'll need to plan a photo session

**Q66 options:**
- Yes — I have 10+ written testimonials with the customer's first name and city
- Yes — I have several Google reviews we can use
- A few here and there
- None I can put my hands on right now

**Q67 options:**
- Vector files (.ai, .eps, .svg, or layered .pdf) — the originals
- High-res PNG only
- Just whatever's on the current website
- I'm not sure — I'll check with whoever made it

---

## After You Save the Form

### Embed it on the page

1. Edit `Pages → NextStep Bath Intake`
2. Add a WPForms block (Gutenberg) or shortcode
3. Select the form you just built
4. Update the page

### Test it yourself FIRST

1. Open the page in an incognito window
2. Fill it out completely with test data ("TEST" in name, your own email)
3. Submit and confirm:
   - You receive the notification email at mike@korekomfortsolutions.com with all fields populated
   - The "Paul" copy goes to the email you used as Q22
   - The on-screen confirmation message displays correctly
   - The conditional logic fields show/hide correctly
4. Delete the test entry from **WPForms → Entries**

### Send Paul the link

```
https://korekomfortsolutions.com/nextstep-intake/
```

---

## Recommended Email to Paul

Subject: `NextStep Bath website rebuild — quick intake (30–45 min)`

> Paul —
>
> Before I rebuild the site, I need about 45 minutes of your input on a few things — your background, your credentials, the cities you want to dominate, and what you actually sell. I built it as a web form so you can fill it out from your phone or computer, no PDF wrestling required.
>
> **Link:** https://korekomfortsolutions.com/nextstep-intake/
>
> A few notes:
> - It's about 53 questions across 7 short sections, with a progress bar
> - Try to do it in one sitting — there's no save-and-resume
> - If a question doesn't apply, write "N/A" or pick the closest option
> - The most important question is "why did you start NextStep" — take your time on that one
>
> Once you submit, you'll get a copy of your answers by email and I'll have everything I need to start the rebuild. I'll be back to you within 5 business days with the rebuilt About page, schema upgrades to your service pages, and a draft of the Columbus city page for your approval.
>
> — Mike

---

## After Paul Submits

You'll have:
1. A WPForms entry stored in the WP database
2. An email in your inbox with all answers formatted via `{all_fields}`
3. Paul's confirmation copy in his inbox
4. (Maybe) uploaded headshot and logo files in `/wp-content/uploads/wpforms/`

Export the entry as CSV from **WPForms → Entries** for archiving. Then the real work starts — Phase 1 of the rebuild plan.
