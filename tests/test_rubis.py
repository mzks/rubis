import os
import signal
import subprocess
from time import sleep
from glob import glob

def test_usage():
    pro = subprocess.run(["rubis", "-h"], preexec_fn=os.setsid)


def test_generate_config():
    pro = subprocess.Popen(["rubis", "-g"], preexec_fn=os.setsid)
    sleep(1)
    assert len(glob('./custom_config.json')) > 0


def test_rubis():
    pro = subprocess.Popen(["rubis", "-r", "-c", "custom_config.json", "-a" ,"1", "-t", "1"], preexec_fn=os.setsid)
    sleep(10)
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

    assert len(glob('./*.json')) > 0
    assert len(glob('./*.csv')) > 0

    import pandas as pd
    df = pd.read_csv(glob('./*.csv')[0])

    assert not df.empty


if __name__ == '__main__':
    test_rubis()
