var path = require("path");

var rules = [
    {
        test: /\.s?[ac]ss$/,
        use: ["style-loader", "css-loader", "sass-loader"],
    },
    {
        test: /\.(js)$/,
        exclude: /node_modules/,
        use: ["babel-loader"],
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
    "static",
    "dist"
);

module.exports = [
    {
        entry: [path.resolve(__dirname, "src", "index.js")],
        output: {
            filename: "illusionist.js",
            path: distRoot,
        },
        module: { rules: rules },
        mode: "development",
        devtool: "source-map",
    },
    {
        entry: [path.resolve(__dirname, "src", "embed.js")],
        output: {
            filename: "illusionist-embed.js",
            path: distRoot,
        },
        module: { rules: rules },
        mode: "development",
        devtool: "source-map",
    },
];
