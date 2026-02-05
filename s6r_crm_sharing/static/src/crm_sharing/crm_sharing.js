/** @odoo-module **/

import { ProjectSharingWebClient } from '@project/project_sharing/project_sharing';
import { session } from '@web/session';

export class CrmSharingWebClient extends ProjectSharingWebClient {
    async _showView() {
        const { action_name, active_id, active_model, open_task_action } = session;
        await this.actionService.doAction(
            action_name,
            {
                clearBreadcrumbs: true,
                additionalContext: {
                    active_id: active_id,
                    active_model: active_model,
                    active_id_chatter: active_id,
                }
            }
        );
        if (open_task_action) {
            await this.actionService.doAction(open_task_action);
        }
    }
}

CrmSharingWebClient.template = 's6r_crm_sharing.CrmSharingWebClient';
