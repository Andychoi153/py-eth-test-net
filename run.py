from worker import Worker
import os

if __name__=='__main__':

    tmp_dir = os.path.dirname(__file__)
    _worker = Worker(tmp_dir)
    _worker.run()
