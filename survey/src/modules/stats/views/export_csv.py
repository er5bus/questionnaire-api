import io
import csv
from flask import make_response
from ....tools.views import generics
from .. import queries


class ExportCSVView(generics.RetrieveAPIView):
    route_path = "/export/csv/<int:department_id>"
    route_name = "export_csv"

    def get(self, **kwargs):
        department_id = kwargs.get("department_id")
        rows = queries.get_all_questions_by_department(department_id) or []
        
        si = io.StringIO()
        fieldnames = ["employee_id", "employee_email", "category", "category_score", 
                      "question", "answer", "area", "question_score"]
        writer = csv.DictWriter(si, delimiter=',', dialect='excel', fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=department-{}.csv".format(department_id)
        output.headers["Content-type"] = "text/csv"
        return output
