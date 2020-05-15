import asyncio
import queue

from illusionist.client import IllusionistNotebookClient


async def main():
    notebook_path = "./notebooks/slider-label.ipynb"
    nbc = IllusionistNotebookClient.from_nb_file(notebook_path, progress_bar=False, nest_asyncio=True)

    nbc.execute(reset_kc=False)

    # km, kc = nbc.km, nbc.km.client()
    # async def execute(cmd):
    #     kc.execute(cmd)
    #     reply = await kc.get_shell_msg(timeout=1)
    #     print("reply content")
    #     print(reply["content"])

    #     output = None
    #     while True:
    #         try:
    #             io = await kc.get_iopub_msg(timeout=1)
    #             print("io content")
    #             print(io["content"])
    #             if (
    #                 "execution_state" in io["content"]
    #                 and io["content"]["execution_state"] == "idle"
    #             ):
    #                 break
    #             output = io
    #         except queue.Empty:
    #             print("timeout!")
    #             break
    #     return output
    # print("--")
    # print(await execute("print(1)"))

    print("--")
    print("!!!", nbc.run_cmd("print(1)"))
    print(nbc.run_cmd("print(1)"))
    print("--")
    print(await nbc.async_run_cmd("a = 1"))
    print("--")
    print(await nbc.async_run_cmd("%who_ls"))

    nbc._cleanup_kernel()


if __name__ == "__main__":
    # main()
    asyncio.run(main())
