from zambeze.orchestration.db.model.abstract_entity import AbstractEntity
from typing import Dict


class ActivityModel(AbstractEntity):
    ID_FIELD_NAME = "activity_id"
    FIELD_NAMES = "activity_id, agent_id, created_at, started_at, ended_at, params"
    ENTITY_NAME = "Activity"

    def __init__(
        self,
        activity_id=None,
        agent_id=None,
        created_at=None,
        started_at=None,
        ended_at=None,
        params=None,
    ):
        self.activity_id = activity_id
        self.agent_id = agent_id
        self.created_at = created_at
        self.started_at = started_at
        self.ended_at = ended_at
        self.params = params

    def get_all_values(self) -> Dict:
        vals = {
            "activity_id": self.activity_id,
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "params": self.params,
        }
        return vals

    def get_values_without_id(self) -> Dict:
        vals = {
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "params": self.params,
        }
        return vals
