import json
import uuid

from src.repository import memrepo as mr
from src.serializers import user_serializer as ser
from src.shared import response_object as res
from src.use_cases import request_objects as req
from src.use_cases import user_use_cases as uc


def handler(event, context):
    # Если есть заголовок Accept и он не application/json - вернуть ошибку
    # 415  — сервер не может вернуть указанный Content-Type
    STATUS_CODES = {
        res.ResponseSuccess.SUCCESS: 200,
        res.ResponseFailure.RESOURCE_ERROR: 404,
        res.ResponseFailure.PARAMETERS_ERROR: 400,
        res.ResponseFailure.SYSTEM_ERROR: 500,
    }

    user1 = {
        "user_id": uuid.uuid4(),
        "login": "user1",
    }
    user2 = {
        "user_id": uuid.uuid4(),
        "login": "user2",
    }

    params = {
        "filters": {},
    }
    request_object = req.UserListRequestObject.from_dict(params)
    repo = mr.MemRepo([user1, user2])
    use_case = uc.UserListUseCase(repo)
    response = use_case.execute(request_object)

    return {
        "statusCode": STATUS_CODES[response.type],
        "body": json.dumps(response.value, cls=ser.UserModelEncoder),
        "headers": {"Content-Type": "application/json"},
    }
