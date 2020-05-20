// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { HTMLManager } from "@jupyter-widgets/html-manager";

import * as LuminoWidget from "@lumino/widgets";
import { DOMWidgetView } from "@jupyter-widgets/base";

export class IllusionistHTMLManager extends HTMLManager {
  onChangeValues: any;

  setOnChangeValues(values: {}) {
    this.onChangeValues = values;
    // console.log(this.onChangeValues);
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

    // Change state
    const a = [];
    for (var control_widget_id of this.onChangeValues["controls"]) {
      // console.log(control_widget_id);
      var widget_value =
        currentState["state"][control_widget_id]["state"]["value"];
      a.push(control_widget_id + "=" + widget_value);
    }
    var hash = a.join(",");
    // console.log(hash);
    var widgetValues = this.onChangeValues["values"][hash];
    // console.log(widgetValues);

    for (var key of Object.keys(widgetValues)) {
      currentState["state"][key]["state"]["value"] = widgetValues[key];
    }

    this.set_state(currentState);
  }
}
