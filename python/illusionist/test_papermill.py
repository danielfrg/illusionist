import asyncio
import queue

import nbformat
import papermill
from jupyter_client.manager import start_new_async_kernel, start_new_kernel
from nbclient import NotebookClient
from papermill.engines import NBClientEngine, NotebookExecutionManager
from papermill.iorw import load_notebook_node


async def main():
    notebook_path = "../../notebooks/slider-label.ipynb"

    nb = load_notebook_node(notebook_path)
    # nb_man = NotebookExecutionManager(nb, progress_bar=False)
    nb_man = NotebookExecutionManager(nb, progress_bar=True)

    # km, kc = await start_new_async_kernel()

    pmc = papermill.engines.PapermillNotebookClient(nb_man, nest_asyncio=True)
    # pmc = papermill.engines.PapermillNotebookClient(nb_man, km=km, nest_asyncio=True)
    # nbout = pmc.execute()
    # # pmc.reset_execution_trackers()
    pmc.start_kernel_manager()
    pmc.start_new_kernel_client()

    pmc.papermill_execute_cells()
    print(pmc.km.client().kernel_info())
    # pmc.wait_for_reply()

    km, kc = pmc.km, pmc.km.client()
    print(1)
    # km, kc = await start_new_async_kernel()

    msg_id = kc.execute("print(1)")
    print(msg_id)
    pmc.wait_for_reply(msg_id)

    # async def execute(cmd):
    #     kc.execute(cmd)
    #     reply = await kc.get_shell_msg(timeout=1)
    #     print("reply content")
    #     print(reply['content'])

    #     output = None
    #     while True:
    #         try:
    #             io = await kc.get_iopub_msg(timeout=1)
    #             print("io content")
    #             print(io["content"])
    #             if 'execution_state' in io['content'] and io['content']['execution_state'] == 'idle':
    #                 break
    #             output = io
    #         except queue.Empty:
    #             print("empty queue!")
    #             break
    #     return output

    try:
        pass
        # print((await execute("print(1)"))['content'])
        # print("-")
        # print((await execute("a = 2"))['content'])
        # print("-")
        # print((await execute("%who_ls int"))['content'])
    finally:
        # # await kc.stop_channels()
        await km.shutdown_kernel(now=True)


if __name__ == "__main__":
    asyncio.run(main())
