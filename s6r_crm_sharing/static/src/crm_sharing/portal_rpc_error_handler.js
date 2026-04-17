import { RPCError } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";
import { UncaughtPromiseError } from "@web/core/errors/error_service";

// swallowAllVisitorErrors (sequence 0) silently drops all errors for non-internal
// users. Portal operators need to see server-side validation errors as notifications.
// Run at sequence -1 to intercept RPCErrors before they are swallowed.
function portalRpcErrorHandler(env, error, originalError) {
    if (user.isInternalUser) {
        return false;
    }
    if (!(error instanceof UncaughtPromiseError)) {
        return false;
    }
    if (!(originalError instanceof RPCError)) {
        return false;
    }
    error.unhandledRejectionEvent.preventDefault();
    const message = originalError.data?.message || originalError.message;
    env.services.notification.add(message, { type: "danger", sticky: true });
    return true;
}

registry
    .category("error_handlers")
    .add("portalRpcErrorHandler", portalRpcErrorHandler, { sequence: -1 });
