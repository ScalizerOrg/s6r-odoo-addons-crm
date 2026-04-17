import { patch } from "@web/core/utils/patch";
import { MediaPlugin } from "@html_editor/main/media/media_plugin";

// PowerboxPlugin.setup() accesses getInsertMediaPowerboxItem().keywords before
// MediaPlugin.setup() sets availableTabs — guard against undefined.
// Spread evaluates the parent getter (crash), so we use Object.create to inherit
// without triggering it, then override keywords safely.
patch(MediaPlugin.prototype, {
    getInsertMediaPowerboxItem() {
        const self = this;
        const parent = super.getInsertMediaPowerboxItem();
        const item = Object.create(parent);
        Object.defineProperty(item, "keywords", {
            get() {
                return (self.availableTabs || []).map((tab) => tab.title);
            },
            enumerable: true,
            configurable: true,
        });
        return item;
    },
});
