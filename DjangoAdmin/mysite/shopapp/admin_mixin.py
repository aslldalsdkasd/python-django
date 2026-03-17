from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
import csv

class ExportAsCSVMixin:

    def export_as_csv(self, request: HttpRequest, queryset: QuerySet):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename= {meta}-csv"

        csv_writer = csv.writer(response)
        csv_writer.writerow(field_names)

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export to CSV"