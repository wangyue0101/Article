import unittest
from flask_app import create_app


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

        self.client = self.app.test_client()


    def tearDown(self):
        self.app_ctx.pop()

    def test_user_login(self):
        rep = self.client.post("/api/v1/user/login", data={"username": "liyang", "password": "ly147258"})
        print(rep.data.decode())
        self.assertEqual(rep.status_code, 200)


unittest.main()
