/** @odoo-module */

import { ProjectSharingFormRenderer } from "@project/project_sharing/views/form/project_sharing_form_renderer";
import { CrmChatterContainer as ChatterContainer } from '../../components/chatter/chatter_container';

export class CrmSharingExtensionFormRenderer extends ProjectSharingFormRenderer { }
CrmSharingExtensionFormRenderer.components = {
    ...ProjectSharingFormRenderer.components,
    ChatterContainer,
};
