import asyncio
import queue
from time import monotonic

import nbformat
from nbclient.exceptions import (
    CellExecutionComplete,
    CellExecutionError,
    CellTimeoutError,
)
from nbclient import NotebookClient
from nbclient.util import ensure_async, run_sync
from traitlets.config.application import Application


from illusionist.utils import DEV_MODE


WIDGET_ONCHANGE_MIMETYPE = "application/vnd.illusionist.widget-onchange+json"


class IllusionistClient(NotebookClient, Application):
    """
    Extends NBClient
    Adds utilities to run commands in the kernel
    """

    store_widget_state = True

    def set_widgets_onchange_metadata(self, values):
        self.nb.metadata.widgets.update({WIDGET_ONCHANGE_MIMETYPE: values})

    async def async_execute(self, reset_kc=False, **kwargs):
        """
        We copy and overwrite this method from nbclient.Client

        We this that extra code in this part because output widgets are
        not being updated if i run code in the kernel after.
        Not sure why :D
        """
        # print("!!!!!!!!!")
        if reset_kc and self.km:
            await self._async_cleanup_kernel()
        self.reset_execution_trackers()

        async with self.async_setup_kernel(**kwargs):
            self.log.info("Executing notebook with kernel: %s" % self.kernel_name)
            for index, cell in enumerate(self.nb.cells):
                # Ignore `'execution_count' in content` as it's always 1
                # when store_history is False
                # print(cell)
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
        Overwrite this to execute something after the notebook has been executed
        """
        pass

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

    # @staticmethod
    # def get_output(reply):
    #     content = reply["content"]
    #     if "data" in content:
    #         return content["data"]["text/plain"]
    #     if "name" in content and content["name"] == "stdout":
    #         return content["text"]

    # async def async_run_cmd(self, cmd, timeout=3, ret_output=False):
    #     self.log.debug("Running command: %s", cmd)

    #     cell = nbformat.NotebookNode()
    #     cell.source = cmd
    #     cell.cell_type = "code"
    #     cell.metadata = {}

    #     self.nb["cells"].append(cell)
    #     cell_index = len(self.nb["cells"]) - 1
    #     print(self.nb.cells, cell_index)
    #     await self.async_execute_cell(cell, cell_index, store_history=False)

    #     # Delete created cell
    #     # del self.nb["cells"][cell_index]

    #     # self.log.debug("Running command: %s", cmd)
    #     # parent_msg_id = await ensure_async(
    #     #     self.kc.execute(cmd, stop_on_error=not self.allow_errors)
    #     # )

    #     # exec_reply = await self._async_poll_for_cmd_reply(parent_msg_id, timeout)
    #     # if ret_output:
    #     #     return self.get_output(exec_reply)
    #     # return exec_reply

    # run_cmd = run_sync(async_run_cmd)

    # async def _async_poll_for_cmd_reply(self, msg_id, timeout):
    #     if timeout is not None:
    #         deadline = monotonic() + timeout

    #     task_poll_output_msg = asyncio.ensure_future(
    #         self._async_poll_output_cmd_message(msg_id)
    #     )

    #     while True:
    #         try:
    #             msg = await ensure_async(self.kc.shell_channel.get_msg(timeout=timeout))
    #             if msg["parent_header"].get("msg_id") == msg_id:
    #                 try:
    #                     output = await asyncio.wait_for(
    #                         task_poll_output_msg, self.iopub_timeout
    #                     )
    #                     return output
    #                 except (asyncio.TimeoutError, queue.Empty):
    #                     if self.raise_on_iopub_timeout:
    #                         raise CellTimeoutError("Timeout waiting for IOPub output")
    #                     else:
    #                         self.log.warning("Timeout waiting for IOPub output")
    #             else:
    #                 if timeout is not None:
    #                     timeout = max(0, deadline - monotonic())
    #         except queue.Empty:
    #             # received no message, check if kernel is still alive
    #             await self._async_check_alive()

    # async def _async_poll_output_cmd_message(self, parent_msg_id):
    #     output = None
    #     while True:
    #         msg = await ensure_async(self.kc.iopub_channel.get_msg(timeout=None))
    #         if msg["parent_header"].get("msg_id") == parent_msg_id:
    #             try:
    #                 # Will raise CellExecutionComplete when completed
    #                 self._process_cmd_message(msg)
    #                 output = msg
    #             except CellExecutionComplete:
    #                 # print("??????", output)
    #                 return output

    # def _process_cmd_message(self, msg):
    #     msg_type = msg["msg_type"]
    #     self.log.debug("msg_type: %s", msg_type)
    #     content = msg["content"]
    #     self.log.debug("content: %s", content)

    #     if msg_type == "error":
    #         tb = "\n".join(content.get("traceback", []))
    #         raise CellExecutionError(tb, ename="<Error>", evalue="")
    #     if msg_type == "status":
    #         if content["execution_state"] == "idle":
    #             raise CellExecutionComplete()
