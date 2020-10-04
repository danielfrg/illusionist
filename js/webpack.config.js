var path = require("path");
const FileManagerPlugin = require("filemanager-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

var pythonPkgStatic = path.resolve(
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
        entry: [path.resolve(__dirname, "src", "embed.js")],
        output: {
            path: path.resolve(__dirname, "dist"),
            filename: "illusionist-embed.js",
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: "illusionist.css",
            }),
            // Copy the output to the Python Package
            new FileManagerPlugin({
                onEnd: {
                    copy: [
                        {
                            source: "./dist/*.*",
                            destination: pythonPkgStatic,
                        },
                    ],
                },
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.(js)$/,
                    include: path.resolve(__dirname, "src"),
                    // exclude: /node_modules/,
                    use: ["babel-loader"],
                },
                // Jupyter Widgets CSS
                {
                    test: /\.css$/i,
                    use: [MiniCssExtractPlugin.loader, "css-loader"],
                    // use: ["null-loader"],
                },
                // Jupyter Widget Icons
                { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, use: ["url-loader"] },
                // Required to load font-awesome
                { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
                { test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
                { test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
                { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
            ],
        },
        mode: "development",
        devtool: "source-map",
    },
    // {
    //     entry: [path.resolve(__dirname, "src", "index.js")],
    //     output: {
    //         path: path.resolve(__dirname, "lib"),
    //         filename: "index.js",
    //         libraryTarget: "commonjs2",
    //     },
    //     module: {
    //         rules: [
    //             {
    //                 test: /\.(js)$/,
    //                 include: path.resolve(__dirname, "src"),
    //                 // exclude: /node_modules/,
    //                 use: ["babel-loader"],
    //             },
    //             // Jupyter Widgets CSS
    //             { test: /\.css$/i, use: ["url-loader"] },
    //             // Jupyter Widget Icons
    //             { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, use: ["url-loader"] },
    //             // Required to load font-awesome
    //             { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
    //             { test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
    //             { test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
    //             { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, use: ["file-loader"] },
    //         ],
    //     },
    //     optimization: {
    //         minimize: false,
    //     },
    //     mode: "development",
    //     devtool: "source-map",
    // },
];
