class Config:
    ENVIRONMENT = "production"
    DEBUG = False
    TESTING = False

    # File uploads
    # MAX_CONTENT_LENGTH sets maximum file size for non-multipart uploads. Flask will raise a RequestEntityTooLarge
    # exception if uploaded file exceeds this limit.
    MAX_CONTENT_LENGTH = 2 * 1000 * 1000 * 1000  # 2GB
    MULTIPART_UPLOAD_CHUNK_SIZE_MB = 1_000  # 1GB


class DevelopmentConfig(Config):
    ENVIRONMENT = "development"
    DEBUG = True
