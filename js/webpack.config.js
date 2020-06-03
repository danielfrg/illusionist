var path = require("path");

var rules = [
    { test: /\.css$/, use: ["style-loader", "css-loader"] },
    {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        use: {
            loader: "url-loader",
            options: {
                limit: 10000,
                mimetype: "image/svg+xml",
            },
        },
    },
    // required to load font-awesome
    {
        test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
        use: {
            loader: "url-loader",
            options: {
                limit: 10000,
                mimetype: "application/font-woff",
            },
        },
    },
    {
        test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
        use: {
            loader: "url-loader",
            options: {
                limit: 10000,
                mimetype: "application/font-woff",
            },
        },
    },
    {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        use: {
            loader: "url-loader",
            options: {
                limit: 10000,
                mimetype: "application/octet-stream",
            },
        },
    },
    { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, use: "file-loader" },
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
            // libraryTarget: "amd",
        },
        module: { rules: rules },
        devtool: "source-map",
    },
];
