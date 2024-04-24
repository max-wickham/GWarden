from src.state.state_manager import StateManager

login_state_manager = StateManager()

item_state_manager = StateManager()

selected_item_state_manager = StateManager()

login_loading_state = StateManager()
login_loading_state.set_state(False)
