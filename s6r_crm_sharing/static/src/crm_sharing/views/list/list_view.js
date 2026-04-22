/** @odoo-module */

import { CrmSharingExtensionListRenderer } from "./list_renderer";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

export const crmSharingExtensionListView = {
    ...listView,
    Renderer: CrmSharingExtensionListRenderer,
};

registry.category("views").add("crm_sharing_list", crmSharingExtensionListView);
