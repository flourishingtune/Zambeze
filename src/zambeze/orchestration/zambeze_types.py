from enum import Enum


class ChannelType(Enum):
    ACTIVITY = "ACTIVITY"
    STATUS = "STATUS"
    TEST = "TEST"


class MessageType(Enum):
    ACTIVITY = "ACTIVITY"
    STATUS = "STATUS"


class ActivityType(Enum):
    BASIC = "BASIC"
    SHELL = "SHELL"
    PLUGIN = "PLUGIN"
    TRANSFER = "TRANSFER"


class QueueType(Enum):
    RABBITMQ = "RabbitMQ"
    NATS = "NATS"
