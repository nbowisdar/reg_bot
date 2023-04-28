def divide_big_msg(msg: str) -> list[str]:
    if len(msg) < 4000:
        return [msg]

    return msg.split("\n\n")

