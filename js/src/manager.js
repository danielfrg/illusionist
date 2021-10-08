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
        this.modelIdToViewEl = {};
    }

    async loadState() {
        await this.loadInitialState();
        await this.loadOnChangeState();
    }

    /**
     * Loads the initial widget state from the HTML script tags
     */
    async loadInitialState() {
        // console.log("loadInitialState()");

        const stateTags = document.body.querySelectorAll(
            `script[type="${WIDGET_STATE_MIMETYPE}"]`
        );
        if (stateTags.length == 0) {
            console.warn(
                "IllusionistWidgetManager: Didn't find widget state on the HTML page"
            );
            return;
        }
        for (let stateTag of stateTags) {
            const widgetState = JSON.parse(stateTag.innerHTML);
            // console.log(widgetState);
            await this.set_state(widgetState);
        }
    }

    /**
     * Loads the onChange widget state from the HTML script tags
     */
    async loadOnChangeState() {
        // console.log("loadOnChangeState()")
        const onChangeTags = document.body.querySelectorAll(
            `script[type="${WIDGET_ONCHANGE_MIMETYPE}"]`
        );
        if (onChangeTags.length == 0) {
            return;
        }
        for (let tag of onChangeTags) {
            const onChangeState = JSON.parse(tag.innerHTML);
            // console.log(onChangeState);
            await this.setOnChangeState(onChangeState);
        }


        this.widgetAffects = {};
        this.onChangeState.control_widgets.forEach((controlId) => {
            this.widgetAffects[controlId] = [];
            for (let [valueWidgetID, obj] of Object.entries(
                this.onChangeState.onchange
            )) {
                if (obj.affected_by.includes(controlId)) {
                    this.widgetAffects[controlId].push(valueWidgetID);
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
            for (let [valueWidgetID, obj] of Object.entries(
                this.onChangeState.onchange
            )) {
                if (obj.affected_by.includes(controlId)) {
                    this.widgetAffects[controlId].push(valueWidgetID);
                }
            }
        });
    }

    /**
     * Build all the widgets
     */
     async renderAllWidgets() {
        const viewEls = document.body.querySelectorAll(
            `script[type="${WIDGET_VIEW_MIMETYPE}"]`
        );

        viewEls.forEach(async (viewEl) => {
            try {
                const widgetViewObject = JSON.parse(viewEl.innerHTML);
                const { model_id } = widgetViewObject;

                // We save this relations so we know where to render the widget
                this.modelIdToViewEl[model_id] = viewEl;

                await this.renderWidget(model_id);
            } catch (error) {
                console.error(error);
            }
        });
    }

    /*
     * Render one widget based on a ModelId
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
            // We create a new div in the parent of the script tag that has that modelID
            // We look for the viewEl on this.modelIdToViewEl

            const viewEl = this.modelIdToViewEl[modelId];

            if (viewEl) {
                widgetEl = document.createElement("div");
                widgetEl.id = modelId;
                viewEl.parentElement.insertBefore(widgetEl, viewEl);
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
     * Handles the state update when a Widget changes.
     * It will trigger the update of the Widget Views.
     */
    async onWidgetChange(modelId) {
        // console.log("onWidgetChange()");
        // console.log("ModelID: " + modelId);
        let state = await this.get_state();
        const onChange = this.onChangeState["onchange"];

        const valueWidgetAffectedBy = this.widgetAffects[modelId];

        if (!valueWidgetAffectedBy) {
            return;
        }
        // console.log("valueWidgetAffectedBy: " + valueWidgetAffectedBy)
        valueWidgetAffectedBy.forEach(async (valueWidgetID) => {
            const valueWidgetState = state["state"][valueWidgetID]["state"];
            const valueWidgetChangeData = onChange[valueWidgetID];
            const widgetIsAffectedBy = valueWidgetChangeData["affected_by"];

            // 1. Iterate the control widgets that affect this value widget
            // and get their values to make the hash
            let controlWidgetValues = [];
            for (let controlId of widgetIsAffectedBy) {
                const inputModel = state["state"][controlId]["state"];
                const valueKey = this.getWidgetValueKey(inputModel["_model_name"]);
                let inputValue = inputModel[valueKey];

                if (inputValue !== undefined) {
                    if (inputValue instanceof Array) {
                        controlWidgetValues.push(`[${inputValue.toString()}]`);
                    } else {
                        controlWidgetValues.push(inputValue);
                    }
                }
            }

            // 2. Make hash based on the controlWidgetValues
            let hash = this.hash_fn(controlWidgetValues);

            // 3. Update value for the widget ()
            const widgetNewValue = valueWidgetChangeData["values"][hash];
            if (widgetNewValue !== undefined) {
                const valueKey = this.getWidgetValueKey(valueWidgetState["_model_name"]);
                state["state"][valueWidgetID]["state"][valueKey] = widgetNewValue;

                // If it's an OutputModel clear the state
                // This avoids objects being rendered multiple times
                // This part is based on WidgetManager.clear_state()
                await resolvePromisesDict(this._models).then((models) => {
                    Object.keys(models).forEach((id) => {
                        let model = models[id];
                        if (valueWidgetID == id && model.name == "OutputModel") {
                            models[id].close();
                            this._models[model.model_id] = null;
                        }
                    });
                });

                await this.set_state(state);
                if (valueWidgetState["_model_name"] == "OutputModel") {
                    this.renderWidget(valueWidgetID);
                }
            }
        });
    }


    /**
     * For a model_name return the field name in the state that contains
     * the value for a widget
     *
     * Use that field name to update the values
     */
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
