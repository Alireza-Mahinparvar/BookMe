from app import app, forms, models, routes, db
from app.models import User, Meeting
import unittest

user = User(username="user12345", email="u@me.com")
user.set_password("12345")
db.session.add(user)
db.session.commit()

class TestApp(unittest.TestCase):
    
    #Tests that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #Tests that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b"Sign In" in response.data)
    
    #Tests login behaves correctly given correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', 
                               data=dict(username="user12345", 
                                         password="12345"
                                          ), 
                               follow_redirects=True
                                    )
        self.assertTrue(b"Sign In" in response.data)
    
    #Tests logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="user12345", 
                                         password="12345"
                                          ), 
                        follow_redirects=True
                    )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b"Home Page", response.data)
    
        
        
db.session.delete(user)
db.session.commit()
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    