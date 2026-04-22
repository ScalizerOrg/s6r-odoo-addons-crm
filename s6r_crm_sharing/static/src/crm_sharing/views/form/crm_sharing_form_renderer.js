/** @odoo-module */

import { CrmChatterContainer as ChatterContainer } from '../../components/chatter/chatter_container';
import { ProjectSharingFormRenderer } from "@project/project_sharing/views/form/project_sharing_form_renderer";

export class CrmSharingExtensionFormRenderer extends ProjectSharingFormRenderer { }
CrmSharingExtensionFormRenderer.components = {
    ...ProjectSharingFormRenderer.components,
    ChatterContainer,
};
