import WidgetManager from "./manager";

const widgetManager = new WidgetManager();

async function init() {
    await widgetManager.loadState();
    await widgetManager.renderAllWidgets();
}

if (document.readyState === "complete") {
    init();
} else {
    window.addEventListener("load", init);
}
