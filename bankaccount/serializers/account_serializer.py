import json

class AccountEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_json = {
                "code":str(o.code).replace("\'", "\""),
                "balance":o.balance
            }
            return to_json
        except AttributeError:
            return super().default(o)