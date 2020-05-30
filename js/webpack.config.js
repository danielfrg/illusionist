var path = require("path");

var rules = [
    { test: /\.css$/, use: ["style-loader", "css-loader"] },
    // required to load font-awesome
    {
        test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
        use:
            "url-loader?limit=10000&mimetype=application/font-woff&publicPath=/static/",
    },
    {
        test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
        use:
            "url-loader?limit=10000&mimetype=application/font-woff&publicPath=/static/",
    },
    {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        use:
            "url-loader?limit=10000&mimetype=application/octet-stream&publicPath=/static/",
    },
    {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        use: "file-loader&publicPath=/static/",
    },
    {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        use:
            "url-loader?limit=10000&mimetype=image/svg+xml&publicPath=/static/",
    },
];

var distRoot = path.resolve(
    __dirname,
    "..",
    "python",
    "share",
    "jupyter",
    "nbconvert",
    "templates",
    "illusionist",
    "static"
);

module.exports = [
    {
        entry: ["./lib/index.js"],
        output: {
            filename: "illusionist.js",
            path: distRoot,
            libraryTarget: "amd",
        },
        module: { rules: rules },
        devtool: "source-map",
    },
];
