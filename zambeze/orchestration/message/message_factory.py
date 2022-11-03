import logging
from typing import Optional

from .message_activity import MessageActivity
from .message_status import MessageStatus
from .message_activity_validator import (MessageActivityValidator,
                                         createActivityTemplate)
from .message_status_validator import (MessageStatusValidator,
                                       createStatusTemplate)
from .abstract_message import AbstractMessage
from ..zambeze_types import MessageType


class MessageFactory:
    def __init__(self, plugins, logger: Optional[logging.Logger] = None):
        self._logger = logger
        self._plugins = plugins

    def createTemplate(
            self,
            message_type: MessageType,
            plugin_name=None,
            args=None) -> tuple:
        """
        Will create a tuple with all the fields needed to built a message

        :param message_type: there are currently two supported message types
        status and activity.
        :type message_type: MessageType
        :param plugin_name: The name of the plugin if any are used to create the
        body of the message
        :type plugin_name: str
        :param args: arguments needed by the plugin to pick an appropriate
        template
        :type args: not yet specified, could be specific to plugin

        :return: the message outline and the MessageType which was passed in
        :rtype: (MessageType, dict)

        :Example:

        >>> factory = MessageFactory()
        >>> activity_msg_globus = factory.createTemplate(
        >>>                                          MessageType.ACTIVITY,
        >>>                                          "globus",
        >>>                                          "transfer")
        >>> # In the print statement below the body: {} content is generated by
        >>> # the plugin.
        >>> print(activity_msg_globus[0].value)
        >>> ACTIVITY
        >>> print(activity_msg_globus[1])
        >>> {   "message_id": "",
        >>>     "type": "",
        >>>     "activity_id": "",
        >>>     "agent_id": "",
        >>>     "campaign_id": "",
        >>>     "credential": {},
        >>>     "submission_time": "",
        >>>     "body": {
        >>>       "plugin": "globus",
        >>>       "transfer": {
        >>>             "type": "synchronous",
        >>>             "items": [
        >>>                 {
        >>>                     "source": "globus://XXXXXXXX...X-XXXXXXXX/file1.txt",
        >>>                     "destination": "globus://YYY...YYYYYYYY/dest/file1.txt"
        >>>                 },
        >>>                 {
        >>>                     "source": "globus://XXXXXXXX-...XXXXXXXXXXXX/file2.txt",
        >>>                     "destination": "globus://YYYY...YYYYYYYY/dest/file2.txt"
        >>>                 }
        >>>             ]
        >>>             }
        >>>         }
        >>>     },
        >>>     "needs": []
        >>> }
        """
        if message_type == MessageType.ACTIVITY:
            activity = createActivityTemplate()
            if plugin_name is not None:
                activity["body"] = self._plugins.messageTemplate(plugin_name, args)
            return (message_type, activity)
        elif message_type == MessageType.STATUS:
            status = createStatusTemplate()
            return (message_type, status)
        else:
            raise Exception(
                "Unrecognized message type cannot createTemplate: "
                f"{message_type.value}"
            )

    def create(self, args: tuple) -> AbstractMessage:
        """Is responsible for creating a Message

        The tuple must be of the form:

        ( MessageType, {} )

        :Example:

        ( MessageType.ACTIVITY, activity_msg )

        """

        if len(args) != 2:
            raise Exception("Malformed input, create method expects tuple of"
                            "length 2")

        if args[0] == MessageType.ACTIVITY:
            validator = MessageActivityValidator()
            result = validator.validateMessage(args[1])
            if result[0]:
                if "plugin" in args[1]["body"]:
                    plugin_name = args[1]["plugin"]
                    results = self._plugins.validateMessage(plugin_name,
                                                            args[1]["body"])
                    if results[0] is False:
                        raise Exception("Invalid plugin message body"
                                        f"{results[1]}")
                return MessageActivity(self._logger, args[1])
            else:
                raise Exception("Invalid activity message: {result[1]}")
        elif args[0] == MessageType.STATUS:
            validator = MessageStatusValidator()
            result = validator.check(args[1])
            if result[0]:
                return MessageStatus(args[1])
            else:
                raise Exception("Invalid status message: {result[1]}")
        else:
            raise Exception(
                "Unrecognized message type cannot instantiate: " f"{args[0].value}"
            )
