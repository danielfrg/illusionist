import IllusionistWidgetManager from "./manager";

let widgetManager;

async function init() {
    widgetManager = new IllusionistWidgetManager();
    await widgetManager.loadState();
    await widgetManager.renderAllWidgets();
}

if (document.readyState === "complete") {
    init();
} else {
    window.addEventListener("load", init);
}
