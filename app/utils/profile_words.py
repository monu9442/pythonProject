from app.utils.es_results import es_result

profile_dicts = []

for result in es_result['hits']['hits']:
    temp = dict()
    profile = result['_source']
    id = profile.get("profile_id", None)
    skills = profile.get("skills",None)
    designation = profile.get("current_employment").get("designation", None)
    employer = profile.get("current_employment").get("employer", None)
    if id and skills and designation and employer:
        temp["id"] = id
        temp["skills"] = skills
        temp["designation"] = designation
        temp["company"] = employer
        profile_dicts.append(temp)


