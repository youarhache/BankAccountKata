from bankaccount.usecases import (response_objects as rs,
                                    request_objects as rq)


class TransferHistoryUseCase:
    def __init__(self, repo):
        self.repo = repo
    
    def execute(self, request):
        try:
            if request:
                response = rs.ResponseSuccess(self.repo.list(filters= request.filters))
            else:
                response = rs.ResponseFailure.from_invalid_request(request)
        except Exception as e:
            response = rs.ResponseFailure.build_system_error(e)            
        return response


class TransferAmountUseCase:
    def __init__(self, trs_repo, account_repo):
        self.trs_repo = trs_repo
        self.acc_repo = account_repo

    def _get_account(self, code):
        return self.acc_repo.find_account(account_code= code)

    def execute(self, request):
        try:
            if not request:
                response = rs.ResponseFailure.from_invalid_request(request)
            elif request.transfer['from'] ==  request.transfer['to']:
                response = rs.ResponseFailure.build_parameters_error('payer account must be different than the payee')
            elif self._get_account(request.transfer['from']) is None or self._get_account(request.transfer['to']) is None:
                response = rs.ResponseFailure.build_parameters_error("account doesn't exist")
            else:
                _trs = request.transfer
                resp_payer = self.acc_repo.account_withdraw(account={'code':_trs['from'], 'amount':_trs['amount']})
                if resp_payer:
                    resp_payee = self.acc_repo.account_deposit(account={'code':_trs['to'], 'amount':_trs['amount']})
                    if resp_payee:
                        response = rs.ResponseSuccess(self.trs_repo.add_transfer(trs= _trs))
                    else:
                        response = rs.ResponseFailure.build_resource_error("payee account could't be credited")
                        #rollback payer debit
                        self.acc_repo.account_deposit(account={'code':_trs['from'], 'amount':_trs['amount']})
                else:
                    response = rs.ResponseFailure.build_resource_error("payer account could't be debited") 
        except Exception as e:
            response = rs.ResponseFailure.build_system_error(e)

        return response