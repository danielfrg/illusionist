from nbconvert.exporters.notebook import NotebookExporter

from illusionist.preprocessor import IllusionistPreprocessor


class IllusionistNotebookExporter(NotebookExporter):
    # Name for the menu item under "File -> Download as" in the IDE
    export_from_notebook = "Illusionist Notebook"
    preprocessors = [IllusionistPreprocessor]
