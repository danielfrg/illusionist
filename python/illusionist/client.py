import nbformat
from nbclient import NotebookClient
from nbclient.util import ensure_async, run_sync
from traitlets.config.application import Application

from illusionist.utils import DEV_MODE


class IllusionistClient(NotebookClient, Application):
    """
    Extends NBClient
    Adds utilities to run commands in the kernel
    """

    store_widget_state = True

    async def async_execute(self, reset_kc=False, **kwargs):
        """
        We copy and add a coupel of lines this method from nbclient.Client

        We need that extra code here because output widgets are
        not being updated if I run code in a function after even
        after keeping the kernel alive. Not sure why.
        """
        if reset_kc and self.km:
            await self._async_cleanup_kernel()
        self.reset_execution_trackers()

        async with self.async_setup_kernel(**kwargs):
            self.log.info("Executing notebook with kernel: %s" % self.kernel_name)
            for index, cell in enumerate(self.nb.cells):
                # Ignore `'execution_count' in content` as it's always 1
                # when store_history is False
                await self.async_execute_cell(
                    cell, index, execution_count=self.code_cells_executed + 1
                )

            # added
            await ensure_async(self.post_exec())
            # end add

            msg_id = await ensure_async(self.kc.kernel_info())
            info_msg = await self.async_wait_for_reply(msg_id)
            self.nb.metadata["language_info"] = info_msg["content"]["language_info"]
            self.set_widgets_metadata()

        return self.nb

    execute = run_sync(async_execute)

    def post_exec(self):
        """
        Overwrite this to execute extra code after the notebook has been executed
        """

    async def async_run_code(self, source, write_cell=None):
        write_cell = write_cell if write_cell is not None else DEV_MODE
        cell = nbformat.NotebookNode()
        cell.cell_type = "code"
        cell.execution_count = self.code_cells_executed + 1
        cell.metadata = {}
        cell.outputs = []
        cell.source = source

        self.nb["cells"].append(cell)
        cell_index = len(self.nb["cells"]) - 1
        # print(cell)
        cell = await self.async_execute_cell(
            cell, cell_index, execution_count=cell.execution_count
        )

        if write_cell == False:
            # Delete created cell
            del self.nb["cells"][cell_index]

        return cell

    run_code = run_sync(async_run_code)

    def run_code_eval(self, source):
        output = self.run_code(source)
        text_plain = output["outputs"][0]["data"]["text/plain"]
        return eval(text_plain)
