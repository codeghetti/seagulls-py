import sys


class SeagullsRuntimeClient:
    def is_bundled(self) -> bool:
        frozen = getattr(sys, 'frozen', False)
        has_meipass = hasattr(sys, '_MEIPASS')
        return frozen and has_meipass
