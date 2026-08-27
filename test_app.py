import unittest
from app import app, db, Students

class StudentAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_show_all_screen(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<th>Phone</th>', html)
        self.assertIn('Hassan Ali', html)
        print('test_show_all_screen passed.')

    def test_new_student_screen(self):
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Phone Number:', html)
        self.assertIn('name="phone"', html)
        print('test_new_student_screen passed.')

    def test_create_new_student_with_phone(self):
        payload = {
            'name': 'Test Student',
            'city': 'Seattle',
            'addr': '123 Pine Street',
            'pin': '98101',
            'phone': '555-999-8888'
        }
        response = self.client.post('/new', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Record was successfully added', html)
        self.assertIn('Test Student', html)
        self.assertIn('Seattle', html)
        self.assertIn('555-999-8888', html)
        print('test_create_new_student_with_phone passed.')

        # Verify DB directly & cleanup
        with app.app_context():
            student = Students.query.filter_by(name='Test Student').first()
            self.assertIsNotNone(student)
            self.assertEqual(student.phone, '555-999-8888')
            db.session.delete(student)
            db.session.commit()
            print('DB check & cleanup passed.')

if __name__ == '__main__':
    unittest.main()
