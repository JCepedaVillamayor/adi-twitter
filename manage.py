from app import create_app
from flask_script import Manager, Shell
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


app = create_app()
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
