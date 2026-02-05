/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { CrmSharingExtensionListRenderer } from "./list_renderer";

export const crmSharingExtensionListView = {
    ...listView,
    Renderer: CrmSharingExtensionListRenderer,
};

registry.category("views").add("crm_sharing_list", crmSharingExtensionListView);
