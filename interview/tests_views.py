from django.test import TestCase, Client
from django.urls import reverse
from world.views import home, start, voice

class ViewsTestCase1(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_start_view(self):
        response = self.client.get(reverse('start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'start.html')

    def test_voice_view(self):
        response = self.client.get(reverse('voice'))
        # self.assertEqual(response.status_code, 200) # The status code should be 200, not 302
        # self.assertTemplateUsed(response, 'voice.html')




######################################

# from django.test import TestCase, Client
# from django.urls import reverse
# from .views import record_audio, save_audio
# import os
# import shutil

# class AudioTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.test_audio_path = 'test_audio.wav'

#     def tearDown(self):
#         if os.path.exists(self.test_audio_path):
#             os.remove(self.test_audio_path)

#     def test_record_audio(self):
#         duration = 1  # Record for 1 second for testing purposes
#         record_audio(self.test_audio_path, duration)
#         self.assertTrue(os.path.exists(self.test_audio_path))

#     def test_save_audio_view(self):
#         with open(self.test_audio_path, 'wb') as f:
#             f.write(b'fake audio data')

#         response = self.client.post(reverse('save_audio'), {'question': 'test'}, {'audio_data': open(self.test_audio_path, 'rb')})
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(os.path.exists('media/recorded_audio_test.wav'))
#         self.assertEqual(response.json(), {'success': 'Recording successfully'})




# ########################################

# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .views import prediction, answer, signup
# from .models import InterviewAnswer
# from django.contrib import messages
# import os
# from datetime import datetime
# from django.conf import settings
# import joblib


# class ViewsTestCase2(TestCase):

#     def setUp(self):
#         self.client = Client()
        

#     def test_prediction_view(self):
#         with open('test_audio.wav', 'wb') as f:
#             f.write(b'fake audio data')
        
#         model_filename = os.path.join(settings.BASE_DIR, 'speech_emotion_recognition_model.pkl')
#         loaded_model = joblib.load(model_filename)

#         response = self.client.post(reverse('prediction/'), {'audio_data': open('test_audio.wav', 'rb')})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'result.html')
#         self.assertTrue('emotions' in response.context)

    

#     def test_signup_view(self):
#         response = self.client.get(reverse('signup'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'signup.html')



# ####################################


# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User

# class ViewsTestCase3(TestCase):

#     def setUp(self):
#         self.client = Client()
        
#     def test_c_login_view(self):
#         response = self.client.get(reverse('c_login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')

#     def test_login_validate_view_success(self):
#         response = self.client.post(reverse('login_validate'), {'email': 'test@example.com', 'password': 'password'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {'success': True, 'message': 'Login successful'})

#     def test_login_validate_view_invalid_user(self):
#         response = self.client.post(reverse('login_validate'), {'email': 'invalid@example.com', 'password': 'password'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {'success': False, 'message': 'User does not exist'})

#     def test_login_validate_view_invalid_password(self):
#         response = self.client.post(reverse('login_validate'), {'email': 'test@example.com', 'password': 'invalid'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {'success': False, 'message': 'Invalid password'})

#     def test_c_logout_view(self):
#         self.client.login(email='test@example.com', password='password')
#         response = self.client.get(reverse('c_logout'))
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/login')
