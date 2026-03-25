import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { RelationalModel } from "@web/model/relational_model/relational_model";
import { ControlPanel } from "@web/search/control_panel/control_panel";

export class CrmSharingKanbanModel extends RelationalModel {
    async _webReadGroup(config) {
        config.context = {
            ...config.context,
            crm_kanban: true,
        };
        return super._webReadGroup(...arguments);
    }
}

export const crmSharingExtensionKanbanView = {
    ...kanbanView,
    Model: CrmSharingKanbanModel,
    ControlPanel: ControlPanel,
};

registry.category("views").add("crm_sharing_kanban", crmSharingExtensionKanbanView);
