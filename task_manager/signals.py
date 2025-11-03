# core/signals.py для отладки потом удалить

import logging
from django.db.backends.signals import connection_created

logger = logging.getLogger(__name__)

def handle_connection_created(sender, connection, **kwargs):
    engine = connection.vendor
    name = connection.settings_dict["NAME"]
    host = connection.settings_dict.get("HOST")
    port = connection.settings_dict.get("PORT")
    
    message = f"Connected to {engine.upper()} database: {name}"
    if host:
        message += f" ({host}:{port})"
    
    logger.info(message)

connection_created.connect(handle_connection_created)