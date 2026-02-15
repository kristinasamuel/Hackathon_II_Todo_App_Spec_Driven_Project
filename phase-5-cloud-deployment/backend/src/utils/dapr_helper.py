import os
from typing import Dict, Any
import json
from dapr.clients import DaprClient
from dapr.conf import Settings
import logging

logger = logging.getLogger(__name__)

def publish_event(pubsub_name: str, topic_name: str, event_data: Dict[str, Any]):
    """
    Publish an event via DAPR with fallback for local development
    """
    # Check if DAPR is available by attempting to connect
    dapr_enabled = os.getenv('DAPR_ENABLED', 'true').lower() == 'true'
    
    if dapr_enabled:
        try:
            with DaprClient() as dapr_client:
                # Test connection first
                dapr_client.get_metadata()
                
                # Publish the event
                dapr_client.publish_event(
                    pubsub_name=pubsub_name,
                    topic_name=topic_name,
                    data=json.dumps(event_data),
                    data_content_type='application/json'
                )
                print(f"Published event to pubsub '{pubsub_name}', topic '{topic_name}': {event_data.get('eventType', 'unknown')}")
        except Exception as e:
            # Log the error but don't fail the operation
            print(f"DAPR publishing failed: {e}. Continuing without DAPR.")
            logger.warning(f"DAPR publishing failed: {e}. Continuing without DAPR.")
    else:
        # DAPR explicitly disabled
        print(f"DAPR disabled. Skipping event publish: {event_data.get('eventType', 'unknown')}")