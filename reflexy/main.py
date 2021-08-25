import sys


def start():
    """Run the game."""
    from reflexy.runner import Runner

    runner = Runner(autonomous=False, training=True, show_vision=True, allow_restart=True)
    runner.run()


if __name__ == "__main__":

    start()
    sys.exit()
