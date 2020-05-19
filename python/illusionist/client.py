import asyncio
import queue
from time import monotonic

from nbclient.exceptions import (
    CellExecutionComplete,
    CellExecutionError,
    CellTimeoutError,
)
from nbclient import NotebookClient
from nbclient.util import ensure_async, run_sync
from traitlets.config.application import Application


class IllusionistClient(NotebookClient, Application):
    """
    Extends NBClient
    Adds utilities to run commands in the kernel
    """

    store_widget_state = True

    def set_widgets_onchange_metadata(self, values):
        mime_type = "application/vnd.illusionist.widget-onchange+json"
        self.nb.metadata.widgets.update({mime_type: values})

    @staticmethod
    def get_output(reply):
        content = reply["content"]
        if "data" in content:
            return content["data"]["text/plain"]
        if "name" in content and content["name"] == "stdout":
            return content["text"]

    async def async_run_cmd(self, cmd, timeout=3, ret_output=False):
        self.log.debug("Running command: %s", cmd)
        parent_msg_id = await ensure_async(
            self.kc.execute(cmd, stop_on_error=not self.allow_errors)
        )

        exec_reply = await self._async_poll_for_cmd_reply(parent_msg_id, timeout)
        if ret_output:
            return self.get_output(exec_reply)
        return exec_reply

    run_cmd = run_sync(async_run_cmd)

    async def _async_poll_for_cmd_reply(self, msg_id, timeout):
        if timeout is not None:
            deadline = monotonic() + timeout

        task_poll_output_msg = asyncio.ensure_future(
            self._async_poll_output_cmd_message(msg_id)
        )

        while True:
            try:
                msg = await ensure_async(self.kc.shell_channel.get_msg(timeout=timeout))
                if msg["parent_header"].get("msg_id") == msg_id:
                    try:
                        output = await asyncio.wait_for(
                            task_poll_output_msg, self.iopub_timeout
                        )
                        return output
                    except (asyncio.TimeoutError, queue.Empty):
                        if self.raise_on_iopub_timeout:
                            raise CellTimeoutError("Timeout waiting for IOPub output")
                        else:
                            self.log.warning("Timeout waiting for IOPub output")
                else:
                    if timeout is not None:
                        timeout = max(0, deadline - monotonic())
            except queue.Empty:
                # received no message, check if kernel is still alive
                await self._async_check_alive()

    async def _async_poll_output_cmd_message(self, parent_msg_id):
        output = None
        while True:
            msg = await ensure_async(self.kc.iopub_channel.get_msg(timeout=None))
            if msg["parent_header"].get("msg_id") == parent_msg_id:
                try:
                    # Will raise CellExecutionComplete when completed
                    self._process_cmd_message(msg)
                    output = msg
                except CellExecutionComplete:
                    # print("??????", output)
                    return output

    def _process_cmd_message(self, msg):
        msg_type = msg["msg_type"]
        self.log.debug("msg_type: %s", msg_type)
        content = msg["content"]
        self.log.debug("content: %s", content)

        if msg_type == "error":
            tb = "\n".join(content.get("traceback", []))
            raise CellExecutionError(tb, ename="<Error>", evalue="")
        if msg_type == "status":
            if content["execution_state"] == "idle":
                raise CellExecutionComplete()
