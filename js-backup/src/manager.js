import { HTMLManager } from "@jupyter-widgets/html-manager";

import * as LuminoWidget from "@lumino/widgets";
import * as base from "@jupyter-widgets/base";
import * as controls from "@jupyter-widgets/controls";
import { output } from "@jupyter-widgets/jupyterlab-manager";

if (typeof window !== "undefined" && typeof window.define !== "undefined") {
    window.define("@jupyter-widgets/base", base);
    window.define("@jupyter-widgets/controls", controls);
    window.define("@jupyter-widgets/output", output);
}

const WIDGET_MIMETYPE = "application/vnd.jupyter.widget-view+json";

export class WidgetManager extends HTMLManager {
    onChangeValues = {};

    async build_widgets() {
        // Set state
        const tags = document.body.querySelectorAll(
            'script[type="application/vnd.jupyter.widget-state+json"]'
        );
        for (let i = 0; i != tags.length; ++i) {
            const stateTag = tags[i];
            const widgetState = JSON.parse(stateTag.innerHTML);
            console.log(widgetState);
            await this.set_state(widgetState);
        }
        console.log(1);

        // Set onChange values
        const onChangeTags = document.body.querySelectorAll(
            'script[type="application/vnd.illusionist.widget-onchange+json"]'
        );
        for (let i = 0; i != onChangeTags.length; ++i) {
            const tag = onChangeTags[i];
            this.onChangeValues = JSON.parse(tag.innerHTML);
        }
        console.log(2);

        // Display models
        // const models = await this.get_state
        const viewTags = document.body.querySelectorAll(
            'script[type="application/vnd.jupyter.widget-view+json"]'
        );
        for (let i = 0; i != viewTags.length; ++i) {
            try {
                const viewtag = viewTags[i];
                const widgetViewObject = JSON.parse(viewtag.innerHTML);
                const { model_id } = widgetViewObject;
                console.log(this._models);
                console.log(model_id);
                const model = await this._models[model_id];
                console.log(model);
                const widgetel = document.createElement("div");
                viewtag.parentElement.insertBefore(widgetel, viewtag);
                const view = await this.display_model(undefined, model, {
                    el: widgetel,
                });

                view.listenTo(view.model, "change", () => {
                    this.onWidgetChange();
                });

                // console.log(view);
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

    setOnChangeValues(values) {
        this.onChangeValues = values;
    }

    /**
     * Handles the state update
     * It will trigger the update of the Widget Views.
     */
    async onWidgetChange() {
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
