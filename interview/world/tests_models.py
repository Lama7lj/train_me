
from django.test import TestCase
from django.utils import timezone
from .models import DjangoMigrations, User, InterviewAnswer

class ModelsTestCase(TestCase):

    def test_django_migrations_model(self):
        migration = DjangoMigrations.objects.create(
            app='world',
            name='0001_initial',
            applied=timezone.now()
        )
        self.assertEqual(migration.app, 'world')
        self.assertEqual(migration.name, '0001_initial')
        self.assertIsNotNone(migration.applied)

    def test_user_model(self):
        user = User.objects.create_user(
            email_id='test@example.com',
            first_name='John',
            last_name='Doe',
            password='password'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_interview_answer_model(self):
        user = User.objects.create_user(
            email_id='test@example.com',
            first_name='John',
            last_name='Doe',
            password='password'
        )
        answer = InterviewAnswer.objects.create(
            user=user,
            about_yourself='I am John Doe.',
            hear_about='From a friend.',
            company_info='Good company.',
            apply_position='Software Engineer'
        )
        self.assertEqual(answer.user.email, 'test@example.com')
        self.assertEqual(answer.about_yourself, 'I am John Doe.')
        self.assertEqual(answer.hear_about, 'From a friend.')
        self.assertEqual(answer.company_info, 'Good company.')
        self.assertEqual(answer.apply_position, 'Software Engineer') 

