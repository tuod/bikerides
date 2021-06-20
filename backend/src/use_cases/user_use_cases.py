from src.shared import response_object as res
from src.shared import use_case as uc


class UserListUseCase(uc.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_user = self.repo.list(filters=request_object.filters)
        return res.ResponseSuccess(domain_user)
