from datetime import timedelta

class DownloadToken:
    def __init__(self, id, files):
        self.id = id
        self.grace_period = timedelta(hours=24)
        self.files = files
        self.downloads = []