/** @odoo-module */

import { CrmChatterComposer as ChatterComposer } from "./chatter_composer";
import { ChatterContainer } from "@project/project_sharing/components/chatter/chatter_container";

export class CrmChatterContainer extends ChatterContainer {
    get crmSharingId() {
        return this.props.crmSharingId || this.props.projectSharingId;
    }

    get composerProps() {
        return {
            ...super.composerProps,
            crmSharingId: this.crmSharingId,
        };
    }

    messagesParams(props) {
        return {
            ...super.messagesParams(props),
            crm_sharing_id: this.crmSharingId,
        };
    }
}

CrmChatterContainer.components = {
    ...ChatterContainer.components,
    ChatterComposer,
};

CrmChatterContainer.props = {
    ...ChatterContainer.props,
    crmSharingId: { type: Number, optional: true },
    projectSharingId: { type: Number, optional: true },
};

CrmChatterContainer.defaultProps = {
    ...ChatterContainer.defaultProps,
    projectSharingId: 0,
};
