from django.apps import apps

def get_all_custom_models():
    default_models = ['Session', 'ContentType','LogEntry','Group', 'Permission', 'User']
    custom_models = []

    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models