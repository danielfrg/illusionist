var path = require("path");
const FileManagerPlugin = require("filemanager-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleAnalyzerPlugin =
    require("webpack-bundle-analyzer").BundleAnalyzerPlugin;

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

    // Build the UMD library
    const config_lib = {
        entry: path.resolve(__dirname, "src", "index.js"),
        output: {
            path: path.resolve(__dirname, "lib"),
            filename: "index.js",
            library: {
                name: "illusionist",
                type: "umd",
            },
        },
        module: {
            rules: [
                {
                    test: /\.(js)$/,
                    exclude: /node_modules/,
                    use: ["babel-loader"],
                },
                {
                    test: /\.s?[ac]ss$/,
                    use: ["null-loader"],
                },
                {
                    test: /\.(eot|ttf|woff|woff2|svg|png|gif|jpe?g)$/,
                    use: ["null-loader"],
                },
            ],
        },
        mode: IS_PRODUCTION ? "production" : "development",
        optimization: {
            minimize: false,
        },
        externals: [/^@jupyter-widgets\/.+$/, "papaparse"],
    };

    // Build the embed JS and CSS
    const config_bundle = {
        entry: path.resolve(__dirname, "src", "embed.js"),
        output: {
            path: path.resolve(__dirname, "dist"),
            filename: "illusionist-embed.js",
            publicPath: "",
        },
        module: {
            rules: [
                {
                    test: /\.(js)$/,
                    exclude: /node_modules/,
                    use: ["babel-loader"],
                },
                // Extract Jupyter Widgets CSS to an external file
                {
                    test: /\.s?[ac]ss$/,
                    use: [extractPlugin, "css-loader"],
                },
                // Bundle Jupyter Widgets and Font Awesome in the CSS
                {
                    test: /\.(eot|ttf|woff|woff2|svg|png|gif|jpe?g)$/,
                    use: ["url-loader"],
                },
            ],
        },
        plugins: [
            // Extract the CSS
            new MiniCssExtractPlugin({
                filename: "illusionist-embed.css",
            }),
            // Copy the bundles to the Python package
            new FileManagerPlugin({
                events: {
                    onEnd: {
                        copy: [
                            {
                                source: "./dist/*.*",
                                destination: pythonPkgStatic,
                            },
                        ],
                    },
                },
            }),
            // new BundleAnalyzerPlugin(),
        ],
        mode: IS_PRODUCTION ? "production" : "development",
        devtool: "source-map",
    };

    let config = [];
    if (IS_PRODUCTION) {
        config.push(config_bundle);
        config.push(config_lib);
    } else {
        config.push(config_bundle);
    }

    return config;
};
