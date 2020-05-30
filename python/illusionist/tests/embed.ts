export function renderWidgets(
    element = document.documentElement,
    loader: (
      moduleName: string,
      moduleVersion: string
    ) => Promise<any> = requireLoader
  ): void {
    requirePromise(['@jupyter-widgets/html-manager']).then(htmlmanager => {
      const managerFactory = (): any => {
        return new htmlmanager.IllusionistHTMLManager({ loader: loader });
      };
      libembed.renderWidgets(managerFactory, element);
    });
}
