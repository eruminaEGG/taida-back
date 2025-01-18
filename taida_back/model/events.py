from uuid import UUID, uuid4
from boto3.dynamodb.conditions import Key, Attr

from typing import Any, Dict, List, Tuple
from scrumble_egg.model.common_dynamodb import CommonDynamoDB
from scrumble_egg.core.enums.event_enum import EventType
from scrumble_egg.core.validations.event_validation import EventValidation


class Event(CommonDynamoDB):

    KEY: str = "EVENTS"

    def __init__(
        self,
        id: UUID,
        event_type: EventType,
        text: str,
        guild_id: str,
        is_egg: bool,
        is_active: bool,
    ) -> None:
        self.id = id
        self.event_type = event_type
        self.text = text
        self.guild_id = guild_id
        self.is_egg = is_egg
        self.is_active = is_active

    @classmethod
    def create_event(
        cls,
        event_type: EventType,
        text: str,
        guild_id: str,
        is_egg: bool,
        is_active: bool,
    ) -> "Event":

        item: Dict[str, Any] = {
            "id": str(uuid4()),
            "event_type": event_type.value,
            "guild_id": guild_id,
            "is_active": is_active,
            "is_egg": is_egg,
            "text": text,
        }

        cls.create(
            key=cls.KEY,
            item=item,
        )

        return cls.json_to_obj(item=item)

    @classmethod
    def get_by_id(
        cls,
        id: str,
        guild_id: str,
    ) -> "Event | None":

        params: Dict[str, Any] = {
            "KeyConditionExpression": Key('key').eq(cls.KEY) & Key('id').eq(id),
            "FilterExpression": Attr('guild_id').eq(guild_id) & Attr('is_deleted').eq(False)
        }

        items: List[Dict[str, Any]] = cls.query_all(params=params)

        if len(items) != 1:
            return None

        return cls.json_to_obj(item=items[0])

    @classmethod
    def list_events_by_guild_id(
        cls,
        guild_id: str,
        offset: int,
        limit: int | None,
        include_egg_events: bool = True,
        order_by: str = "created_at",
        is_asc: bool = True,
    ) -> Tuple[int, List["Event"]]:

        params: Dict[str, Any] = {
            "KeyConditionExpression": Key('key').eq(cls.KEY),
            "FilterExpression": Attr('guild_id').eq(guild_id) & Attr('is_deleted').eq(False)
        }

        if include_egg_events:
            # #GGのイベントも含める
            params["FilterExpression"] |= Attr('is_egg').eq(True) & Attr('is_deleted').eq(False)

        items: List[Dict[str, Any]] = cls.query_all(params=params)

        # アイテムをソート
        items.sort(key=lambda x: x[order_by], reverse=not is_asc)

        limited_items: List[Dict[str, Any]] = items[offset: offset + limit] if \
            limit is not None else items[offset:]

        return len(items), [cls.json_to_obj(item=item) for item in limited_items]

    def update_event(self) -> "Event":
        updated_event: dict[str, Any] = self.update(
            key=self.KEY,
            id=str(self.id),
            update_attributes={
                "event_type": self.event_type.value,
                "guild_id": self.guild_id,
                "is_egg": self.is_egg,
                "is_active": self.is_active,
                "text": self.text,
            }
        )

        return self.json_to_obj(item=updated_event)

    def delete_event(self) -> None:
        self.delete(
            key=self.KEY,
            id=str(self.id),
        )

    @classmethod
    def json_to_obj(
        cls,
        item: Dict[str, Any]
    ) -> "Event":

        event_type: EventType = EventValidation.validate_event_type(item["event_type"])

        return cls(
            id=UUID(item["id"]),
            event_type=event_type,
            guild_id=item["guild_id"],
            is_egg=item["is_egg"],
            is_active=item["is_active"],
            text=item["text"],
        )

    def to_json(self):
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "guild_id": self.guild_id,
            "is_egg": self.is_egg,
            "is_active": self.is_active,
            "text": self.text,
        }
