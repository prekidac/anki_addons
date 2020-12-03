from aqt.overview import Overview


def unbury_block(func):
    def wrapper(*args, **kwargs):
        pass
    return wrapper


Overview.onUnbury = unbury_block(Overview.onUnbury)
