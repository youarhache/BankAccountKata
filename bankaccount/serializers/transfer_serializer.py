import json

class TransferEncoder(json.JSONEncoder):
    def default(self, o):
        to_json = {
            "trs_id": str(o.trs_id),
            "trs_timestamp": str(o.trs_timestamp),
            "trs_from": o.trs_from.to_dict(),
            "trs_to": o.trs_to.to_dict(),
            "trs_amount": o.trs_amount,
        }

        return to_json