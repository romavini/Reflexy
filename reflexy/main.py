import sys


def start():
    from reflexy.runner import Runner

    runner = Runner(autonomous=False, show_vision=False, allow_restart=True)
    runner.run()


if __name__ == "__main__":

    start()
    sys.exit()
