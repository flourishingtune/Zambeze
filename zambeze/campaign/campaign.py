#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Oak Ridge National Laboratory.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License.

import logging

from .activities.abstract_activity import Activity
from ..orchestration.agent import Agent

from typing import Optional


class Campaign:
    """A Scientific Campaign.

    :param name: The campaign name.
    :type name: str
    :param activities: List of activities.
    :type activities: Optional[list[Activity]]
    :param logger: The logger where to log information/warning or errors.
    :type logger: Optional[logging.Logger]
    """

    def __init__(
        self,
        name: str,
        activities: Optional[list[Activity]] = [],
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Create an object that represents a science campaign."""
        self.logger: logging.Logger = (
            logging.getLogger(__name__) if logger is None else logger
        )
        self.name: str = name
        self.activities: list[Activity] = activities
        self.agent = Agent(logger=self.logger)

    def add_activity(self, activity: Activity) -> None:
        """Add an activity to the campaign.

        :param activity: An activity object.
        :type activity: Activity
        """
        self.logger.debug(f"Adding activity: {activity.name}")
        self.activities.append(activity)

    def dispatch(self) -> None:
        """Dispatch the set of current activities in the campaign."""
        for activity in self.activities:
            self.logger.debug(f"Running activity: {activity.name}")
            self.agent.dispatch_activity(activity)
