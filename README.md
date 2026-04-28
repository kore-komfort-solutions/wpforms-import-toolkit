# wpforms-import-toolkit

> Generate working WPForms Pro JSON import files from a clean Python spec, with the WPForms 1.10 schema captured and documented so you don't have to reverse-engineer it yourself.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![WPForms Pro](https://img.shields.io/badge/WPForms-Pro%201.10-066aab)](https://wpforms.com)

If you've ever tried to hand-craft a WPForms JSON import file, you know what this repo solves. You build the JSON, the form imports cleanly into the builder, and then it crashes the front-end PHP renderer with a generic "There has been a critical error on this website" — no useful diagnostic anywhere. That happens because **WPForms's import-time validation accepts a much looser structure than its render-time validation**, and the actual schema isn't publicly documented.

This toolkit fixes that. It contains:

- A **Python generator** (`build_wpforms_json_v4.py`) that emits known-working WPForms Pro JSON for multi-page forms with conditional logic, custom themes, anti-spam, notifications, confirmations, and a 50+ field intake template
- The **complete WPForms 1.10 schema reference** captured from a fresh export, with every required key documented
- A **lessons-learned doc** covering the 13 schema gotchas that crash hand-crafted imports, with the exact diagnostic workflow when an import fails

The repo was extracted from real client work — building a contractor intake form for a bath-remodeling business in Central Ohio. Four import attempts failed before we figured out the schema requirements. This repo exists so the next person doesn't lose the same 90 minutes.

---

## Quick start

```bash
git clone https://github.com/kore-komfort-solutions/wpforms-import-toolkit.git
cd wpforms-import-toolkit
python3 build_wpforms_json_v4.py
```

Output: `NextStep_Intake_WPForms_Import_v4.json` — a ready-to-import file for a contractor-website intake form.

To customize for your own use case, edit the question content in `build_wpforms_json_v4.py` (it's heavily commented). The schema scaffolding stays the same.

Then in WordPress: **WPForms → Tools → Import** → upload the JSON.

---

## Why this exists

WPForms is one of the most popular form plugins for WordPress, and many agencies/freelancers want to deploy the same complex form across multiple client sites without rebuilding it 50 times in the drag-and-drop builder. The official advice is to use the export/import feature — but the JSON format is not publicly documented, has changed multiple times, and version mismatches between source and target installs produce silent or fatal errors.

This toolkit captures what actually works on **WPForms Pro 1.10.0.4** (April 2026). When WPForms ships major version updates, the schema may change — see the diagnostic workflow in `WPForms_Import_Lessons_Learned.md` for how to capture an updated reference from a target install.

---

## What's in the repo

| File | Purpose |
|---|---|
| `build_wpforms_json_v4.py` | Python script that generates the JSON. Edit the question content, regenerate. |
| `NextStep_Intake_WPForms_Import_v4.json` | A ready-to-import working example (50+ field contractor intake form with conditional logic). |
| `wpforms-form-export-04-28-2026.json` | The schema reference — a clean export from WPForms Pro 1.10. Use this as a template for new field types. |
| `WPForms_Import_Lessons_Learned.md` | The 13 schema gotchas, the diagnostic workflow when imports fail, and the build process that actually works. |
| `NextStepBath_WPForms_Build_Spec.md` | Field-by-field build spec for the example form — useful as a fallback if you'd rather build manually in the WPForms UI than via JSON import. |

---

## The 13 schema gotchas (short version)

Each of these crashed the form during development. Full details in `WPForms_Import_Lessons_Learned.md`:

1. **Multi-page forms require a closing `position: "bottom"` pagebreak** — without it the renderer crashes with a fatal PHP error
2. Choices must include `icon` and `icon_style` keys even when not using icons
3. Radio fields need `other_size`, `other_placeholder`, and four `choices_icons_*` keys
4. Checkbox fields need a `choice_limit` key (can be empty string)
5. Phone fields use `format: "smart"` not `"us"`
6. HTML fields use `label_disable: "1"` not `label`
7. File-upload fields need camera-capture metadata keys (`camera_format`, `camera_aspect_ratio`, etc.) added in late 2024
8. Top pagebreak needs `progress_text` and `nav_align` keys
9. Conditional logic operators are single letters: `i` (is), `c` (contains), `e` (empty)
10. Form-level `settings` must include the full `themes` block, `anti_spam` block, `antispam_v3`, `store_spam_entries`, `purge_entries_days`, `form_tags`
11. Notifications need `enable`, `template`, `file_upload_attachment_fields`, `entry_csv_*` keys
12. Confirmations need `name`, `page_url_parameters`, `message_entry_preview_style` keys
13. Form root needs `providers`, `meta`, `search_terms`, `id`, `field_id` keys

---

## The one rule that saves hours

**Before writing any WPForms JSON, export a working sample from the target install.** WPForms's schema is version-sensitive and changes between releases. A reference from one install is the only authoritative source for the format you should match.

The included `wpforms-form-export-04-28-2026.json` is current for WPForms Pro 1.10.0.4. For other versions, follow this process in the target install:

1. WPForms → Add New → Blank Form
2. Drag in one of every field type you'll use (text, textarea, radio, checkbox, dropdown, phone, email, url, file-upload, html, page break)
3. Turn on conditional logic on at least one field
4. Save the form
5. WPForms → Tools → Export → download the JSON

That JSON is your authoritative schema reference. Match its structure when generating the production form.

---

## Diagnostic workflow when an import fails

Symptoms: form imports, displays in builder, but Save or Preview crashes the site with "There has been a critical error" or "Updating failed. The response is not a valid JSON response."

In order:

1. **Check WordPress admin email** — fatal errors trigger an automatic email with the actual PHP error message (rate-limited to one per error type per 6 hours)
2. **Check the host error log** — Hostinger: hPanel → Files → File Manager → `public_html/error_log`; SiteGround: Site Tools → Statistics → Error Log; cPanel: usually `~/public_html/error_log`
3. **Check Chrome DevTools Network tab** — F12, reload the form preview URL, find the 500-status row, expand the Response tab
4. **Enable WP_DEBUG** as a fallback by adding to `wp-config.php`:
   ```php
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   define('WP_DEBUG_DISPLAY', false);
   ```
   then check `/wp-content/debug.log`
5. **If 30 minutes of debugging hasn't surfaced the cause, pivot to manual UI build** using the field-by-field build spec. WPForms's drag-and-drop builder validates every step and is guaranteed to produce a working form.

---

## Limitations and caveats

- **Verified on WPForms Pro 1.10.0.4 only.** Other versions may have schema differences. The diagnostic workflow above is the right starting point for adapting.
- **File-upload fields are excluded from the example JSON.** They have complex camera-capture metadata in WPForms 1.10 that's safer to add through the UI after import. Two minutes per field.
- **Save & Resume settings are not in the example JSON.** Configure in the WPForms UI after import (Settings → Save and Resume).
- **WPForms is a commercial plugin.** This toolkit doesn't include or redistribute any WPForms code. It's interoperability tooling for your own legitimately-licensed installation.

---

## Contributing

Found a schema requirement that's not documented here? Hit a crash this repo didn't predict? Open an issue with:

- Your WPForms version (Pro/Lite, exact number)
- The error message from your host's error log or wp-debug.log
- A minimal JSON snippet that reproduces it

Pull requests welcome — particularly for new field types, newer WPForms versions, or non-English locales.

---

## License

MIT. Use it, fork it, ship it inside your agency's workflow, charge clients to deploy it. Just keep the copyright notice.

---

## About Kore Komfort Solutions

This toolkit was extracted from client work at [Kore Komfort Solutions](https://korekomfortsolutions.com) — managed WordPress websites and digital intelligence reports for HVAC, plumbing, electrical, and remodeling contractors. If you run an agency serving contractors, or you're a contractor whose website isn't bringing in leads, [the contractor intelligence reports](https://korekomfortsolutions.com/contractor-intelligence-report/) score your current digital presence against your local competition and identify the highest-impact fixes.

Built by [Mike Warner](https://github.com/MikeWarnerkks) — 30 years in the trades, now helping independent contractors get found online.
