from bankaccount.shared.abstract_uow import UnitOfWorkManager
from bankaccount.entities.account import Account
from bankaccount.usecases import (response_objects as rs,
                                    request_objects as rq)


class AccountUsecase:
    def __init__(self, uowm: UnitOfWorkManager):
        self._uowm = uowm


class AccountCreationUseCase(AccountUsecase):
    def execute(self, request):
        with self._uowm.start() as unit_of_work:
            try:
                if request:
                    _found_account = unit_of_work.accounts.find_account(account_code= request.account['code'])
                    if(_found_account is None):
                        unit_of_work.accounts.add_account(account= Account(account_code=request.account['code'], 
                                                                            account_balance=request.account['amount']))
                        unit_of_work.commit()
                        response = rs.ResponseSuccess()    
                    else:
                        response = rs.ResponseFailure.build_resource_error('account already exists')
                else:
                    response = rs.ResponseFailure.from_invalid_request(request)
            except Exception as e:
                unit_of_work.rollback()
                response = rs.ResponseFailure.build_system_error(e)
        return response


class AccountDepositUseCase(AccountUsecase):
    def execute(self, request):
        with self._uowm.start() as unit_of_work:
            try:
                if request:
                    _found_account = unit_of_work.accounts.find_account(account_code=request.account['code'])
                    if(_found_account is not None):
                        response = rs.ResponseSuccess(unit_of_work.accounts.account_deposit(account=_found_account,
                                                                                            amount=request.account['amount']))
                        unit_of_work.commit()
                    else:
                        response = rs.ResponseFailure.build_resource_error('account not found')
                else:
                    response = rs.ResponseFailure.from_invalid_request(request)
            except Exception as e:
                unit_of_work.rollback()
                response = rs.ResponseFailure.build_system_error(e)            
        return response


class AccountWithdrawUseCase(AccountUsecase):
    def execute(self, request):
        with self._uowm.start() as unit_of_work:
            try:
                if request:
                    _found_account = unit_of_work.accounts.find_account(account_code=request.account['code'])
                    if(_found_account is not None):    
                        if(float(_found_account.balance) >= float(request.account['amount'])):
                            with self._uowm.start() as unit_of_work:
                                response = rs.ResponseSuccess(unit_of_work.accounts.account_withdraw(account= _found_account,
                                                                                            amount=request.account['amount']))
                                unit_of_work.commit()
                        else:
                            response = rs.ResponseFailure.build_parameters_error('incorrect withdraw amount')
                    else:
                        response = rs.ResponseFailure.build_resource_error('account not found')
                else:
                    response = rs.ResponseFailure.from_invalid_request(request)
            except Exception as e:
                unit_of_work.rollback()
                response = rs.ResponseFailure.build_system_error(e)            
        return response