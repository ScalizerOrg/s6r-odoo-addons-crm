import { patch } from "@web/core/utils/patch";
import { MediaPlugin } from "@html_editor/main/media/media_plugin";

// PowerboxPlugin.setup() accesses getInsertMediaPowerboxItem().keywords before
// MediaPlugin.setup() sets availableTabs — guard against undefined.
patch(MediaPlugin.prototype, {
    getInsertMediaPowerboxItem() {
        const self = this;
        return {
            ...super.getInsertMediaPowerboxItem(),
            get keywords() {
                return (self.availableTabs || []).map((tab) => tab.title);
            },
        };
    },
});
