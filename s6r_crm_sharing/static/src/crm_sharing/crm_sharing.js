import { ProjectSharingWebClient } from '@project/project_sharing/project_sharing';
import { session } from '@web/session';
import { patch } from '@web/core/utils/patch';

patch(ProjectSharingWebClient.prototype, {
    async loadRouterState() {
        const { action_name, active_id, active_model, open_task_action } = session;
        if (action_name && action_name === 's6r_crm_sharing.crm_lead_action_sharing') {
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
        } else {
            await super.loadRouterState();
        }
    }
});
