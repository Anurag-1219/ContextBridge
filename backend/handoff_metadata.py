from typing import Dict
from datetime import datetime, timezone
import uuid


def create_handoff_metadata(
    source: str = "ContextBridge",
    version: str = "1.0"
) -> Dict:

    return {
        "handoff_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "source": source
    }


def create_handoff_package(
    handoff: Dict,
    source: str = "ContextBridge",
    version: str = "1.0"
) -> Dict:

    metadata = create_handoff_metadata(
        source=source,
        version=version
    )

    return {
        "metadata": metadata,
        "context": handoff
    }
