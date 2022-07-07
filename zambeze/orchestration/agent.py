#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Oak Ridge National Laboratory.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License.

import asyncio
import logging
import pathlib

from typing import Optional
from .processor import Processor, MessageType
from ..campaign.activities.abstract_activity import Activity, ActivityStatus
from ..settings import ZambezeSettings


class Agent:
    """A distributed Agent.

    :param conf_file: Path to configuration file
    :type conf_file: Optional[pathlib.Path]
    :param logger: The logger where to log information/warning or errors.
    :type logger: Optional[logging.Logger]
    """

    def __init__(
        self,
        conf_file: Optional[pathlib.Path] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Create an object that represents a distributed agent."""
        self._logger: logging.Logger = (
            logging.getLogger(__name__) if logger is None else logger
        )
        self._settings = ZambezeSettings(conf_file=conf_file, logger=self._logger)
        self._processor = Processor(settings=self._settings, logger=self._logger)
        self._processor.start()

    @property
    def processor(self) -> None:
        return self._processor

    def dispatch_activity(self, activity: Activity) -> None:
        """
        Dispatch an activity.

        :param activity: An activity object.
        :type activity: Activity
        """
        asyncio.run(
            self.processor.send(MessageType.COMPUTE.value, activity.generate_message())
        )
        activity.status = ActivityStatus.QUEUED
