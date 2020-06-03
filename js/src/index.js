import { WidgetManager } from "./manager";
// import { renderMathJax } from './mathjax';

// import "../style/index.css";

console.log("index.js");

var widgetManager = new WidgetManager();

async function init() {
    await widgetManager.build_widgets();
    // illusionist.renderMathJax();
}

if (document.readyState === "complete") {
    init();
} else {
    window.addEventListener("load", init);
}
