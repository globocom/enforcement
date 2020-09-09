import di
from helper.config import Config


config = Config()

if __name__ == "__main__":
    di.watcher.run()
