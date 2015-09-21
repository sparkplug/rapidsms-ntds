if ntd_location.exists():

    report=NTDReport.objects.create(reporter=reporter)
    report.parish = ntd_location[0].location
    report.treated_lt_6_male_trac = int(values['Treated Less Than 6 Months male'])
    report.treated_lt_6_female_trac = int(values['Treated Less Than 6 Months female'])
    report.treated_6_to_4_male_trac = int(values['Treated 6 Months to 4 years male'])
    report.treated_6_to_4_female_trac = int(values['Treated 6 Months to 4 years female'])
    report.treated_4_to_14_male_trac = int(values['Treated 5 to 14 male'])
    report.treated_4_to_14_female_trac = int(values['Treated 5 to 14 female'])
    report.treated_gt_14_male_trac = int(values['Treated greater than 15 male'])
    report.treated_gt_14_female_trac = int(values['Treated greater than 15 female'])
    report.trachoma=int(values['Treated 6 Months to 4 years female'])+int(values['Treated 6 Months to 4 years male'])+int(values['Treated Less Than 6 Months male'])+int(values['Treated Less Than 6 Months female'])+int(values['Treated 5 to 14 male'])+int(values['Treated 5 to 14 female'])+int(values['Treated greater than 15 male'])+int(values['Treated greater than 15 female'])
    report.save()
else:
    submission.response = "Invalid location code"
    submission.has_errors = True
    submission.save()
    return