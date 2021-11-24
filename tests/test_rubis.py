import os
import signal
import subprocess
from time import sleep
from glob import glob

def test_usage():
    pro = subprocess.run(["rubis", "-h"], preexec_fn=os.setsid)


def test_rubis():
    pro = subprocess.Popen(["rubis", "-r"], preexec_fn=os.setsid)
    sleep(10)
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

    assert len(glob('./*.json')) > 0
    assert len(glob('./*.csv')) > 0

if __name__ == '__main__':
    test_rubis()
