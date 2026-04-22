/** @odoo-module */

import { CrmSharingExtensionFormController } from './crm_sharing_form_controller';
import { CrmSharingExtensionFormRenderer } from './crm_sharing_form_renderer';
import { formView } from '@web/views/form/form_view';
import { registry } from "@web/core/registry";

export const crmSharingExtensionFormView = {
    ...formView,
    Controller: CrmSharingExtensionFormController,
    Renderer: CrmSharingExtensionFormRenderer,
};

registry.category("views").add("crm_sharing_form", crmSharingExtensionFormView);
