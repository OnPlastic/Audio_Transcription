from __future__ import annotations


def ask_choice(question: str, choices: dict[str, object]) -> object:
    """
    Ask the user to choose from predefined options.
    
    Parameters
    ----------
    question : str
        The question shown to the user.
    choices : dict[str, object]
        Mapping of valid input options to return values.
        
        Example:
        {"j": True, "n": False}
        {"s": "save", "m": "mail"}
    
    Returns
    -------
    object
        The mapped value from the choices dictionary.
    """

    options = "/".join(choices.keys())

    while True:
        answer = input(f"{question} ({options}): ").strip()

        if answer in choices:
            return choices[answer]
        
        print(f"Ungültige Eingabe! Erlaubte Optionen: ({options})")


def ask_email() -> str:
    """
    Ask the user for an email address and validate it.
    
    Returns
    -------
    str
        A valid email address entered by the user.
    """

    while True:
        addr = input("Bitte geben Sie eine gültige E-Mail-Adresse ein: ").strip()

        if "@" in addr and "." in addr:
            print("Mailadresse: ", addr)
            return addr
        
        print("Ungültige E-Mail-Adresse! Bitte versuchen Sie es erneut.")