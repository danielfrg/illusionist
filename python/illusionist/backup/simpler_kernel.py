from jupyter_client.manager import start_new_kernel


km, client = start_new_kernel()

msg_id = client.execute("print(1)")
# msg_id = client.execute("pr")

### Collect the response payload
reply = client.get_shell_msg(msg_id)
print(reply)
