from typing import List

def get_command_suggestions(facts: dict, running_config: str, question: str) -> List[str]:
    """
    Mock function to simulate AI suggestions based on device data and user question.
    Later, this will be replaced with real AI model calls.
    """
    # TODO: Real AI integration later
    suggestions = [
        f"configure terminal\ninterface GigabitEthernet0/1\ndescription Connected to Server A",
        f"configure terminal\ninterface GigabitEthernet0/2\nshutdown",
        f"configure terminal\nhostname NewDeviceName"
    ]

    return suggestions
