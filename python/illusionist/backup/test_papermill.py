import asyncio
import queue

import nbformat

# import papermill
# from jupyter_client.manager import start_new_async_kernel, start_new_kernel
from nbclient import NotebookClient
from papermill.clientwrap import PapermillNotebookClient
from papermill.engines import NotebookExecutionManager
from papermill.iorw import load_notebook_node


# def main():
async def main():
    notebook_path = "./notebooks/slider-label.ipynb"
    nb = load_notebook_node(notebook_path)
    nb_man = NotebookExecutionManager(nb, progress_bar=True)

    # nbc = NotebookClient(nb=nb)
    nbc = PapermillNotebookClient(nb_man=nb_man, nest_asyncio=True)

    nbc.execute(reset_kc=False)
    km, kc = nbc.km, nbc.km.client()
    # print(km.has_kernel)
    print(km, kc)

    async def execute(cmd):
        kc.execute(cmd)
        reply = await kc.get_shell_msg(timeout=1)
        print("reply content")
        print(reply["content"])

        output = None
        while True:
            try:
                io = await kc.get_iopub_msg(timeout=1)
                print("io content")
                print(io["content"])
                if (
                    "execution_state" in io["content"]
                    and io["content"]["execution_state"] == "idle"
                ):
                    break
                output = io
            except queue.Empty:
                print("timeout!")
                break
        return output

    print("--")
    print(await execute("print(1)"))
    print("--")
    print(await execute("a = 1"))
    print("--")
    print(await execute("%who_ls"))

    # await kc.stop_channels()
    await km.shutdown_kernel(now=True)


if __name__ == "__main__":
    # main()
    asyncio.run(main())
