import asyncio
import queue

import nbformat
import papermill
from jupyter_client.manager import start_new_async_kernel, start_new_kernel
from nbclient import NotebookClient
from papermill.engines import NBClientEngine, NotebookExecutionManager
from papermill.iorw import load_notebook_node


# def main():
async def main():
    notebook_path = "./notebooks/slider-label.ipynb"
    nb = load_notebook_node(notebook_path)

    nbc = NotebookClient(nb=nb)
    nbc = NotebookClient(nb=nb, nest_asyncio=True, reset_kc=False)

    nbc.execute(reset_kc=False)
    km, kc = nbc.km, nbc.km.client()
    # print(km.has_kernel)
    print(km, kc)

    # def execute(code):
    #     msg_id = kc.execute(code)
    #     print(msg_id)
    #     reply = nbc.wait_for_reply(msg_id)
    #     print(reply)

    # print(execute("print(1)"))

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
