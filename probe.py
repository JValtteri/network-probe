import os
import time

class Probe():

    def __init__(self):

        self.id = 0
        self.name = "probe"
        self.ip_list = ['1.1.1.1', '1.0.0.1']
        self.count = 1
        self.time_interval = 2

    def run_probes(self):
        for ip in self.ip_list:
            result = self.ping(ip)
            print(result)
        time.sleep(self.time_interval)

    def ping(self, ip):
        """
        returns:
        {"target": IP, "up": 1 or 0, "timestamp": POSIX(ms)}
        """

        posix = time.time() * 1000
        response = os.popen(f"ping -n {self.count} {ip}").read()
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

    def detect_network(self):
        "Trace the first nodes of the network"
        trace_ips = []
        response = os.popen(f"pathping -q 1 1.1.1.1").readlines()
        for line in response:
            if len(line) > 3 and line[2] in ["1", "2", "3"]:
                trace_ip = line.rsplit("[")[1][0:-3]
                print(trace_ip)


if __name__ == "__main__":
    probe = Probe()
    for i in range(3):
        probe.run_probes()
    # probe.detect_network()
