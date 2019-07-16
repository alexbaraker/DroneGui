import sshtunnel


class SSHTunnel():

    def __init__(self, ip, port):
        sshtunnel.SSH_TIMEOUT = 1.0
        self.tunnel_server = None
        
        try:
            self.tunnel_server = sshtunnel.SSHTunnelForwarder(
                (ip, 22),
                ssh_username='snickerdoodle',
                ssh_password='snickerdoodle',
                remote_bind_address=('127.0.0.1', port),
                local_bind_address=('127.0.0.1', port),
            )
        except Exception as e:
            print('Error creating SSH Tunnel', e)
            raise e

        try: 
            self.tunnel_server.start()
            print('Tunneled to server at tcp://%s:%s' % ( str(ip), str(port) ))
        except sshtunnel.BaseSSHTunnelForwarderError:
            print('Setting up SSH tunnel failed. Are you on same ip as target or is target running?')
            raise


    def __del__(self):
        if self.tunnel_server:
            self.tunnel_server.stop()
