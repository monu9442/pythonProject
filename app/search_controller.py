import json
import copy
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, abort
from app.services.search.PaginatedSearch import PaginatedSearch
from app.services.search.BuildQuery import BuildQuery
from app.services.search.BuildResponse import Results
from app.validation.RequestParamValidation import RequestValidation
from app.validation.SearchQueryValidation import SearchQueryValidation
from utils.Logger import LoggerUtil
from utils.Mongo import mongo_util
from utils.DbConnect import DbConnect
from utils.common.CleanData import DataUtil

search_module = Blueprint('search', __name__)

recruiter_dict = DbConnect.get_recruiter_dict()

@search_module.route("/search", methods=["POST", "GET"])
def search():
    log_data = {}
    if request.method == "GET":
        return "Search_API takes POST requests. Thank You!"
    try:
        if not request.json:
            return jsonify(json.dumps("Empty Request Form")), 400
        form_data = validate_query(DataUtil.cleanData(request.json))
        form_data['is_aggregate_call'] = False
        # Don't add any code here. Any changes to the form data to be done in validate_query function.
        # Changing form data here will cause aggregations to break
        form_data["is_similar_profile_call"] = False
        all_resumes_query, express_resumes_query, synonyms_dict = BuildQuery.search_query(form_data)
        result, ex_resumes_ids, all_resumes_ids = Results.getSearchProfiles(express_resumes_query, all_resumes_query,
                                                                            form_data, synonyms_dict)
        result["synonyms"] = synonyms_dict.get("synonyms") if synonyms_dict.get("synonyms") else {}
        log_data["REQUEST_FORM"] = json.dumps(request.json)
        log_data["EXPRESS_RESUMES_QUERY"] = json.dumps(express_resumes_query)
        log_data["UNIQ_ID"] = form_data.get("uniq_id")
        log_data["SIG"] = form_data.get("sig")
        log_data["ALL_RESUMES_QUERY"] = json.dumps(all_resumes_query)
        log_data["synonyms"] = json.dumps(synonyms_dict)
        log_data["RESPONSE_STATUS"] = "Success"
        log_data["TOTAL_RESUMES_MATCHED"] = result["total_count"]
        LoggerUtil.logger.debug(log_data)
        #log_data["RESPONSE"] = (result)
        mongo_util.insert_data("polaris-search",log_data)
        return jsonify(result)
    except BadRequest as e:
        log_data["RESPONSE_STATUS"] = "Failure"
        graylog_msg = "API: search\n{}\nRequest Form: {}".format(e.description, json.dumps(request.json))
        log_data["Error"] = graylog_msg
        LoggerUtil.logger.error(log_data)
        mongo_util.insert_data("polaris-search", log_data)
        return jsonify(json.dumps(e.description)), 400
    except Exception as e:
        log_data["RESPONSE_STATUS"] = "Failure"
        graylog_msg = "API: search\n{}\nRequest Form: {}".format(e, json.dumps(request.json))
        log_data["Error"] = graylog_msg
        LoggerUtil.logger.error(log_data)
        mongo_util.insert_data("polaris-search", log_data)


@search_module.route("/aggregate", methods=["POST", "GET"])
def aggregate():
    if request.method == "GET":
        return "Search_API takes POST requests. Thank You!"
    log_data = {}
    try:
        if not request.json:
            return jsonify(json.dumps("Empty Request Form")), 400
        form_data = validate_query(DataUtil.cleanData(request.json))
        form_data['is_aggregate_call'] = True
        form_data["is_similar_profile_call"] = False
        all_resumes_query, express_resumes_query, synonyms_dict = BuildQuery.search_query(form_data)
        aggregate_query = BuildQuery.aggregate_query(all_resumes_query, form_data)
        # query result
        result = Results.get_aggreations(aggregate_query, form_data)
        # post processing
        response = Results.process_aggregation_result(result.get("aggregations"),form_data)
        log_data["REQUEST_FORM"] = json.dumps(request.json)
        log_data["ALL_RESUMES_QUERY"] = json.dumps(all_resumes_query)
        log_data["AGGREGATE_QUERY"] = json.dumps(aggregate_query)
        log_data["RESPONSE_STATUS"] = "Success"
        log_data["UNIQ_ID"] = form_data.get("uniq_id")
        log_data["RESULT_COUNT"] = response["count"]
        LoggerUtil.logger.debug(log_data)
        #log_data["RESPONSE"] = (response)
        mongo_util.insert_data("polaris-aggregate", log_data)
        return jsonify(response)
    except Exception as e:
        LoggerUtil.logger.error(e, exc_info=True)
        graylog_msg = "API: search\n{}\nRequest Form: {}".format(e, json.dumps(request.json))
        log_data["Error"] = graylog_msg
        mongo_util.insert_data("polaris-search", log_data)


@search_module.route("/paginated_search", methods=["POST", "GET"])
def paginated_search():
    if request.method == "GET":
        return "Search_API takes POST requests. Thank You!"
    try:
        if not request.json:
            return jsonify(json.dumps("Request Form is Empty !!!")), 400

        form_data = validate_query(DataUtil.cleanData(request.json))
        all_resumes_query, express_resumes_query, synonyms_dict = BuildQuery.search_query(form_data)
        #all_resumes_query_copy = copy.deepcopy(all_resumes_query)
        #count = PaginatedSearch.get_paginated_search_count(all_resumes_query_copy, form_data)
        response = PaginatedSearch.get_paginated_result(all_resumes_query, form_data)
        log_data = {
            "API": "paginated_search",
            "query": all_resumes_query,
            "form_data": form_data
        }
        LoggerUtil.logger.debug(log_data)
        return jsonify(response)
    except Exception as e:
        log_data = {
            "query": all_resumes_query,
            "form_data": form_data,
            "Exception": e
        }
        LoggerUtil.logger.error(e, exc_info=True)


def validate_query(form_data):
    is_validated, description = RequestValidation.validateSearchParams(form_data)
    if not is_validated:
        raise BadRequest(description)
    SearchQueryValidation.validate_queries(form_data.get("queries"))
    SearchQueryValidation.validate_filters(form_data.get("filters"))
    SearchQueryValidation.validate_filters(form_data.get("refine_search"))
    data = DataUtil.cleanData(form_data)
    if form_data.get("queries") is not None and form_data.get("queries").get("synonyms") is not None:
        data["queries"]["synonyms"] = form_data.get("queries").get("synonyms")
    return data


@search_module.route("/validate/boolean", methods=["GET"])
def validate_boolean():
    if request.method == "POST":
        return "Validate boolean takes GET requests. Thank You!"
    query = request.args.get('query')
    if not request.args.get('query'):
        abort(400, "Empty Request")
    brackets_balanced = Results.areBracketsBalanced(query)
    resp=Results.validate_boolean_query(query)

    if resp==400 or not brackets_balanced:
        return jsonify({'lenient':1})

    resp = Results.validate_boolean_query(query)
    if resp == 400:
        return jsonify({'lenient': 1})

    return jsonify({'lenient': 0})


@search_module.route("/update_rec_access", methods=["POST"])
def update_recruiter_dict():
    if request.method == "GET":
        return jsonify("This API takes only POST METHODS......THANK YOU!!!")
    try:
        form_data = DbConnect.get_processed_form_data(request.json)
        rec_ids = form_data.keys()
        access_change_data = DbConnect.get_access_change_data(form_data)
        success = DbConnect.update_db(access_change_data, rec_ids)
        recruiter_dict_status = DbConnect.update_rec_dict(form_data, recruiter_dict)
        LoggerUtil.logger.info(f"Recruiter Feature Access modified for following Recruiters : {rec_ids}......."
                               f"form_data : {form_data}")
        if success and recruiter_dict_status:
            return jsonify({"Action": "Update", "Status": "OK"})
        else:
            return jsonify({"Action": "Update", "Status": "API FAILED"})
    except Exception as E:
        return jsonify(f"Exception Occurred : {E}")


