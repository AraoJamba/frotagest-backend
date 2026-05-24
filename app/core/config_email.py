
from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="eulilnerty@gmail.com",
    MAIL_PASSWORD="dkwa zaaf nsuw vmlg",
    MAIL_FROM="eulilnerty@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="FrotaGest",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS = True
)