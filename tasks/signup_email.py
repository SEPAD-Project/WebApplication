from source import celery
from source.server_side.Website.Email.signup_verify import verify_code_sender
from pathlib import Path

@celery.task
def start_process_send_signup_email(email, generated_code):
        template_path = Path(__file__).parent.parent / 'server_side' / 'Website' / 'Email' / 'templates' / 'signup_verify.html'

        with open(template_path, 'r') as file:
            html_content = file.read().replace('{{ verification_code }}', generated_code)

        verify_code_sender(email, 'Verify Email', html_content)
    