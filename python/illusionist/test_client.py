import asyncio

from illusionist.client import Illusionist


def get_output(reply):
    content = reply["content"]
    if "data" in content:
        return content["data"]["text/plain"]
    if "name" in content and content["name"] == "stdout":
        return content["text"]


def get_source(func):
    import inspect

    return inspect.getsource(func)


def filter_widgets(var_names):
    import ipywidgets as widgets

    return [item for item in var_names if isinstance(eval(item), widgets.Widget)]


async def main():
    notebook_path = "./notebooks/slider-label.ipynb"
    illusionist = Illusionist.from_nb_file(notebook_path)
    client = illusionist
    # client.log_level = "DEBUG"

    client.execute(reset_kc=False)

    # print("--")
    # print(client.run_cmd("print(1)"))
    # print("--")
    # print(client.run_cmd("a = 1"))
    # print(client.run_cmd("from ipywidgets import Widget"))
    # print("--")
    # print(client.run_cmd("%who_ls Widget"))

    all_vars = get_output(client.run_cmd("%who_ls"))
    _ = client.run_cmd(f"all_vars = {all_vars}")

    _ = client.run_cmd(get_source(filter_widgets))
    _ = client.run_cmd("widget_vars = filter_widgets(all_vars)")
    _ = client.run_cmd("print(widget_vars)")
    print(get_output(_))

    client._cleanup_kernel()


if __name__ == "__main__":
    # main()
    asyncio.run(main())
