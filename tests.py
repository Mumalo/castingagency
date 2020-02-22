import unittest
from app import app
from models import Movies, Actors
from faker import Faker
import json
from datetime import datetime
import tempfile

CASTING_ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCI" \
                          "sImtpZCI6Ik1rVTBNa1JETjBVM" \
                          "1JrSkRRakkzUVRZeE9VTkdORFU1T0RC" \
                          "Q1JVWTFPREl6UWtZMlJqazFRdy" \
                          "J9.eyJpc3MiOiJodHRwczovL2Rldi1o" \
                          "M3ZoNXZuNC5ldS5hdXRoMC5jb" \
                          "20vIiwic3ViIjoiYXV0aDB8NWU0ZWIz" \
                          "ZWUxMjc4MTgwY2U0YTEwNDU2IiwiYXVkIj" \
                          "oiaHR0cDovL2xvY2Fsc2hvc3Q6NTAwMCIs" \
                          "ImlhdCI6MTU4MjI4MjU4NywiZXhwIjo" \
                          "xNTgyMjg5Nzg3LCJhenAiOiJxbXVrbTV" \
                          "3RmRBMXZpcWVZMGxUcXJ2cklUR" \
                          "HhoU3hybyIsInNjb3BlIjoiIiwicGVy" \
                          "bWlzc2lvbnMiOlsiZ2V0OmFjdG9yLWRld" \
                          "GFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0O" \
                          "m1vdmllcyJdfQ.a-LwA03EuMEc_1t0" \
                          "p_ops2UmUYPyOxbdTtfZa6qdB53wdyQRR" \
                          "eu3JEnZOdAOhj7NCRGTA168bbrx3jBLdCE" \
                          "0x75AQWbsRaUziLhacRIIzdej79IrBVBI-" \
                          "YEkguuaDUgA4oZkx57z7HWoMyIf" \
                          "Vt0S7z-1bnyBv6UFW5Wv_Rxap2xLPvX4T" \
                          "Q8fB9UJGlWfz7LDmj8-Vzn4L2-bt9zJjWB-" \
                          "m3dRTyIxc-ojxNPHJI91Ydver_D8SEu2m2W" \
                          "Mr5M3VrZbMd2hhhefyHFtqc6jOv" \
                          "pDVFDqy-l3ntfvX6qag3YcxcjJcUWpgYuY" \
                          "Ux-ZrDHZg3GWa-NfvoCW1Qpwa3tX2-_srg"

EXECUTIVE_PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIs" \
                           "ImtpZCI6Ik1rVTBNa1JETjBVM1JrSkRRa" \
                           "kkzUVRZeE9VTkdORFU1T0RCQ1JVWTFPREl6UW" \
                           "tZMlJqazFRdyJ9.eyJpc3MiOiJodHRwczovL2R" \
                           "ldi1oM3ZoNXZuNC5ldS5hdXRoMC5jb20vIiwic" \
                           "3ViIjoiYXV0aDB8NWU0ZWIwNTQ4MDBmMzcw" \
                           "Y2RhNmJjZjUxIiwiYXVkIjoiaHR0cDovL2x" \
                           "vY2Fsc2hvc3Q6NTAwMCIsImlhdCI6MTU4Mj" \
                           "MxNjYxNSwiZXhwIjoxNTgyMzIzODE1LCJhen" \
                           "AiOiJxbXVrbTV3RmRBMXZpcWVZMGxUcX" \
                           "J2cklURHhoU3hybyIsInNjb3BlIjoiIiwicG" \
                           "VybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG" \
                           "9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6Y" \
                           "WN0b3ItZGV0YWlscyIsImdldDphY3RvcnM" \
                           "iLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3" \
                           "JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY" \
                           "3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.q_rjq" \
                           "KNcRH8b39OiryjpiHYqS-lpGjvX0KZWu_3Ww" \
                           "gTEr6fSSiOV4VtU6UjrlAG9aZus5FBuourBk" \
                           "3uG-SnJVYdgZ1w_MRcTYLwRv2a4pcW7LoTQh" \
                           "2m7ONsOq6Kl5eSY9cyotDJzVDcfe_6opFmxNY" \
                           "Z_gF33SOGmmurxjFro5aedl-0yYC0098qPae" \
                           "7spSMdcLA5i62tJkkVOmoWrPdhEAnaCXvdEIyI" \
                           "KoVGPh39YfSuDbrYvrryh6tZHt7uis3IjQ" \
                           "PNXdzDmiJKdOZpSISA-ZmvPsBXu4Iee6RQ6H5" \
                           "tjkVxeM60tXOZspvHH3o1KGJhq-ti9SO6VgjNxhTVtyLAUQ"

EXPIRED_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6" \
                "IkpXVCIsImt" \
                "pZCI6Ik1rVTBNa1JETjBVM1JrSkRR" \
                "akkzUVRZeE9VTkdO" \
                "RFU1T0RCQ1JVWTFPREl6UWtZMlJqaz" \
                "FRdyJ9.eyJpc3MiOiJodHRwczovL2Rld" \
                "i1oM3ZoNXZuNC5ldS5hd" \
                "XRoMC5jb20vIiwic3ViIjoiYXV0aDB" \
                "8NWU0ZWIwNTQ4MDBmMzcwY2RhNmJjZjU" \
                "xIiwiYXVkIjoiaHR0cDo" \
                "vL2xvY2Fsc2hvc3Q6NTAwMCIsIml" \
                "hdCI6MTU4MjI4MjcwOCwiZXhwIjo" \
                "xNTgyMjg5OTA4LCJhenAiOiJxbX" \
                "VrbTV3RmRBMXZpcWVZMGxUcXJ2ck" \
                "lURHhoU3hybyIsInNjb3BlIjoiI" \
                "iwicGVybWlzc2lvbnMiOlsiZG" \
                "VsZXRlOmFjdG9ycyIsImRlbGV0Z" \
                "Tptb3ZpZXMiLCJnZXQ6YWN0b3I" \
                "tZGV0YWlscyIsImdldDphY3RvcnMi" \
                "LCJnZXQ6bW92aWVzIiwicGF0Y2g6" \
                "bW92aWVzIiwicG9zdDphY3RvcnMi" \
                "LCJwb3N0Om1vdmllcyJdfQ.l2SuzbQ" \
                "uvczXio5lLK9ty6U7Du9oji2DeSQ" \
                "pbmiPD5wskJLT8mbPQRXKg_x-dtyu" \
                "8ParR3DYZEJ7nJvrcOo9P1nnaR5n" \
                "Ua7elujxQgD9XqTWN09onQznIE3DK" \
                "MUzHl9xtxWEwKIRQmeNvwc8ClaHPO" \
                "712sYPnWZEEk3puch0Oj8jjDU1Sj" \
                "3D4DpioP27x9tfMbcJeJcog_a_0pHN-" \
                "pyEC5FshSuIgST-dJxioifP18MnjcpE" \
                "rkQRQnquwsNKSvn6VWB-VN_i" \
                "__-Cpa4J5Bu2oAQ8Bow3st--A4hqjY" \
                "7j0sHi7-Tm8YHbRnGFsehUbh7SIYmAY9BVjjf6x-Fwv_thIg"

fake = Faker()


def get_headers(token):
    return {'Authorization': f'Bearer {token}'}


now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class MoviesTestCase(unittest.TestCase):
    """This class represents the movies test case"""

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client

    def test_get_authorization_url(self):
        res = self.client().get('/authorization/url')
        self.assertEqual(res.status_code, 200)

    def test_post_movie_with_valid_token(self):
        post_data = {"title": fake.name(), "release_date": "2019/09/22"}
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        res = self.client().post("/movies", json=post_data, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_get_movies_with_invalid_token(self):
        auth_header = get_headers("invalid token")
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Unauthorized")

    def test_patch_movie(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"title": fake.text()}
        movie_id = Movies.query.all()[0].id
        res = self.client().patch(f'/movies/{movie_id}', json=data, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_movie_404(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"title": "fake text"}
        movie_id = 10000
        res = self.client().patch(f'/movies/{movie_id}', json=data, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        movie_id = Movies.query.all()[0].id
        res = self.client().delete(f'/movies/{movie_id}', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_movie_404(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        movie_id = 1000
        res = self.client().patch(f'/movies/{movie_id}', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_get_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_get_actors_401(self):
        auth_header = get_headers("invalid token")
        res = self.client().get("/actors", headers=auth_header)
        self.assertEqual(res.status_code, 401)

    def test_post_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"name": fake.name(), "age": 13, "gender": "Male"}
        res = self.client().post("/actors", headers=auth_header, json=data)
        self.assertEqual(res.status_code, 200)

    def test_patch_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"name": fake.name(), "age": 13, "gender": "Male"}
        self.client().post("/actors", headers=auth_header, json=data)
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        actor_id = Actors.query.all()[0].id
        data = {"name": fake.name()}
        res = self.client().patch(f'/actors/{actor_id}', headers=auth_header, json=data)
        self.assertEqual(res.status_code, 200)

    def test_post_actors_401(self):
        auth_header = get_headers(EXPIRED_TOKEN)
        data = {"name": fake.name(), "age": 13, "gender": "Male"}
        res = self.client().post("/actors", headers=auth_header, json=data)
        self.assertEqual(res.status_code, 401)

    def test_delete_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        actor_id = Actors.query.all()[0].id
        res = self.client().delete(f'/actors/{actor_id}', headers=auth_header)
        self.assertEqual(res.status_code, 200)

    def test_delete_actors_404(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        actor_id = 1000
        res = self.client().delete(f'/movies/{actor_id}', headers=auth_header)
        self.assertEqual(res.status_code, 404)

    def test_401_missing_permission(self):
        auth_header = get_headers(CASTING_ASSISTANT_TOKEN)
        actor_id = Actors.query.all()[0].id
        res = self.client().delete(f'/movies/{actor_id}', headers=auth_header)
        self.assertEqual(res.status_code, 401)

    def test_401_token_expired(self):
        auth_header = get_headers(EXPIRED_TOKEN)
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "token has expired")


if __name__ == '__main__':
    unittest.main()
