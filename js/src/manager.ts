import { HTMLManager } from "@jupyter-widgets/html-manager";
import { DOMWidgetModel } from "@jupyter-widgets/base";

import Papa from "papaparse";

const WIDGET_STATE_MIMETYPE = "application/vnd.jupyter.widget-state+json";
const WIDGET_VIEW_MIMETYPE = "application/vnd.jupyter.widget-view+json";
const WIDGET_ONCHANGE_MIMETYPE =
    "application/vnd.illusionist.widget-onchange+json";

export class WidgetManager extends HTMLManager {
    public onChangeValues: any = {};

    /**
     * Main entry point to build the widgets to the DOM
     */
    public async build_widgets() {
        // Set state
        await this.load_state();
        await this.load_onchange();

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
                // console.log(model_id);
                // console.log(model);
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
        const state = await this.get_state();
        // console.log(state);
        const onChange = this.onChangeValues["onchange"];

        let i = 1;
        for (let output_id in onChange) {
            console.log("----");
            console.log("Output ID:");
            console.log(output_id);
            const this_info = onChange[output_id];
            const affected_by_ids = this_info["affected_by"];

            // if (model.)

            let inputs = [];
            for (let input_id of affected_by_ids) {
                const widget_state = state["state"][input_id]["state"];
                console.log("Input ID:");
                console.log(input_id);
                let input_value = widget_state["value"];
                let index_value = widget_state["index"];
                console.log("Input/index Value:");
                if (input_value !== undefined) {
                    // Ints and Booleans
                    // console.log(input_value);
                    if (
                        typeof input_value === "number" ||
                        typeof input_value === "boolean"
                    ) {
                        inputs.push(input_value);
                    } else if (input_value instanceof Array) {
                        // IntRangeSlider
                        inputs.push(`[${input_value.toString()}]`);
                    }
                } else if (index_value !== undefined) {
                    // Selection widgets
                    // console.log(index_value);
                    if (typeof index_value === "number") {
                        inputs.push(index_value);
                    } else if (index_value instanceof Array) {
                        // SelectMultiple
                        inputs.push(`[${index_value.toString()}]`);
                    }
                }
            }
            if (i == 2) {
                // break;
            }
            i = i + 1;

            console.log("Inputs final:");
            console.log(inputs);
            let hash = this.hash_fn(inputs);
            console.log("Hash:");
            console.log(hash);

            const output_value = this_info["values"][hash];
            console.log("Output value");
            console.log(output_value);
            if (output_value !== undefined) {
                state["state"][output_id]["state"]["value"] = output_value;
            }
        }

        this.set_state(state);
    }

    public hash_fn(inputs: Array<any>) {
        let quotes = [];
        for (let input of inputs) {
            if (typeof input === "number") {
                quotes.push(false);
            }
            quotes.push(true);
        }
        // console.log(quotes);

        var results = Papa.unparse([inputs], {
            quotes: quotes,
            quoteChar: '"',
        });
        // console.log("!!!!");
        // console.log(results);
        return results;
    }
}
