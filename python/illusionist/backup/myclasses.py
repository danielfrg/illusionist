import nbformat
from nbclient import NotebookClient
from papermill.engines import NBClientEngine, NotebookExecutionManager
from papermill.iorw import load_notebook_node


if __name__ == "__main__":
    notebook_path = "../../notebooks/slider-label.ipynb"
    nb = load_notebook_node(notebook_path)

    # nb_man = NotebookExecutionManager(nb)
    engine = NBClientEngine()
    out = engine.execute_notebook(nb, kernel_name="python3")
    print(out)
    print(engine.nb)
