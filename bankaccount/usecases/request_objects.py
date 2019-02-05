import collections


class Request:
    def __init__(self):
        self.errors = []

    def has_errors(self):
        return (len(self.errors)>0)

    def add_error(self, param, msg):
        self.errors.append({'parameter':param, 'message':msg})

    def __bool__(self):
        return (not self.has_errors())

class TransferHistoRequest(Request):
    def __init__(self, filters=None):
        self.errors = []
         #ToDo : add more validation conditions
        if filters is not None and not isinstance(filters, collections.Mapping):
            self.add_error('filters', 'parameter not in the correct format')
        else:
            self.filters = filters

    @classmethod
    def from_dict(cls, dict):
        return cls(filters = dict.get('filters', None))


class AccountOperationRequest(Request):
    def __init__(self, account=None):
        self.errors = []
        #ToDo : add more validation conditions
        if account is None:
            self.add_error('account', 'parameter is required')

        elif not isinstance(account, collections.Mapping):
            self.add_error('account', 'parameter not in the correct format')

        elif 'code' not in account or 'amount' not in account:
            self.add_error('account', 'account code and amount are required')

        elif len(account['code']) == 0:
            self.add_error('account', "account code can't be empty")

        elif not isinstance(account['amount'], float) or float(account['amount']) < 0:
            self.add_error('account', "amount must be a positive number")
            
        else:
            self.account = account

    @classmethod
    def from_dict(cls, dict):
        return cls(account = dict.get('account', None))


class TransferAmountRequest(Request):
    def __init__(self, trs=None):
        self.errors = []
        if trs is None:
            self.add_error('transfer', 'parameter is required')

        elif not isinstance(trs, collections.Mapping):
            self.add_error('transfer', 'parameter not in the correct format')

        elif ('from' not in trs or 'to' not in trs or 'amount' not in trs 
               or 'id' not in trs or 'timestamp' not in trs):
            self.add_error('transfer', 'a required attribute is missing')

        elif not trs['id']:
            self.add_error('transfer', "ID can't be empty")        

        elif not trs['from'] or not trs['to']:
            self.add_error('transfer', "account codes can't be empty")

        elif not isinstance(trs['amount'], float) or float(trs['amount']) < 0:
            self.add_error('transfer', "amount must be a positive number")

        else:
            self.transfer = trs

    @classmethod
    def from_dict(cls, dict):
        return cls(trs = dict.get('transfer', None))