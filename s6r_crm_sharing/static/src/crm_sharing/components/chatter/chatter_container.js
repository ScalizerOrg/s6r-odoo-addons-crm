/** @odoo-module */

import { ChatterContainer } from "@project/project_sharing/components/chatter/chatter_container";
import { CrmChatterComposer as ChatterComposer } from "./chatter_composer";

export class CrmChatterContainer extends ChatterContainer {
    get composerProps() {
        return {
            ...super.composerProps,
            crmSharingId: this.props.crmSharingId,
        };
    }

    messagesParams(props) {
        return {
            ...super.messagesParams(props),
            crm_sharing_id: props.crmSharingId,
        };
    }
}

CrmChatterContainer.components = {
    ...ChatterContainer.components,
    ChatterComposer,
};

CrmChatterContainer.props = {
    ...ChatterContainer.props,
    crmSharingId: Number,
};
