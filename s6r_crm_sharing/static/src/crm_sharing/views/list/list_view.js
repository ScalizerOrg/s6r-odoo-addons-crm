import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { RelationalModel } from "@web/model/relational_model/relational_model";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { CrmSharingExtensionListRenderer } from "./list_renderer";

export const crmSharingExtensionListView = {
    ...listView,
    Model: RelationalModel,
    ControlPanel: ControlPanel,
    Renderer: CrmSharingExtensionListRenderer,
};

registry.category("views").add("crm_sharing_list", crmSharingExtensionListView);
