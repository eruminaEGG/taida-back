from datetime import datetime
import boto3
import os
from typing import Any


from scrumble_egg.utils.datetime_util import DatetimeUtil


class CommonDynamoDB:

    @classmethod
    def getTable(cls) -> Any:
        resource: Any = boto3.resource('dynamodb')
        return resource.Table(os.environ["TABLE_NAME"])

    @classmethod
    def create(
        cls,
        key: str,
        item: dict[str, Any],
    ) -> None:
        """
        レコードを作成する共通関数

        Args:
            item (dict[str, Any]): レコードに追加する項目
        """
        timestamp: datetime = DatetimeUtil.get_current_time()
        common_item: dict[str, Any] = {
            "key": key,
            "created_at": timestamp.isoformat(timespec="microseconds"),
            "updated_at": timestamp.isoformat(timespec="microseconds"),
            "is_deleted": False,
        }

        create_item: dict[str, Any] = {**item, **common_item}
        cls.getTable().put_item(Item=create_item)

    @classmethod
    def update(
        cls,
        key: str,
        id: str,
        update_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """
        指定されたidに一致するアイテムを更新する共通関数

        Args:
            key (str): 削除対象のテーブルのキー
            item_id (str): 削除対象のアイテムのid
        """

        update_expression, expression_attribute_names, expression_attribute_values = \
            cls.create_update_expression(update_attributes=update_attributes)

        # アイテムを更新
        updated_item: dict[str, Any] = cls.getTable().update_item(
            Key={"key": key, "id": id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )
        return updated_item.get("Attributes", {})

    @classmethod
    def delete(
        cls,
        key: str,
        id: str,
    ) -> dict[str, Any]:
        """
        指定されたidに一致するアイテムを削除する共通関数

        Args:
            key (str): 削除対象のテーブルのキー
            item_id (str): 削除対象のアイテムのid
        """
        return cls.update(key=key, id=id, update_attributes={"is_deleted": True})

    @classmethod
    def create_update_expression(
        cls,
        update_attributes: dict[str, Any]
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        # 共通の属性を設定
        timestamp: datetime = DatetimeUtil.get_current_time()
        common_item: dict[str, Any] = {
            "updated_at": timestamp.isoformat(timespec="microseconds")
        }

        # 更新する属性を含める
        update_attributes.update(common_item)

        # UpdateExpression を構築
        update_expression: str = "SET "
        expression_attribute_names: dict[str, Any] = {}
        expression_attribute_values: dict[str, Any] = {}

        for attribute_name, attribute_value in update_attributes.items():
            update_expression += f"#{attribute_name} = :{attribute_name}, "
            expression_attribute_names[f"#{attribute_name}"] = attribute_name
            expression_attribute_values[f":{attribute_name}"] = attribute_value

        update_expression = update_expression[:-2]  # Remove the trailing comma and space

        return update_expression, expression_attribute_names, expression_attribute_values

    @classmethod
    def query_all(
        cls,
        params: dict[str, Any]
    ) -> list[dict[str, Any]]:

        # TODO データが多くなった時のページング処理を入れる
        return cls.getTable().query(**params)["Items"]

    @classmethod
    def transform_to_dynamo_db(
        cls,
        item: dict[str, Any]
    ) -> dict[str, Any]:
        """
        dict を DynamoDB クライアント形式に変形する

        Args:
            item (dict[str, Any]): 変形対象の辞書

        Returns:
            dict[str, Any]: 変形後の辞書
        """
        client_item: dict[str, Any] = {}
        for k, v in item.items():
            client_item[k] = cls.to_dynamodb_client(v)

        return client_item

    @classmethod
    def to_dynamodb_client(
        cls,
        value: Any
    ) -> dict[str, Any]:
        """
        値を DynamoDB のクライアント形式に変形する

        Args:
            value (Any): 任意の値

        Returns:
            dict[str, Any]: クライアント形式に変形した値
        """

        if isinstance(value, str):
            return {"S": value}
        elif isinstance(value, int):
            return {"N": str(value)}
        elif isinstance(value, list):
            return {"L": [cls.to_dynamodb_client(item) for item in value]}
        elif isinstance(value, dict):
            return {"M": {k: cls.to_dynamodb_client(v) for k, v in value.items()}}
        elif isinstance(value, bool):
            return {"BOOL": value}
        elif value is None:
            return {"NULL": True}
        else:
            raise Exception(f"Unsupported type: {type(value)}")
