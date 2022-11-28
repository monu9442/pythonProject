from api_tester import update_recruiter_dict

recruiter_dict = {"a":False, "b":True, "c":False}

update_recruiter_dict(["a","b"], "deny", recruiter_dict)

print(recruiter_dict)
