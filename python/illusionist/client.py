import asyncio
import queue
from async_generator import asynccontextmanager


import nbformat
# import papermill
# from jupyter_client.manager import start_new_async_kernel, start_new_kernel
from nbclient import NotebookClient
from papermill.iorw import load_notebook_node
from papermill.clientwrap import PapermillNotebookClient
from papermill.engines import NotebookExecutionManager
from nbclient.util import run_sync, ensure_async

from nbclient.exceptions import (CellControlSignal,
    CellTimeoutError,
    DeadKernelError,
    CellExecutionComplete,
    CellExecutionError
    )


class IllusionistNotebookClient(PapermillNotebookClient):

    @classmethod
    def from_nb_file(cls, fpath, progress_bar=True, **kwargs):
        nb = load_notebook_node(fpath)
        nb_man = NotebookExecutionManager(nb, progress_bar=progress_bar)
        
        return cls(nb_man=nb_man, **kwargs)
    
    # @asynccontextmanager
    # async def async_setup_kernel(self, **kwargs):
    #     """
    #     Overwriting this until nbclient release with PR:
    #     """
    #     reset_kc = kwargs.pop('reset_kc', False)
    #     if self.km is None:
    #         self.start_kernel_manager()

    #     if not self.km.has_kernel:
    #         await self.async_start_new_kernel_client(**kwargs)
    #     try:
    #         yield
    #     finally:
    #         if reset_kc:
    #             await self._async_cleanup_kernel()

    async def async_run_cmd(self, cmd, timeout=3):
        parent_msg_id = await ensure_async(self.kc.execute(cmd, stop_on_error=not self.allow_errors))

        exec_reply = await self._async_poll_for_reply_cmd(
            parent_msg_id, timeout)

        return exec_reply


    run_cmd = run_sync(async_run_cmd)


    async def _async_poll_for_reply_cmd(self, msg_id, timeout):
        task_poll_output_msg = asyncio.ensure_future(
            self._async_poll_output_msg_cmd(msg_id)
        )

        while True:
            try:
                msg = await ensure_async(self.kc.shell_channel.get_msg(timeout=timeout))
                if msg['parent_header'].get('msg_id') == msg_id:
                    try:
                        output = await asyncio.wait_for(task_poll_output_msg, self.iopub_timeout)
                        return output
                    except (asyncio.TimeoutError, queue.Empty):
                        if self.raise_on_iopub_timeout:
                            raise CellTimeoutError.error_from_timeout_and_cell(
                                "Timeout waiting for IOPub output", self.iopub_timeout, cell
                            )
                        else:
                            self.log.warning("Timeout waiting for IOPub output")
                else:
                    if timeout is not None:
                        timeout = max(0, deadline - monotonic())
            except queue.Empty:
                # received no message, check if kernel is still alive
                await self._async_check_alive()
        

    async def _async_poll_output_msg_cmd(self, parent_msg_id):
        output = None
        while True:
            msg = await ensure_async(self.kc.iopub_channel.get_msg(timeout=None))
            if msg['parent_header'].get('msg_id') == parent_msg_id:
                try:
                    # Will raise CellExecutionComplete when completed
                    # print("io", msg)
                    self._process_cmd_message(msg)
                    output = msg
                except CellExecutionComplete:
                    # print("??????", output)
                    return output

    def _process_cmd_message(self, msg):
        msg_type = msg['msg_type']
        self.log.debug("msg_type: %s", msg_type)
        content = msg['content']
        self.log.debug("content: %s", content)

        if msg_type == 'status':
            if content['execution_state'] == 'idle':
                raise CellExecutionComplete()





