#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Oak Ridge National Laboratory.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License.

import logging

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
from datetime import datetime

from zambeze.orchestration.message.abstract_message import AbstractMessage


class ActivityStatus(Enum):
    CREATED = auto()
    QUEUED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


class Activity(ABC):
    """An abstract class of a scientific campaign activity.

    :param name: Campaign activity name.
    :type name: str
    :param files: List of file URIs.
    :type files: Optional[list[str]]
    :param command: Action's command.
    :type command: Optional[str]
    :param arguments: List of arguments.
    :type arguments: Optional[list[str]]
    :param logger: The logger where to log information/warning or errors.
    :type logger: Optional[logging.Logger]
    """

    files: list[str]
    command: Optional[str]
    arguments: list[str]
    logger: Optional[logging.Logger]
    campaign_id: Optional[str]
    origin_agent_id: Optional[str]
    running_agent_ids: Optional[list[str]]
    message_id: Optional[str]
    activity_id: Optional[str]
    source_file: Optional[str]
    dest_directory: Optional[str]
    override_existing: Optional[bool]

    def __init__(
        self,
        name: str,
        files: list[str] = None,
        command: Optional[str] = None,
        arguments: list[str] = None,
        logger: Optional[logging.Logger] = None,
        campaign_id: Optional[str] = None,
        origin_agent_id: Optional[str] = None,
        running_agent_ids: Optional[list[str]] = None,  # Set default to None
        message_id: Optional[str] = None,
        activity_id: Optional[str] = None,
        source_file: Optional[str] = None,
        dest_directory: Optional[str] = None,
        override_existing: Optional[bool] = False,
        submission_time: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.running_agent_ids = (
            running_agent_ids if running_agent_ids is not None else []
        )

        """Create an object that represents a science campaign activity."""
        self.logger = logging.getLogger(__name__) if logger is None else logger
        self.name: str = name
        self.files = files
        self.command = command
        self.arguments = arguments
        self.campaign_id = campaign_id
        self.origin_agent_id = origin_agent_id
        self.submission_time = submission_time
        self.message_id = message_id
        self.activity_id = activity_id
        self.source_file = source_file
        self.dest_directory = dest_directory
        self.override_existing = override_existing
        self.status: ActivityStatus = ActivityStatus.CREATED
        self.__dict__.update(kwargs)

        self.submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    def add_files(self, files: list[str]) -> None:
        """Add a list of files to the dataset.

        :param files: List of file URIs.
        :type files: list[str]
        """
        self.files.extend(files)

    def add_file(self, file: str) -> None:
        """Add a file to the dataset.

        :param file: A URI to a single file.
        :type file: str
        """
        self.files.append(file)

    def add_arguments(self, args: list[str]) -> None:
        """Add a list of arguments to the action.

        :param args: List of arguments.
        :type args: list[str]
        """
        self.arguments.extend(args)

    def add_argument(self, arg: str) -> None:
        """Add an argument to the action.

        :param arg: An argument.
        :type arg: str
        """
        self.arguments.append(arg)

    def set_command(self, command: str) -> None:
        """Set the action's command.

        :param command: A command.
        :type command: str
        """
        self.command = command

    def get_status(self) -> ActivityStatus:
        """Get current activity status.

        :return: Current activity status
        :rtype: ActivityStatus
        """
        return self.status

    @abstractmethod
    def generate_message(self) -> AbstractMessage:
        raise NotImplementedError(
            "Method to generate message has not been instantiated."
        )
