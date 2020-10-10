import { HTMLManager, requireLoader } from "@jupyter-widgets/html-manager";
import { resolvePromisesDict } from "@jupyter-widgets/base";
import Papa from "papaparse";

export const WIDGET_STATE_MIMETYPE =
    "application/vnd.jupyter.widget-state+json";
export const WIDGET_VIEW_MIMETYPE = "application/vnd.jupyter.widget-view+json";
export const WIDGET_ONCHANGE_MIMETYPE =
    "application/vnd.illusionist.widget-onchange+json";

const NUMERIC_WIDGETS = [
    "IntSliderModel",
    "FloatSlider",
    "FloatLogSlider",
    "IntRangeSliderModel",
    "FloatRangeSlider",
    "BoundedIntTextModel",
    "BoundedFloatText",
    "IntText",
    "FloatText",
    "IntProgressModel",
    "FloatProgressModel",
];

const BOOLEAN_WIDGETS = ["ToggleButtonModel", "CheckboxModel", "ValidModel"];

const SELECTION_WIDGETS = [
    "DropdownModel",
    "RadioButtonsModel",
    "SelectModel",
    "SelectionSliderModel",
    "SelectionRangeSliderModel",
    "ToggleButtonsModel",
    "SelectMultipleModel",
];

const STRING_WIDGETS = [
    "TextModel",
    "TextAreaModel",
    "LabelModel",
    "HTMModelL",
    "HTMLMathModel",
    "ImageModel",
];

export default class IllusionistWidgetManager extends HTMLManager {
    constructor() {
        super();
        this.loader = requireLoader;
        this.onChangeState = null;
        this.modelIdToViewScriptTag = {};
    }

    async loadState() {
        await this.loadInitialState();
        await this.loadOnChangeState();
    }

    /**
     * Loads the widget initial state from the HTML script tags
     */
    async loadInitialState() {
        const stateTags = document.body.querySelectorAll(
            `script[type="${WIDGET_STATE_MIMETYPE}"]`
        );
        if (stateTags.length == 0) {
            console.log(
                "IllusionistWidgetManager: Didn't find widget state on the HTML page"
            );
            return;
        }
        for (let stateTag of stateTags) {
            const widgetState = JSON.parse(stateTag.innerHTML);
            await this.set_state(widgetState);
        }
    }

    /**
     * Loads the onChange widget state from the HTML script tags
     */
    async loadOnChangeState() {
        const onChangeTags = document.body.querySelectorAll(
            `script[type="${WIDGET_ONCHANGE_MIMETYPE}"]`
        );
        if (onChangeTags.length == 0) {
            return;
        }
        for (let tag of onChangeTags) {
            const onChangeState = JSON.parse(tag.innerHTML);
            await this.setOnChangeState(onChangeState);
        }
        this.widgetAffects = {};

        this.onChangeState.control_widgets.forEach((controlId) => {
            this.widgetAffects[controlId] = [];
            for (let [outputId, obj] of Object.entries(
                this.onChangeState.onchange
            )) {
                if (obj.affected_by.includes(controlId)) {
                    this.widgetAffects[controlId].push(outputId);
                }
            }
        });
    }

    /**
     * Equivalent of WidgetManager.set_state for the onChange State from Illusionist
     * @param {Object} onChangeState
     */
    async setOnChangeState(onChangeState) {
        this.onChangeState = onChangeState;
        this.widgetAffects = {};

        this.onChangeState.control_widgets.forEach((controlId) => {
            this.widgetAffects[controlId] = [];
            for (let [outputId, obj] of Object.entries(
                this.onChangeState.onchange
            )) {
                if (obj.affected_by.includes(controlId)) {
                    this.widgetAffects[controlId].push(outputId);
                }
            }
        });
    }

    /*
     * Render one widgetd based on a ModelId
     */
    async renderWidget(modelId) {
        const model = await this.get_model(modelId);
        const view = await this.create_view(model);

        let widgetEl = document.body.querySelector(`div[id="${modelId}"]`);
        if (widgetEl) {
            // If there is a div with ID equal to the modelId
            // Render the widget inside that element
            widgetEl.innerHTML = "";
        } else {
            // If there is not a div with ID equal to the modelID
            // We create a div in the parent of the script tag that has that modelID
            // We look for the viewScriptTag on the this.modelIdToViewScriptTag map

            const viewScriptTag = this.modelIdToViewScriptTag[modelId];

            if (viewScriptTag) {
                widgetEl = document.createElement("div");
                widgetEl.id = modelId;
                viewScriptTag.parentElement.insertBefore(
                    widgetEl,
                    viewScriptTag
                );
            } else {
                console.error(
                    "Couldn't not find an element where to render the widget: " +
                        modelId
                );
                return;
            }
        }

        // Render Widget
        await this.display_view("", view, { el: widgetEl });

        // Set listeners for onChange state
        if (this.onChangeState) {
            if (this.onChangeState.control_widgets.includes(modelId)) {
                // If its on the list of control widgets add the listener
                view.listenTo(model, "change", () => {
                    this.onWidgetChange(modelId);
                });
            }
        }
    }

    /**
     * Build all the widgets
     */
    async renderAllWidgets() {
        const viewScriptTags = document.body.querySelectorAll(
            `script[type="${WIDGET_VIEW_MIMETYPE}"]`
        );

        viewScriptTags.forEach(async (viewScriptTag) => {
            try {
                const widgetViewObject = JSON.parse(viewScriptTag.innerHTML);
                const { model_id } = widgetViewObject;

                // We save this map so we know where to render the widget
                this.modelIdToViewScriptTag[model_id] = viewScriptTag;

                await this.renderWidget(model_id);
            } catch (error) {
                console.error(error);
            }
        });
    }

    /**
     * Handles the state update when a Widget changes.
     * It will trigger the update of the Widget Views.
     */
    async onWidgetChange(modelId) {
        // console.log("onWidgetChange");
        // console.log(modelId);
        let state = await this.get_state();
        const onChange = this.onChangeState["onchange"];

        const outputsAffected = this.widgetAffects[modelId];

        if (!outputsAffected) {
            return;
        }

        outputsAffected.forEach(async (outputId) => {
            const outputModel = state["state"][outputId]["state"];
            const outputOnChangeData = onChange[outputId];
            const outputAffectedBy = outputOnChangeData["affected_by"];

            // console.log("Affected by:");
            // console.log(outputAffectedBy);

            // 1. Iterate controlValues and get the values to make the has
            let controlValues = [];
            for (let controlId of outputAffectedBy) {
                const inputModel = state["state"][controlId]["state"];
                const key = this.getWidgetValueKey(inputModel["_model_name"]);
                let inputValue = inputModel[key];

                if (inputValue !== undefined) {
                    if (inputValue instanceof Array) {
                        controlValues.push(`[${inputValue.toString()}]`);
                    } else {
                        controlValues.push(inputValue);
                    }
                }
            }

            // 2. Make hash based on the controlValues
            let hash = this.hash_fn(controlValues);

            // 3. Update affected widgets
            const outputValue = outputOnChangeData["values"][hash];
            if (outputValue !== undefined) {
                const key = this.getWidgetValueKey(outputModel["_model_name"]);
                state["state"][outputId]["state"][key] = outputValue;

                // If it's an OutputModel clear the state
                // This avoids objects being rendered multiple times
                // This part is based on WidgetManager.clear_state()
                await resolvePromisesDict(this._models).then((models) => {
                    Object.keys(models).forEach((id) => {
                        let model = models[id];
                        if (model.name == "OutputModel") {
                            models[id].close();
                            this._models[model.model_id] = null;
                        }
                    });
                });

                await this.set_state(state);
                if (outputModel["_model_name"] == "OutputModel") {
                    this.renderWidget(outputId);
                }
            }
        });
    }

    getWidgetValueKey(model_name) {
        if (SELECTION_WIDGETS.includes(model_name)) {
            return "index";
        } else if (model_name == "OutputModel") {
            return "outputs";
        } else if (
            NUMERIC_WIDGETS.includes(model_name) ||
            BOOLEAN_WIDGETS.includes(model_name) ||
            STRING_WIDGETS.includes(model_name)
        ) {
            return "value";
        }
    }

    hash_fn(inputs) {
        let quotes = [];
        for (let input of inputs) {
            if (typeof input === "number") {
                quotes.push(false);
            } else {
                quotes.push(true);
            }
        }

        var results = Papa.unparse([inputs], {
            quotes: quotes,
            quoteChar: '"',
        });
        return results;
    }
}
