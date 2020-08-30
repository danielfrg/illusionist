import IllusionistWidgetManager from "./manager";

const widgetManager = new IllusionistWidgetManager();

async function init() {
    await widgetManager.loadState();
    await widgetManager.renderAllWidgets();
}

if (document.readyState === "complete") {
    init();
} else {
    window.addEventListener("load", init);
}
