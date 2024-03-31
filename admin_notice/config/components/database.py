import os


# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DJANGO_ADMIN_NOTICE_DB_ENGINE'),
#         'NAME': os.environ.get('PG_ADMIN_NOTICE_DB_NAME'),
#         'USER': os.environ.get('PG_ADMIN_NOTICE_USER'),
#         'PASSWORD': os.environ.get('PG_ADMIN_NOTICE_PASSWORD'),
#         'HOST': os.environ.get('PG_ADMIN_NOTICE_DB_HOST', '127.0.0.1'),
#         'PORT': os.environ.get('PG_ADMIN_NOTICE_DB_PORT', 5436),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'notify'),
        'USER': os.environ.get('DB_USER', 'admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', 5432),
        # 'OPTIONS': {
        #     # Нужно явно указать схемы, с которыми будет работать приложение.
        #     'options': '-c search_path=public,content'
        # }
    }
}