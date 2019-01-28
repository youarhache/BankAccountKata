from bankaccount.usecases import (response_objects as rs,
                                    request_objects as rq)


class AccountUsecase:
    def __init__(self, repo):
        self.repo = repo

    def _get_account(self, code):
        return self.repo.find_account(account_code= code)


class AccountCreationUseCase(AccountUsecase):
    def execute(self, request):
        try:
            if request:
                if(self._get_account(request.account['code']) is None):
                    response = rs.ResponseSuccess(self.repo.add_account(account= request.account))
                else:
                    response = rs.ResponseFailure.build_resource_error('account already exists')
            else:
                response = rs.ResponseFailure.from_invalid_request(request)
        except Exception as e:
            response = rs.ResponseFailure.build_system_error(e)            
        return response


class AccountDepositUseCase(AccountUsecase):
    def execute(self, request):
        try:
            if request:
                if(self._get_account(request.account['code']) is not None):
                    response = rs.ResponseSuccess(self.repo.account_deposit(account= request.account))
                else:
                    response = rs.ResponseFailure.build_resource_error('account not found')
            else:
                response = rs.ResponseFailure.from_invalid_request(request)
        except Exception as e:
            response = rs.ResponseFailure.build_system_error(e)            
        return response


class AccountWithdrawUseCase(AccountUsecase):
    def execute(self, request):
        try:
            if request:
                _found_account = self._get_account(request.account['code'])
                if(_found_account is not None):    
                    if(_found_account.balance >= float(request.account['amount'])):
                        response = rs.ResponseSuccess(self.repo.account_withdraw(account= request.account))
                    else:
                        response = rs.ResponseFailure.build_parameters_error('incorrect withdraw amount')
                else:
                    response = rs.ResponseFailure.build_resource_error('account not found')
            else:
                response = rs.ResponseFailure.from_invalid_request(request)
        except Exception as e:
            response = rs.ResponseFailure.build_system_error(e)            
        return response