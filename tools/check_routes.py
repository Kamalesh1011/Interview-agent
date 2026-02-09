import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

with app.test_client() as c:
    r = c.get('/admin-students')
    print('/admin-students', r.status_code)
    print(r.get_data(as_text=True)[:200])

    r2 = c.get('/admin-students.html')
    print('/admin-students.html', r2.status_code)
    print(r2.get_data(as_text=True)[:200])
