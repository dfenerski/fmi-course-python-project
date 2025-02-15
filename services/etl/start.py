import django
from django.conf import settings
from pathlib import Path


BASE_DIR = Path(__file__).resolve()

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR.parent.parent / 'database' / 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        'start',
    ]
)

django.setup()


def main():
    from django.contrib.auth.models import User
    for obj in User.objects.all():
        print(obj)


if __name__ == "__main__":
    main()
