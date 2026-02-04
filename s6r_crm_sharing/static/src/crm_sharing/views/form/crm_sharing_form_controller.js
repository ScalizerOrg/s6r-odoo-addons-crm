/** @odoo-module */

import { ProjectSharingFormController } from "@project/project_sharing/views/form/project_sharing_form_controller";
import { useViewCompiler } from '@web/views/view_compiler';
import { CrmSharingExtensionChatterCompiler } from './crm_sharing_form_compiler';
import { CrmChatterContainer as ChatterContainer } from '../../components/chatter/chatter_container';

export class CrmSharingExtensionFormController extends ProjectSharingFormController {
    setup() {
        super.setup();
        const { arch } = this.archInfo;
        const xmlDocChatter = this.archInfo.xmlDoc.querySelector("div.oe_chatter");
        const template = document.createElement('t');
        if (xmlDocChatter && xmlDocChatter.parentNode.nodeName === "form") {
            template.appendChild(xmlDocChatter.cloneNode(true));
        }
        const mailTemplates = useViewCompiler(CrmSharingExtensionChatterCompiler, arch, { Mail: template }, {});
        this.mailTemplate = mailTemplates.Mail;
    }
}

CrmSharingExtensionFormController.components = {
    ...ProjectSharingFormController.components,
    ChatterContainer,
}
