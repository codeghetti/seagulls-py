"""
Ideally everything from this package can be moved into the main engine some time soon.
"""
from seagulls.cat_demos.engine.v2._executables import IExecutable, executable
from seagulls.cat_demos.engine.v2._session_stages import GameSessionStages
from ._session_state_client import GameSessionState, GameSessionStateClient

__all__ = [
    "IExecutable",
    "executable",
    "GameSessionStages",
    "GameSessionState",
    "GameSessionStateClient",
]
