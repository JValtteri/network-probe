import os
import time

class Probe():

    def __init__(self):

        self.id = 0
        self.name = "probe"
        self.ip_list = ['1.1.1.1', '1.0.0.1']
        self.count = 1

    def run_probes(self):
        for ip in self.ip_list:
            result = self.ping(ip)
            print(result)

    def ping(self, ip):
        """
        sends a PING to IP and returns
            "target": IP,
            "up": 1 or 0,
            "timestamp": POSIX (ms)
        """

        posix = time.time() * 1000
        response = os.popen(f"ping -n {self.count} {ip}").read()
        # print(response)
        if (f"Received = {self.count}") in response:
            up = 1
        else:
            up = 0

        result = {
            "target": ip,
            "up": up,
            "timestamp": posix
        }
        return result


if __name__ == "__main__":
    probe = Probe()
    probe.run_probes()
