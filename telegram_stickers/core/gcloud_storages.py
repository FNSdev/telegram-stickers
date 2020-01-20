from storages.backends.gcloud import GoogleCloudStorage


class GoogleCloudMediaStorage(GoogleCloudStorage):
    def __init__(self, **settings):
        settings['location'] = 'media'
        super().__init__(**settings)
