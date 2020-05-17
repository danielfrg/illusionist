import asyncio
import json

from illusionist import kernel_utils
from illusionist.client import Illusionist


def get_source(code):
    import inspect

    return inspect.getsource(code)


async def main():
    notebook_path = "./notebooks/slider-label.ipynb"
    illusionist = Illusionist.from_nb_file(notebook_path, progress_bar=False)
    client = illusionist
    # client.log_level = "DEBUG"

    client.execute(reset_kc=False)
    client.nb_man.complete_pbar()

    # Source helper code
    _ = client.run_cmd(get_source(kernel_utils))

    # Iterate widgets
    # _ = client.run_cmd("out = get_all_widgets()")
    # _ = client.run_cmd("print(out)")
    # print(get_output(_))

    _ = client.run_cmd("widget_vars = generate_json()")
    output_json = client.run_cmd("print(widget_vars)", ret_output=True)
    print(output_json)
    output_json = json.loads(output_json)

    with open("notebooks/serialized.json", "w") as f:
        json.dump(output_json, f, indent=2)
    # serialized = json.dump(_, )

    # print(client.widget_state)

    # Clean up
    client._cleanup_kernel()


if __name__ == "__main__":
    asyncio.run(main())
