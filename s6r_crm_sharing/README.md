# S6R CRM Sharing

Portal-based sharing interface for CRM opportunities. Allows portal users (customers, partners) to view and interact with their assigned leads/opportunities through a secure, restricted web interface.

## Features

- **Portal access** — Customers and partners reach opportunities at `/my/opportunities`
- **Multiple views** — Kanban, list, and form views tailored for portal context
- **Field-level security** — Portal users can only read/write explicitly allowed fields
- **Integrated chatter** — Messaging and followers work in portal context
- **Responsive layout** — Chatter renders as sidebar (≥XXL screens) or below form (smaller screens)
- **Iframe embedding** — Portal wraps a full backend-style web client in an iframe for seamless UX

## Architecture

The module follows Odoo's project sharing pattern, extended for CRM:

```
Portal user → /my/opportunities
    └─ iframe → /my/opportunities/crm_sharing
        └─ CrmSharingWebClient
            └─ crm_lead_action_sharing (kanban/list/form)
```

The iframe loads a stripped backend web client (no menu bar) that executes the opportunities action directly.

## Security

Portal users (`base.group_portal`) receive:

| Permission | Allowed |
|------------|---------|
| Read       | ✓       |
| Write      | ✓ (restricted fields only) |
| Create     | ✓ (restricted fields only) |
| Delete     | ✗       |

**Readable fields** (24): name, partner_id, email_from, phone, contact_name, mobile, campaign_id, source_id, medium_id, tag_ids, type, stage_id, probability, expected_revenue, priority, kanban_state, team_id, user_id, user_company_ids, message_follower_ids, access_token, active, company_id, description, email_cc

**Writable fields** (12): name, partner_id, phone, email_from, description, expected_revenue, probability, priority, kanban_state, tag_ids, team_id, user_id, message_follower_ids

Any write attempt on fields outside this set raises `AccessError`.

## Dependencies

- `project` — Base project module (provides project sharing framework)
- `website_crm_partner_assign` — Portal routing for CRM partner assignment

## Module Structure

```
s6r_crm_sharing/
├── models/
│   └── crm_lead.py              # Field-level access control for portal users
├── controllers/
│   └── portal.py                # Routes: /my/opportunities and /my/opportunities/crm_sharing
├── views/
│   └── crm_sharing_views.xml    # Kanban, list, quick-create, and form views + window action
├── templates/
│   └── crm_sharing_templates.xml # Portal wrapper, iframe, and embedded web client templates
├── security/
│   └── ir.model.access.csv      # Portal user permissions on crm.lead
└── static/src/crm_sharing/
    ├── crm_sharing.js            # Main web client (CrmSharingWebClient)
    ├── views/
    │   ├── kanban/kanban_view.js
    │   ├── list/list_view.js + list_renderer.js
    │   └── form/                 # Controller, renderer, compiler
    └── components/chatter/       # CRM-aware chatter container and composer
```

## Configuration

No post-install configuration required. Once installed, portal users with access to CRM leads can navigate to `/my/opportunities`.

The session info injected into the iframe includes `crm_lead_action_sharing` as the startup action. To change which leads are visible to portal users, configure domain filters on that action or restrict `crm.lead` record rules.

## Author

Scalizer — License LGPL-3
