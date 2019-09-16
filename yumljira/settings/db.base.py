DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yumljira',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'CHARSET': 'UTF8',
            'NAME': 'yumljira-test'
        }
    }
}

