import queue
from pprint import PrettyPrinter

from jupyter_client.manager import start_new_kernel


class SimpleKernel:
    """
    ## Description
    **SimpleKernel**:
     A simplistic Jupyter kernel client wrapper.
    Additional information in [this GitHub issue]
    (
    )
    """

    def __init__(self):
        """
        ## Description
        Initializes the `kernel_manager` and `client` objects
        and starts the kernel. Also initializes the pretty printer
        for displaying object properties and execution result
        payloads.
        ## Parameters
        None.
        """
        ### Initialize kernel and client
        self.kernel_manager, self.client = start_new_kernel()

        ### Initialize pretty printer
        self.pp = PrettyPrinter(indent=2)

    ### end __init__ ####

    def execute(self, code, verbose=False, get_type=False):
        """
        ## Description
        **execute**:
        Executes a code string in the kernel. Can return either
        the full execution response payload, or just `stdout`. Also,
        there is a verbose mode that displays the execution process.
        ## Parameters
        code : string
            The code string to get passed to `stdin`.
        verbose : bool (default=False)
            Whether to display processing information.
        get_type : bool (default=False) NOT IMPLEMENTED
            When implemented, will return a dict including the output
            and the type. E.g.
            1+1 ==> {stdout: 2, type: int}
            "hello" ==> {stdout: "hello", type: str}
            print("hello") ==> {stdout: "hello", type: NoneType}
            a=10 ==> {stdout: None, type: None}
        ## Returns
        `stdout` or the full response payload.
        """
        debug = lambda x: print(x if verbose else "")

        debug("----------------")
        debug("executing code: " + code)

        ### Execute the code
        msg_id = self.client.execute(code)

        ### Collect the response payload
        reply = self.client.get_shell_msg(msg_id)
        debug("reply content")
        debug(reply["content"])

        ### Get the execution status
        ### When the execution state is "idle" it is complete
        io_msg_content = self.client.get_iopub_msg(timeout=1)["content"]

        ### We're going to catch this here before we start polling
        if (
            "execution_state" in io_msg_content
            and io_msg_content["execution_state"] == "idle"
        ):
            return "no output"

        ### Continue polling for execution to complete
        ### which is indicated by having an execution state of "idle"
        while True:
            ### Save the last message content. This will hold the solution.
            ### The next one has the idle execution state indicating the execution
            ###is complete, but not the stdout output
            temp = io_msg_content

            ### Poll the message
            try:
                io_msg_content = self.client.get_iopub_msg(timeout=1)["content"]
                debug("io_msg content")
                debug(io_msg_content)
                if (
                    "execution_state" in io_msg_content
                    and io_msg_content["execution_state"] == "idle"
                ):
                    break
            except queue.Empty:
                debug("timeout get_iopub_msg")
                break

        debug("temp")
        debug(temp)

        ### Check the message for various possibilities

        if "data" in temp:  # Indicates completed operation
            debug("has data")
            out = temp["data"]["text/plain"]
            if get_type:
                debug("code: " + code)
                the_type = self.execute("type(" + code + ")")
                debug(the_type)
                out = {out: the_type}
        elif "name" in temp and temp["name"] == "stdout":  # indicates output
            debug("name is stdout")
            out = temp["text"]
            if get_type:
                debug("code: " + code)
                if code.startswith("print("):
                    the_type = "string"
                else:
                    the_type = self.execute("type(" + code + ")")
                debug(the_type)
                out = {out: the_type}
                debug("out is " + str(out))
        elif "traceback" in temp:  # Indicates error
            print("ERROR")
            out = "\n".join(temp["traceback"])  # Put error into nice format
        else:
            out = ""

        debug("----------------\n\n")

        debug("returning " + str(out))
        return out

    ### end execute ####

    def showManager(self):
        """
        ## Description
        **showManager**:
        Pretty Print kernel manager object.
        """

        self.pp(self.kernel_manager)

    def showClient(self):
        """
        ## Description
        **showClient**:
        Pretty Print client object.
        """

        self.pp(self.client)

    def prettyPrint(self, payload):
        """
        ## Description
        **prettyPrint**:
        A convenience method to pretty print the reply payload.
        ## example
        ```
        >>> reply = my_kernel.execute("1+1")
        >>> my_kernel.prettyPrint(reply)
        ```
        """

    def __del__(self):
        """
        ## Description
        Destructor. Shuts down kernel safely.
        """
        self.kernel_manager.shutdown_kernel()


### end Simple Kernel ###


def test(verbose=False):

    kernel = SimpleKernel()

    commands = [
        # '1+1',
        # 'a=5',
        "b=0",
        "b",
        # 'print()',
        # 'print("hello there")',
        # '10',
        # 'a*b',
        # 'a',
        # 'a+b',
        # 's = "this is s"',
        # 'print(s)',
        # 'type(s)',
        # 'type(a)',
        # 'type(1.0*a)',
        # 'print(a+b)',
        # 'print(a*10)',
        # 'c=1/b',
        # 'd = {"a":1,"b":"Two","c":[1,2,3]}',
        # 'd',
        # 'import json',
        # 'j = json.loads(str(d).replace(\"\\\'\",\"\\"\"))',
        # 'j',
        # 'import pandas as pd',
        # 'df = pd.DataFrame(dict(A=[1,2,3], B=["one", "two", "three"]))',
        # 'df',
        # 'df.describe()'
    ]

    for command in commands:
        print(">>> " + command)
        out = kernel.execute(command, verbose=True, get_type=False)
        if out:
            print(out)


if __name__ == "__main__":
    test()
