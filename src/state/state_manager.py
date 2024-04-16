from abc import ABC

from src.state.state_widget import StateWidget


class StateManager(ABC):

    def __init__(self, default = None) -> None:
        super().__init__()
        self.observers: list[StateWidget] = []
        self.state = default

    def subscribe(self, observer: StateWidget):
        self.observers.append(observer)

    def read_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self._notify_observers()

    def _notify_observers(self):
        for observer in self.observers:
            observer.render()
