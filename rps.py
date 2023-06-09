import random
# Inspired by https://www.reddit.com/r/coolguides/comments/cauhw3/ultimate_rock_paper_scissors/
options = ["rock",
           "fire",
           "scissors",
           "snake",
           "human",
           "tree",
           "wolf",
           "sponge",
           "paper",
           "air",
           "water",
           "dragon",
           "devil",
           "lightning",
           "gun"]

option_icons = ["🪨",
                "🔥",
                "✂",
                "🐍",
                "🙂",
                "🌳",
                "🐺",
                "🧽",
                "📰",
                "🌀",
                "💧",
                "🐉",
                "😈",
                "⚡",
                "🔫"]

def rps(a: str, b: str) -> str|None:
    """
    Function takes two string inputs a and b.
    Return the winning string, or None if neither won.
    """
    a = a.lower()
    b = b.lower()
    if a not in options:
        raise ValueError(f"\"{a}\" is not a valid choice.")
    elif b not in options:
        raise ValueError(f"\"{b}\" is not a valid choice.")
    elif a == b:
        return None
    else:
        N = len(options)
        threshold = N // 2
        a_idx = options.index(a)
        b_idx = options.index(b)
        b_idx_shifted = (b_idx - a_idx) % N
        return a if b_idx_shifted <= threshold else b

def random_option() -> str:
    """
    Return a random choice out of the valid move options.
    """
    return random.choice(options)

def get_option_icon(option: str) -> str:
    """
    Return the icon for the corresponding move option.
    """
    if option not in options:
        raise ValueError(f"\"{option}\" is not a valid choice.")
    idx = options.index(option)
    return option_icons[idx]

def comparison_string(a: str, b: str) -> str:
    """
    Function takes two string inputs a and b.
    Return a string comparing their icons.
    - a < b
    - a = b
    - a > b
    """
    winner = rps(a, b)
    a_icon = get_option_icon(a)
    b_icon = get_option_icon(b)
    if winner is None:
        sign = "="
    elif winner == a:
        sign = ">"
    else:
        sign = "<"
    return f"{a_icon} {sign} {b_icon}"

def get_winner(name_a: str, a: str, name_b: str, b: str) -> str|None:
    """
    Function takes four string inputs: two names and two move options.
    Return the name of the winner, if there is one.
    Otherwise, return None
    """
    winner = rps(a, b)
    if winner is None:
        return None
    elif winner == a:
        return name_a
    else:
        return name_b
