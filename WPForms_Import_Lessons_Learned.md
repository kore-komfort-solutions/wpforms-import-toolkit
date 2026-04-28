# WPForms JSON Import — Hard-Won Lessons

**Status:** Confirmed working on WPForms Pro 1.10.0.4 (April 2026). This document captures the schema gotchas that took four iterations to find. Read this BEFORE attempting another hand-crafted WPForms JSON import.

---

## The One Rule That Saves Hours

**Before writing a single line of JSON, export a working sample from the target WPForms install.**

Steps:

1. In the target WordPress site, **WPForms → Add New → Blank Form**
2. Drag in one of every field type you plan to use (text, textarea, email, phone, url, radio, checkbox, dropdown, file upload, html, page break)
3. On at least one field, turn on conditional logic and add a rule
4. Save the form
5. **WPForms → Tools → Export** → select the form → download the JSON

**That JSON is your authoritative schema reference.** Don't trust:

- Any tutorial or reference older than 6 months — WPForms's internal format changes
- The 2020 wpmetabox example floating around GitHub — outdated, missing keys
- Documentation from WPForms — they don't publish the import schema
- Your memory of how it worked on a previous project — version drift is real

The schema captured from one client install will be your starting point for the form you're building for that client. **Generate the production JSON against the same install's schema.**

---

## The Critical Gotchas (Each One Crashed v1–v3)

### 1. Multi-page forms REQUIRE a closing pagebreak

This was the smoking gun. A form with `position: "top"` pagebreak at the start and `position: "normal"` between pages **must** also have `position: "bottom"` at the end:

```json
{
  "id": "X",
  "type": "pagebreak",
  "position": "bottom",
  "prev": ""
}
```

Without it, the form imports and renders in the builder but **crashes the front-end PHP renderer with a fatal error.** Symptoms:

- Form preview returns "There has been a critical error on this website"
- Saving any page that embeds the form fails with "Updating failed. The response is not a valid JSON response."
- Hostinger/server logs show a 500 status on `/?wpforms_form_preview={id}`
- WPForms internal logs capture nothing because the crash is upstream of WPForms's logging

### 2. Choices need `icon` and `icon_style` keys

Even if you don't show icons. Every choice on radio/checkbox/dropdown fields needs:

```json
{"label": "Option 1", "value": "", "image": "", "icon": "face-smile", "icon_style": "regular"}
```

Omitting these works in the builder but can cause edge-case render failures.

### 3. Radio fields need a bunch of "icons" metadata even when not using icons

Required at the field level, not just choices:

```json
"choices_icons_color": "#066aab",
"choices_icons_size": "large",
"choices_icons_style": "default",
"choices_images_style": "modern",
"other_size": "medium",
"other_placeholder": ""
```

### 4. Checkbox needs `choice_limit`

Required key, can be empty string:

```json
"choice_limit": ""
```

### 5. Phone field uses `format: "smart"`, not `"us"`

The `"us"` value from older docs causes silent failures. Use `"smart"` (auto-detects format) unless you have a specific reason otherwise.

### 6. HTML fields use `label_disable: "1"`, not `label`

```json
{
  "id": "X",
  "type": "html",
  "name": "",
  "code": "<div>...</div>",
  "label_disable": "1",
  "css": ""
}
```

The 2020 reference had `label` and `description` fields — current schema does not.

### 7. File-upload fields need camera-capture metadata

```json
{
  "id": "X",
  "type": "file-upload",
  "label": "Upload",
  "extensions": "",
  "max_size": "",
  "max_file_number": "1",
  "style": "modern",
  "camera_format": "photo",
  "camera_aspect_ratio": "original",
  "camera_ratio_width": "4",
  "camera_ratio_height": "3",
  "camera_time_limit_minutes": "1",
  "camera_time_limit_seconds": "30"
}
```

This is for the in-browser camera-capture feature added to WPForms in late 2024/2025. **If you don't need camera capture and want to play it safe, skip file-upload fields entirely in the JSON and add them in the UI after import.** Two minutes per field.

### 8. Top pagebreak needs `progress_text` and `nav_align`

```json
{
  "id": "X",
  "type": "pagebreak",
  "position": "top",
  "indicator": "progress",
  "indicator_color": "#7CB342",
  "progress_text": "Step {current_page} of {last_page}",
  "title": "",
  "nav_align": "left",
  "css": ""
}
```

### 9. Conditional logic operators are single letters, not words

| Operator | Meaning |
|---|---|
| `i` | is (equality) — for radio, dropdown |
| `c` | contains — for checkbox |
| `e` | empty / exists |
| `!i` | is not |
| `!c` | does not contain |
| `!e` | not empty |

Using `==` (which the WPForms front-end JS sometimes accepts) will fail validation on save in many cases.

### 10. Form-level settings that MUST be present

If any of these are missing, the form may import but rendering or saving may fail:

```json
"settings": {
  "themes": { /* full theme block — see below */ },
  "form_title": "...",
  "form_desc": "",
  "submit_text": "Submit",
  "submit_text_processing": "Sending...",
  "form_class": "",
  "submit_class": "",
  "ajax_submit": "1",
  "purge_entries_days": "365",
  "notification_enable": "1",
  "notifications": { /* see below */ },
  "confirmations": { /* see below */ },
  "antispam_v3": "1",
  "store_spam_entries": "1",
  "anti_spam": {
    "time_limit": {"enable": "1", "duration": "2"},
    "filtering_store_spam": "1",
    "country_filter": {"action": "allow", "country_codes": [], "message": "..."},
    "keyword_filter": {"message": "..."}
  },
  "form_tags": []
}
```

Plus at the form root level:

```json
"providers": {"constant-contact-v3": []},
"meta": {"template": "blank"},
"search_terms": "",
"id": "1",
"field_id": <next-available-int>,
"fields": { ... }
```

### 11. Notification objects need extra keys

```json
{
  "enable": "1",
  "notification_name": "Default Notification",
  "email": "{admin_email}",
  "subject": "...",
  "sender_name": "...",
  "sender_address": "{admin_email}",
  "replyto": "",
  "message": "{all_fields}",
  "template": "",
  "file_upload_attachment_fields": [],
  "entry_csv_attachment_entry_information": [],
  "entry_csv_attachment_file_name": "entry-details"
}
```

The `enable`, `template`, `file_upload_attachment_fields`, `entry_csv_*` keys were not in older schemas.

### 12. Confirmation objects need extra keys

```json
{
  "name": "Default Confirmation",
  "type": "message",
  "message": "<p>...</p>",
  "message_scroll": "1",
  "page": "previous_page",
  "page_url_parameters": "",
  "redirect": "",
  "message_entry_preview_style": "basic"
}
```

`name`, `page_url_parameters`, `message_entry_preview_style` are required in current schema.

### 13. The `themes` block is large and required

Skip it and the form may import but lose styling control:

```json
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
  "buttonBackgroundColor": "#7CB342",
  "buttonBorderColor": "#7CB342",
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
  "pageBreakColor": "#7CB342",
  "customCss": "",
  "copyPasteJsonValue": "<JSON-stringified copy of the same theme settings>"
}
```

The `copyPasteJsonValue` is a JSON-stringified version of itself — yes, really. WPForms stores the theme twice for some reason.

---

## Diagnostic Workflow When an Import Fails

If an import imports-but-doesn't-save or imports-but-crashes-on-preview:

### Step 1: Check the Hostinger/SiteGround/server error log

Hostinger: hPanel → Files → File Manager → public_html → look for `error_log` (sometimes hidden, no extension)

SiteGround: Site Tools → Statistics → Error Log

The fatal error message will tell you the exact missing class, missing key, or malformed structure.

### Step 2: If no error log file exists

Enable WP_DEBUG by adding to `wp-config.php`:

```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

Then trigger the error and check `/wp-content/debug.log`.

### Step 3: Browser DevTools Network tab

Open the form preview URL with Chrome DevTools open (F12) → Network tab → look for the row with status 500 → click → Response tab. Sometimes the PHP fatal text appears there before WordPress's generic error page kicks in.

### Step 4: Check the WPForms admin email

WordPress automatically emails the site admin when a critical error occurs (rate-limited to one per error type per 6 hours). Subject is typically *"[Site Name] Your Site is Experiencing a Technical Issue."*

### Step 5: If no other diagnostic surfaces — pivot to manual UI build

If 30 minutes of debugging hasn't surfaced the cause, **stop iterating on JSONs.** Build the form manually in the WPForms drag-and-drop builder using your build spec. 30–45 minutes guaranteed working beats unlimited debugging time.

---

## The Build Process That Actually Works

For any future client form:

1. **Write the build spec first** — questions, options, conditional rules — in plain markdown
2. **Get a fresh schema export from the target install** (5 minutes)
3. **Generate the JSON programmatically** (Python script that mirrors the schema captured in step 2)
4. **Test import on a staging site first if possible**
5. **On production: import → click into form → click Save without changes → click Preview**
6. **If save and preview both succeed,** add file uploads in UI, configure Save & Resume, set required-field flags
7. **Embed and test end-to-end** with your own email before sending the link to the client

The Python script approach matters because once you have a working generator for one client, the next client's intake form is mostly a content swap — the schema scaffolding is reusable.

---

## Files in This Project

- `build_wpforms_json_v4.py` — the Python generator that produced the working JSON
- `NextStep_Intake_WPForms_Import_v4.json` — the working import file
- `NextStepBath_WPForms_Build_Spec.md` — the human-readable build spec (used as reference for manual builds and for understanding what the JSON should produce)
- `NextStepBath_Intake_Questionnaire.pdf` — the printable PDF version (predecessor to the web form)
- `wpforms-form-export-04-28-2026.json` — Mike's reference export from his install. **Save this. Future contractor intake forms should be generated against this schema until WPForms ships a major version update.**

---

## When to Refresh This Document

- Any time WPForms is updated to a new major version (1.11, 2.0, etc.)
- Any time the import workflow fails on a new client install
- Any time WPForms publishes new field types you want to use (e.g., signature, calculation, repeater)

When refreshing: re-do the schema export step and diff against the saved 2026 reference. Document every key that changed.
