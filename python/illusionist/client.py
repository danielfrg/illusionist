import nbformat
from nbclient import NotebookClient
from nbclient.util import ensure_async, run_sync
from traitlets.config.application import Application

from illusionist.config import settings


class IllusionistClient(NotebookClient, Application):
    """
    Extends NBClient to add some utilities to run commands in the kernel
    """

    store_widget_state = True

    async def async_execute(self, reset_kc=False, **kwargs):
        """
        We overwrite and copy the original code for this function from
        nbclient.NotebookClient and change a couple of things

        We need to do this because output widgets are
        not being updated if I run code in a function after even
        after keeping the kernel alive (not sure why).
        """
        if reset_kc and self.km:
            await self._async_cleanup_kernel()
        self.reset_execution_trackers()

        async with self.async_setup_kernel(**kwargs):
            self.log.info(
                "Executing notebook with kernel: %s" % self.kernel_name
            )
            for index, cell in enumerate(self.nb.cells):
                # Ignore `'execution_count' in content` as it's always 1
                # when store_history is False
                await self.async_execute_cell(
                    cell, index, execution_count=self.code_cells_executed + 1
                )

            # ADDED
            await ensure_async(self.after_notebook())
            # NED

            msg_id = await ensure_async(self.kc.kernel_info())
            info_msg = await self.async_wait_for_reply(msg_id)
            self.nb.metadata["language_info"] = info_msg["content"][
                "language_info"
            ]
            self.set_widgets_metadata()

        return self.nb

    execute = run_sync(async_execute)

    def after_notebook(self):
        """
        This is called after the regular notebook cells have been executed
        """

    async def async_exec_code(self, source, write_cell=settings.dev_mode):
        """
        Execute code in a Kernel

        Parameters
        ----------
            source (str): Execute this code
            write_cell (bool, default=None): Write a new cell to the notebook

        Returns
        -------
            NotebookNode
        """
        cell = nbformat.NotebookNode()
        cell.cell_type = "code"
        cell.execution_count = self.code_cells_executed + 1
        cell.metadata = {}
        cell.outputs = []
        cell.source = source

        self.nb["cells"].append(cell)
        cell_index = len(self.nb["cells"]) - 1
        cell = await self.async_execute_cell(
            cell, cell_index, execution_count=cell.execution_count
        )

        if write_cell == False:
            # Delete created cell
            del self.nb["cells"][cell_index]

        return cell

    exec_code = run_sync(async_exec_code)

    def eval_cell(self, cell):
        """
        Run Python `eval` on a NotebookCell

        Parameters
        ----------
            cell (NotebookNode):

        Returns
        -------
            Python objects
        """
        output_txt = cell["outputs"][0]["data"]["text/plain"]
        return eval(output_txt)
