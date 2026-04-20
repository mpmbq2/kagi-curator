from __future__ import annotations

import os
import sys
from datetime import datetime

from .config.loader import load_config
from .config.pipeline import build_pipeline
from .delivery.smtp_deliverer import SMTPDeliverer
from .formatting.email_formatter import EmailFormatter
from .formatting.plain_text_formatter import PlainTextFormatter


def main() -> None:
    config_path = os.environ.get("KAGI_CURATOR_CONFIG")
    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        print(f"Error: configuration file not found — {e}", file=sys.stderr)
        sys.exit(1)

    use_email_format = os.environ.get("KAGI_FORMAT", "").lower() == "email"
    send_email = os.environ.get("KAGI_SEND_EMAIL", "").lower() in ("1", "true", "yes")

    formatter = EmailFormatter() if (use_email_format or send_email) else PlainTextFormatter()
    orchestrator = build_pipeline(config, formatter)
    output = orchestrator.generate_newsletter()

    if send_email:
        if not config.email:
            print(
                "Error: KAGI_SEND_EMAIL is set but no [email] section in config.",
                file=sys.stderr,
            )
            sys.exit(1)
        ec = config.email
        deliverer = SMTPDeliverer(
            smtp_host=ec.smtp_host,
            from_address=ec.from_address,
            to_addresses=ec.to_addresses,
            smtp_port=ec.smtp_port,
            smtp_username=ec.smtp_username,
            smtp_password=ec.smtp_password,
            from_name=ec.from_name,
            use_tls=ec.use_tls,
        )
        deliverer.deliver(subject=_render_subject(ec.subject), html_content=output)
        print(f"Email sent to: {', '.join(ec.to_addresses)}")
    else:
        print(output)


def _render_subject(template: str) -> str:
    return template.replace("{date}", datetime.now().strftime("%B %-d, %Y"))
