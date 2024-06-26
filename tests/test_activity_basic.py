import re
import pytest
import logging

from zambeze.campaign.activities.basic import BasicActivity
from zambeze.utils.identity import valid_uuid

@pytest.mark.unit
def test_basic_activity_attributes():
    logger = logging.getLogger(__name__)
    activity = BasicActivity(
        name="Reverse Words",
        fn=lambda line: " ".join(reversed(line.split())),
        line="Hello World",
        logger=logger
    )
    
    # Type is set to "BASIC"
    assert activity.type == "BASIC"

    # Origin agent ID is None. It will be set by the message handler
    assert (
        activity.origin_agent_id is None
    )

    # Verify the fn attribute is a callable
    assert callable(activity.fn)

    # Valid UUIDs
    assert valid_uuid(activity.campaign_id)
    assert valid_uuid(activity.activity_id)

    # Valid submission time (down to milliseconds)
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$"
    assert re.match(pattern, activity.submission_time)