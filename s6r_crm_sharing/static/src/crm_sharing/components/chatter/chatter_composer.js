/** @odoo-module */

import { ChatterComposer } from "@project/project_sharing/components/chatter/chatter_composer";

export class CrmChatterComposer extends ChatterComposer {
    prepareMessageData() {
        return {
            ...super.prepareMessageData(),
            crm_sharing_id: this.props.crmSharingId,
        };
    }
}

CrmChatterComposer.props = {
    ...ChatterComposer.props,
    crmSharingId: { type: Number, optional: true },
    projectSharingId: { type: Number, optional: true },
};

CrmChatterComposer.defaultProps = {
    ...ChatterComposer.defaultProps,
    projectSharingId: 0,
};
