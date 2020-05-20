This is a fork of the `@jupyter-widgets` packages that we change

The structure is similar to make it easy to use other modules if needed.

# illusionist-html-manager

Fork of `@jupyter-widgets/html-manager`.

Changes:

- Creates `htmlmanager.IllusionistHTMLManager` that extends `@jupyter-widgets/html-manager/HTMLManager`
- Other files just change the reference class to use the new `IllusionistHTMLManager`
- `package.json` adds `@jupyter-widgets/html-manager` as dependency
