import json

class TransferEncoder(json.JSONEncoder):
    def default(self, o):
        to_json = {
            "trs_id": o.trs_id,
            "trs_timestamp": str(o.trs_timestamp),
            "trs_from": str(o.trs_from),
            "trs_to": str(o.trs_to),
            "trs_amount": o.trs_amount,
        }

        return to_json