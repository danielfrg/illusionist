// NOTE: this file is not transpiled, async/await is the only modern feature we use here
require(["static/illusionist"], function (illusionist) {
    // requirejs doesn't like to be passed an async function, so create one inside
    (async function () {
        var widgetManager = new illusionist.WidgetManager();

        async function init() {
            await widgetManager.build_widgets();
            // illusionist.renderMathJax();
        }

        if (document.readyState === "complete") {
            init();
        } else {
            window.addEventListener("load", init);
        }
    })();
});
