var path = require("path");
const FileManagerPlugin = require("filemanager-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer")
    .BundleAnalyzerPlugin;

const extractPlugin = {
    loader: MiniCssExtractPlugin.loader,
};

const pythonPkgStatic = path.resolve(
    __dirname,
    "..",
    "python",
    "illusionist",
    "templates",
    "illusionist",
    "assets"
);

module.exports = (env, argv) => {
    const IS_PRODUCTION = argv.mode === "production";

    const config_dist = {
        entry: path.resolve(__dirname, "src", "embed.js"),
        output: {
            path: path.resolve(__dirname, "dist"),
            filename: "illusionist-embed.js",
        },
        module: {
            rules: [
                {
                    test: /\.(js)$/,
                    exclude: /node_modules/,
                    use: ["babel-loader"],
                },
                // Extract Jupyter Widgets CSS to external file
                {
                    test: /\.s?[ac]ss$/,
                    use: [extractPlugin, "css-loader"],
                    // use: ["null-loader"],
                },
                // Bundle Jupyter Widgets and Font Awesome in the CSS
                {
                    test: /\.(eot|ttf|woff|woff2|svg|png|gif|jpe?g)$/,
                    loader: require.resolve("url-loader"),
                    // loader: require.resolve("file-loader"),
                    // options: {
                    //     name: "[name].[ext]?[hash]",
                    // outputPath: "assets/",
                    // },
                },
            ],
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: "illusionist-embed.css",
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
            // new BundleAnalyzerPlugin(),
        ],
        mode: IS_PRODUCTION ? "production" : "development",
        devtool: "source-map",
    };

    let config = [config_dist];

    return config;
};
