import asyncio
import queue

import nbformat
import papermill
from jupyter_client.manager import start_new_async_kernel, start_new_kernel
from nbclient import NotebookClient
from papermill.engines import NBClientEngine, NotebookExecutionManager
from papermill.iorw import load_notebook_node


async def main():

    print(1)
    km, kc = await start_new_async_kernel()

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

    print((await execute("print(1)"))["content"])
    print("-")
    print((await execute("a = 2"))["content"])
    print("-")
    print((await execute("%who_ls int"))["content"])

    await km.shutdown_kernel(now=True)


if __name__ == "__main__":
    asyncio.run(main())
