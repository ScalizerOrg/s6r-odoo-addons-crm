import { browser } from "@web/core/browser/browser";
import { router } from "@web/core/browser/router";
import { patch } from "@web/core/utils/patch";

patch(router, {
    stateToUrl(state) {
        const url = super.stateToUrl(state);
        // project_sharing's patch (applied before ours) already replaced "/odoo" with "/my/projects",
        // so the CRM path arrives here as "/my/projects/crm_sharing[/id]".
        return url.replace("/my/projects/crm_sharing", "/my/opportunities/crm_sharing");
    },
    urlToState(urlObj) {
        urlObj.pathname = urlObj.pathname.replace(
            /\/my\/opportunities\/crm_sharing/,
            "/odoo/crm_sharing"
        );
        const state = super.urlToState(urlObj);
        return state;
    },
});

// Re-initialize router state after patching stateToUrl/urlToState.
router.replaceState(router.urlToState(new URL(browser.location)));
