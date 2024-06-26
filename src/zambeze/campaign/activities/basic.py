# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Oak Ridge National Laboratory.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License.

import time
import uuid
from typing import Callable

from zambeze.campaign.activities.abstract_activity import Activity
from zambeze.orchestration.message.abstract_message import AbstractMessage
from zambeze.orchestration.message.message_factory import MessageFactory
from zambeze.orchestration.zambeze_types import MessageType, ActivityType


class BasicActivity(Activity):
    """Allows executing a python method as a campaign activity. 

    :param name: Campaign activity name.
    :type name: str

    :param fn: The function to execute.
    :type fn: Callable

    :param logger: The logger where to log information/warning or errors.
    :type logger: Optional[logging.Logger]
    """

    def __init__(
        self,
        name: str,
        fn: Callable,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            message_id=str(uuid.uuid4()),
            activity_id=str(uuid.uuid4()),
        )
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def generate_message(self) -> AbstractMessage:
        factory = MessageFactory(logger=self.logger)
        template = factory.create_template(
            MessageType.ACTIVITY, ActivityType.BASIC
        )

        # Message fields
        template[1].origin_agent_id = self.origin_agent_id
        template[1].running_agent_ids = self.running_agent_ids
        template[1].activity_id = self.activity_id
        template[1].message_id = self.message_id
        template[1].campaign_id = self.campaign_id
        template[1].submission_time = str(int(time.time()))

        # BASIC activity specific fields
        template[1].body.type = "BASIC"
        template[1].body.fn = self.fn

        return factory.create(template)