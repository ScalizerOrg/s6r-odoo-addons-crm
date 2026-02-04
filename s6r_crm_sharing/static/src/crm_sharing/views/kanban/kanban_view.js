/** @odoo-module */

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { ProjectSharingTaskKanbanDynamicGroupList } from "@project/project_sharing/views/kanban/kanban_view";
import { KanbanModel } from "@web/views/kanban/kanban_model";

export class CrmSharingExtensionTaskKanbanDynamicGroupList extends ProjectSharingTaskKanbanDynamicGroupList {
    get context() {
        return {
            ...super.context,
            crm_kanban: true,
        };
    }
}

export class CrmSharingExtensionTaskKanbanModel extends KanbanModel {}

CrmSharingExtensionTaskKanbanModel.DynamicGroupList = CrmSharingExtensionTaskKanbanDynamicGroupList;

export const crmSharingExtensionKanbanView = {
    ...kanbanView,
    Model: CrmSharingExtensionTaskKanbanModel,
};

registry.category("views").add("crm_sharing_kanban", crmSharingExtensionKanbanView);
