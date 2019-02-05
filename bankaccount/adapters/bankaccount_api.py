import uuid
import datetime
import json
from flask import Blueprint, request, Response
from bankaccount.adapters.orm import SqlAlchemy
from bankaccount.serializers import (account_serializer as acc_ser, transfer_serializer as trs_ser)  
from bankaccount.usecases import (request_objects as req, response_objects as resp,
                                transfer_usecases as trs_uc, account_usecases as acc_uc)
from bankaccount.repositories import db_uow, db_repo_transfer as repo_trs


STATUS_CODES = {
    resp.ResponseSuccess.SUCCESS: 200,
    resp.ResponseFailure.RESOURCE_ERROR: 404,
    resp.ResponseFailure.PARAMETERS_ERROR: 400,
    resp.ResponseFailure.SYSTEM_ERROR: 500
}


db = SqlAlchemy('sqlite:///bankaccount.db')
db.configure_mappings()
db.create_schema()


blueprint = Blueprint('bankaccount', __name__)

@blueprint.route('/transfers', methods=['GET'])
def transfers_histo():
    filter_params = {'filters':{}}
    for arg, value in request.args.items():
        if arg.startswith('filter_'):
            filter_params['filters'][arg.replace('filter_', '')] = value

    req_object = req.TransferHistoRequest.from_dict(filter_params)
    session = db.get_session()
    repo = repo_trs.DbRepoTrs(session)
    usecase = trs_uc.TransferHistoryUseCase(repo)

    resp_object = usecase.execute(req_object)

    return Response(json.dumps(resp_object.value, cls=trs_ser.TransferEncoder),
                    mimetype='application/json',
                    status=STATUS_CODES[resp_object.type])


@blueprint.route('/transfer', methods = ['POST'])
def transfer_create():
    if request.headers['Content-Type'] != 'application/json':
        return Response(json.dumps({'message':'content type must be json'}),
                    mimetype='application/json',
                    status=STATUS_CODES[resp.ResponseFailure.PARAMETERS_ERROR])
    else:
        id = uuid.uuid4()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_req = request.json
        trs = {'id':str(id),'timestamp':timestamp, 'from':json_req['from'], 'to':json_req['to'], 'amount':json_req['amount']}
        req_object = req.TransferAmountRequest(trs=trs)
        uowm = db.unit_of_work_manager
        usecase = trs_uc.TransferAmountUseCase(uowm)

        resp_object = usecase.execute(req_object)

        return Response(json.dumps(resp_object.value, cls=trs_ser.TransferEncoder),
                        mimetype='application/json',
                        status=STATUS_CODES[resp_object.type])



@blueprint.route('/account', methods = ['POST'])
def account_create():
    if request.headers['Content-Type'] != 'application/json':
        return Response(json.dumps({'message':'content type must be json'}),
                    mimetype='application/json',
                    status=STATUS_CODES[resp.ResponseFailure.PARAMETERS_ERROR])
    else:
        req_object = req.AccountOperationRequest(account=request.json)
        uowm = db.unit_of_work_manager
        usecase = acc_uc.AccountCreationUseCase(uowm)

        resp_object = usecase.execute(req_object)

        return Response(json.dumps(resp_object.value, cls=acc_ser.AccountEncoder),
                        mimetype='application/json',
                        status=STATUS_CODES[resp_object.type])


@blueprint.route('/account-deposit', methods = ['PUT'])
def account_deposit():
    if request.headers['Content-Type'] != 'application/json':
        return Response(json.dumps({'message':'content type must be json'}),
                    mimetype='application/json',
                    status=STATUS_CODES[resp.ResponseFailure.PARAMETERS_ERROR])
    else:
        req_object = req.AccountOperationRequest(account=request.json)
        uowm = db.unit_of_work_manager
        usecase = acc_uc.AccountDepositUseCase(uowm)

        resp_object = usecase.execute(req_object)

        return Response(json.dumps(resp_object.value, cls=acc_ser.AccountEncoder),
                        mimetype='application/json',
                        status=STATUS_CODES[resp_object.type])


@blueprint.route('/account-withdraw', methods = ['PUT'])
def account_withdraw():
    if request.headers['Content-Type'] != 'application/json':
        return Response(json.dumps({'message':'content type must be json'}),
                    mimetype='application/json',
                    status=STATUS_CODES[resp.ResponseFailure.PARAMETERS_ERROR])
    else:
        req_object = req.AccountOperationRequest(account=request.json)
        uowm = db.unit_of_work_manager
        usecase = acc_uc.AccountWithdrawUseCase(uowm)

        resp_object = usecase.execute(req_object)

        return Response(json.dumps(resp_object.value, cls=acc_ser.AccountEncoder),
                        mimetype='application/json',
                        status=STATUS_CODES[resp_object.type])