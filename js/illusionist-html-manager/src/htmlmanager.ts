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
    var widgetView = await view;
    LuminoWidget.Widget.attach(widgetView.pWidget, el);

    // Added
    // Adds one listener to the widget model
    widgetView.listenTo(widgetView.model, "change", () => {
      this.onWidgetChange();
    });
  }

  /**
   * Handles the update of the state of the Manager.
   * It will trigger the update of the Widget Views.
   */
  async onWidgetChange() {
    var currentState = await this.get_state();
    for (var output_id in this.onChangeValues["onchange"]) {
      console.log(output_id)
      var this_info = this.onChangeValues["onchange"][output_id]
      var affected_by_ids = this_info["affected_by"]
      console.log(affected_by_ids)

      var a = [];
      for (var input_id of affected_by_ids) {
        a.push(currentState["state"][input_id]["state"]["value"])
      }
      var hash = a.join(",");
      console.log(hash)

      var output_value = this_info["values"][hash]
      console.log(output_value)
      currentState["state"][output_id]["state"]["value"] = output_value;
    }

    this.set_state(currentState);
  }
}
