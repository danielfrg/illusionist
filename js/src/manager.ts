import { HTMLManager } from "@jupyter-widgets/html-manager";

import { DOMWidgetModel, DOMWidgetView } from "@jupyter-widgets/base";
import * as LuminoWidget from "@lumino/widgets";

// if (
//     typeof window !== "undefined" &&
//     typeof (window as any).define !== "undefined"
// ) {
//     (window as any).define("@jupyter-widgets/base", base);
//     (window as any).define("@jupyter-widgets/controls", controls);
//     // (window as any).define("@jupyter-widgets/output", output);
// }

const WIDGET_STATE_MIMETYPE = "application/vnd.jupyter.widget-state+json";
const WIDGET_VIEW_MIMETYPE = "application/vnd.jupyter.widget-view+json";
const WIDGET_ONCHANGE_MIMETYPE =
    "application/vnd.illusionist.widget-onchange+json";

export class WidgetManager extends HTMLManager {
    public onChangeValues: any = {};
    // public models_ids: String[] = [];

    /**
     * Main entry point to build the widgets to the DOM
     */
    public async build_widgets() {
        // Set state
        this.load_state();
        this.load_onchange();

        // Display models
        const viewTags = document.body.querySelectorAll(
            `script[type="${WIDGET_VIEW_MIMETYPE}"]`
        );
        for (let i = 0; i != viewTags.length; ++i) {
            try {
                const viewtag = viewTags[i];
                const widgetViewObject = JSON.parse(viewtag.innerHTML);
                const { model_id } = widgetViewObject;
                const model = await this.get_model(model_id);
                const widgetEl = document.createElement("div");
                if (model && viewtag && viewtag.parentElement) {
                    // console.log(model_id);
                    // console.log(model);
                    viewtag.parentElement.insertBefore(widgetEl, viewtag);
                    let dommodel: DOMWidgetModel = model as DOMWidgetModel;
                    const view = await this.create_view(dommodel);
                    await this.display_view(view, widgetEl);

                    view.listenTo(view.model, "change", () => {
                        this.onWidgetChange();
                    });
                }
            } catch (error) {
                console.error(error);
                // Each widget view tag rendering is wrapped with a try-catch statement.
                //
                // This fixes issues with widget models that are explicitely "closed"
                // but are still referred to in a previous cell output.
                // Without the try-catch statement, this error interupts the loop and
                // prevents the rendering of further cells.
                //
                // This workaround may not be necessary anymore with templates that make use
                // of progressive rendering.
            }
        }
    }

    /**
     * Loads the widget state.
     */
    public async load_state() {
        const tags = document.body.querySelectorAll(
            `script[type="${WIDGET_STATE_MIMETYPE}"]`
        );
        for (let stateTag of tags) {
            const widgetState = JSON.parse(stateTag.innerHTML);
            console.log(widgetState);
            await this.set_state(widgetState);
        }
    }

    /**
     * Loads the onchange state.
     */
    public async load_onchange() {
        const onChangeTags = document.body.querySelectorAll(
            `script[type="${WIDGET_ONCHANGE_MIMETYPE}"]`
        );
        for (let i = 0; i != onChangeTags.length; ++i) {
            const tag = onChangeTags[i];
            this.onChangeValues = JSON.parse(tag.innerHTML);
        }
        console.log(this.onChangeValues);
    }

    /**
     * Handles the state update
     * It will trigger the update of the Widget Views.
     */
    public async onWidgetChange() {
        const currentState = await this.get_state();
        // console.log(currentState);

        for (let output_id in this.onChangeValues["onchange"]) {
            // console.log(output_id);
            const this_info = this.onChangeValues["onchange"][output_id];
            const affected_by_ids = this_info["affected_by"];

            let inputs = [];
            for (let input_id of affected_by_ids) {
                let input_value =
                    currentState["state"][input_id]["state"]["value"];
                if (input_value) {
                    input_value = input_value.toString();
                    // console.log("Input:");
                    // console.log(input_value);
                    // console.log(input_value.indexOf(","));
                    // If there are multiple values (Range Sliders) make them a list
                    if (input_value.indexOf(",") > 0) {
                        input_value = `[${input_value}]`;
                    }
                }
                inputs.push(input_value);
            }
            let hash = inputs.join("|");

            const output_value = this_info["values"][hash];
            // console.log("hash:");
            // console.log(hash);
            // console.log(output_value);
            currentState["state"][output_id]["state"]["value"] = output_value;
        }

        this.set_state(currentState);
    }
}
