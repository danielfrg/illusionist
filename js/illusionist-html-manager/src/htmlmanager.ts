// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { HTMLManager } from "@jupyter-widgets/html-manager";

import * as LuminoWidget from "@lumino/widgets";
import { DOMWidgetView } from "@jupyter-widgets/base";

export class IllusionistHTMLManager extends HTMLManager {
  onChangeValues: any;

  setOnChangeValues(values: {}) {
    this.onChangeValues = values;
  }

  /**
   * Display the specified view. Element where the view is displayed
   * is specified in the `options.el` argument.
   */
  async display_view(
    view: Promise<DOMWidgetView> | DOMWidgetView,
    el: HTMLElement
  ): Promise<void> {
    let widgetView = await view;
    LuminoWidget.Widget.attach(widgetView.pWidget, el);

    // Added
    // Adds one listener to the widget model
    widgetView.listenTo(widgetView.model, "change", () => {
      this.onWidgetChange();
    });
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
        let input_value = currentState["state"][input_id]["state"]["value"];
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
