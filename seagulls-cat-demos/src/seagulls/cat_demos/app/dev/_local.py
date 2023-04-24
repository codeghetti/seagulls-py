import multiprocessing
from multiprocessing import Queue
from uuid import uuid4

from seagulls.cat_demos.app._di_container import CatDemosDiContainer
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId

uid = str(uuid4())

class LocalDevelopment:

    _uuid: str

    def __init__(self) -> None:
        self._uuid = str(uuid4())

    def start(self) -> None:
        ctx = multiprocessing.get_context()
        queue = ctx.Queue()
        for x in range(2):
            print(f"run #{x}")
            p = ctx.Process(target=self._remote_engine, args=(queue,))
            p.start()
            self._local_engine(queue)
            p.join()
            """
            p1 = process 1
            p2 = process 2

            p1 creates a window and listens for frame surfaces to be placed into the queue
            p1 renders each frame
            p1 places pygame input events into the queue
            p2 runs the game session without a window
            p2 renders each frame onto a Surface and sends it into the queue
            p2 consumes input events from the queue grouped by frames
            p1 watches the src and resource directories for changes
            p1 launches a p3 process to replace p2, handing it a new queue
            p1 publishes events to both p2 and p3 queues until the transition is complete
            p1 stops consuming from p2 when the first frame has been received by p3
            p1 stops publishing to p2, terminates p2, and renames p3 to p2
            """

    def _local_engine(self, queue: Queue) -> None:
        container = CatDemosDiContainer(None)
        container._launch_command().execute()
        queue.put(GameObjectId("foo"))

    def _remote_engine(self, queue: Queue) -> None:
        container = CatDemosDiContainer(None)
        container._launch_command().execute()
        queue.put(GameObjectId("foo"))


if __name__ == "__main__":
    local = LocalDevelopment()
    local.start()
