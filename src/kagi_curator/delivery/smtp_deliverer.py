from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from .base_deliverer import BaseDeliverer


class SMTPDeliverer(BaseDeliverer):
    """Delivers newsletters via SMTP."""

    def __init__(
        self,
        smtp_host: str,
        from_address: str,
        to_addresses: List[str],
        smtp_port: int = 587,
        smtp_username: str | None = None,
        smtp_password: str | None = None,
        from_name: str = "Daily News Digest",
        use_tls: bool = True,
    ) -> None:
        self._host = smtp_host
        self._port = smtp_port
        self._username = smtp_username
        self._password = smtp_password
        self._from_address = from_address
        self._from_name = from_name
        self._to_addresses = to_addresses
        self._use_tls = use_tls

    def deliver(self, subject: str, html_content: str, plain_content: str = "") -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = (
            f"{self._from_name} <{self._from_address}>"
            if self._from_name else self._from_address
        )
        msg["To"] = ", ".join(self._to_addresses)

        if plain_content:
            msg.attach(MIMEText(plain_content, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        with smtplib.SMTP(self._host, self._port) as server:
            if self._use_tls:
                server.starttls()
            if self._username and self._password:
                server.login(self._username, self._password)
            server.sendmail(
                self._from_address,
                self._to_addresses,
                msg.as_string(),
            )
