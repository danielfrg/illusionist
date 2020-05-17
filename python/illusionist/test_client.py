import asyncio

from illusionist.client import Illusionist
from illusionist import kernel_utils


def get_output(reply):
    content = reply["content"]
    if "data" in content:
        return content["data"]["text/plain"]
    if "name" in content and content["name"] == "stdout":
        return content["text"]


def get_source(func):
    import inspect

    return inspect.getsource(func)


async def main():
    notebook_path = "./notebooks/slider-label.ipynb"
    illusionist = Illusionist.from_nb_file(notebook_path, progress_bar=False)
    client = illusionist
    # client.log_level = "DEBUG"

    client.execute(reset_kc=False)
    client.nb_man.complete_pbar()

    # Get all variables from notebook
    # all_vars = get_output(client.run_cmd("%who_ls"))
    # _ = client.run_cmd(f"all_vars = {all_vars}")

    # Source helper code
    _ = client.run_cmd(get_source(kernel_utils))

    # Iterate widgets
    _ = client.run_cmd("out = get_all_widgets()")
    _ = client.run_cmd("print(out)")
    print(get_output(_))

    _ = client.run_cmd("widget_vars = generate_json()")
    _ = client.run_cmd("print(widget_vars)")
    print(get_output(_))

    # _ = client.run_cmd("slider.value = 2")
    # _ = client.run_cmd("widget_vars = generate_json()")
    # _ = client.run_cmd("print(widget_vars)")
    # print(get_output(_))
    

    # print(client.widget_state)

    # Clean up
    client._cleanup_kernel()


if __name__ == "__main__":
    asyncio.run(main())
