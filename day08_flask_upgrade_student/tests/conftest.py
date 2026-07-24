# day08_flask_upgrade_student/tests/conftest.py
import sys
from pathlib import Path
import pytest

# 将 day08_flask_upgrade_student/ 目录加入 sys.path，使 app 等模块可被导入
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        c.post("/login", data={"username": "student", "password": "day07"})
        yield c