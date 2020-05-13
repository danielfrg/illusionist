import asyncio

import nbformat
from IPython.utils.capture import capture_output
from nbclient import NotebookClient


async def main():
    nb_fname = "../../notebooks/slider-label.ipynb"

    with open(nb_fname) as f:
        nb = nbformat.read(f, as_version=4)

    client = NotebookClient(nb)
    _ = client.execute()

    kc = client.km.client()

    with capture_output() as io:
        reply = kc.execute_interactive("print('hello')")

    print(io.stdout)


if __name__ == "__main__":
    asyncio.run(main())
