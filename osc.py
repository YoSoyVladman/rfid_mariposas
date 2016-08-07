import OSC

c = OSC.OSCClient()
c.connect(('172.1.1.211', 1221))   # localhost, port 57120
oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/login")
oscmsg.append('HELLO')
c.send(oscmsg)
