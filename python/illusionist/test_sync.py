import asyncio
import queue

import nbformat
import papermill
from jupyter_client.manager import start_new_async_kernel, start_new_kernel
from nbclient import NotebookClient
from papermill.engines import NBClientEngine, NotebookExecutionManager
from papermill.iorw import load_notebook_node


km, client = start_new_kernel()


def execute(code):
    msg_id = client.execute(code)
    io_msg_content = client.get_iopub_msg(timeout=1)["content"]

    ### We're going to catch this here before we start polling
    if (
        "execution_state" in io_msg_content
        and io_msg_content["execution_state"] == "idle"
    ):
        raise "no output"

    while True:
        ### Save the last message content. This will hold the solution.
        ### The next one has the idle execution state indicating the execution
        ###is complete, but not the stdout output
        temp = io_msg_content

        ### Poll the message
        try:
            io_msg_content = client.get_iopub_msg(timeout=1)["content"]
            print("io_msg content")
            print(io_msg_content)
            if (
                "execution_state" in io_msg_content
                and io_msg_content["execution_state"] == "idle"
            ):
                break
        except queue.Empty:
            print("timeout get_iopub_msg")
            break

    print("temp")
    print(temp)


execute("print(1)")
execute("a = 2")
execute("%who_ls int")
