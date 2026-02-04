/** @odoo-module */

import { registry } from "@web/core/registry";
import { projectSharingExtensionListView } from "@project/project_sharing/views/list/list_view";
import { CrmSharingExtensionListRenderer } from "./list_renderer";

export const crmSharingExtensionListView = {
    ...projectSharingExtensionListView,
    Renderer: CrmSharingExtensionListRenderer,
};

registry.category("views").add("crm_sharing_list", crmSharingExtensionListView);
