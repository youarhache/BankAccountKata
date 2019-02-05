from bankaccount.shared.abstract_uow import UnitOfWorkManager
from bankaccount.entities.transfer import Transfer
from bankaccount.entities.account import Account
from bankaccount.usecases import (response_objects as rs,
                                    request_objects as rq)


class TransferHistoryUseCase:
    def __init__(self, repo):
        self._repo = repo
    
    def execute(self, request):
        try:
            if request:
                response = rs.ResponseSuccess(self._repo.list(filters= request.filters))
            else:
                response = rs.ResponseFailure.from_invalid_request(request)
        except Exception as e:
            response = rs.ResponseFailure.build_system_error(e)            
        return response


class TransferAmountUseCase:
    def __init__(self, uowm: UnitOfWorkManager):
        self._uowm = uowm

    def execute(self, request):
        with self._uowm.start() as unit_of_work:
            try:
                if not request:
                    response = rs.ResponseFailure.from_invalid_request(request)
                
                elif len(request.errors) > 0:
                    response = rs.ResponseFailure.build_parameters_error('parameter not in the correct format')
                
                else:
                    _acc_from = unit_of_work.accounts.find_account(account_code= request.transfer['from'])
                    _acc_to = unit_of_work.accounts.find_account(account_code= request.transfer['to'])
                    
                    if request.transfer['from'] ==  request.transfer['to']:
                        response = rs.ResponseFailure.build_parameters_error('payer account must be different than the payee')
                    
                    elif _acc_from is None or _acc_to is None:
                        response = rs.ResponseFailure.build_parameters_error("account doesn't exist")
                    
                    else:
                        _trs = Transfer(request.transfer['id'], 
                                        request.transfer['timestamp'],
                                        _acc_from,
                                        _acc_to, 
                                        request.transfer['amount'])

                        unit_of_work.accounts.account_withdraw(account=_acc_from, amount=_trs.trs_amount)
                        unit_of_work.accounts.account_deposit(account=_acc_to, amount=_trs.trs_amount)
                        unit_of_work.transfers.add_transfer(trs= _trs)
                        unit_of_work.commit()
                        response = rs.ResponseSuccess()
                        
            except Exception as e:
                unit_of_work.rollback()
                response = rs.ResponseFailure.build_system_error(e)

        return response