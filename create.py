from openpyxl import Workbook
from projects.models import  Service, ChecklistTemplate,ServiceCategory

wb = Workbook()
ws = wb.active
ws.title = "Service Checklist Master"

ws.append([
    "Category",
    "Service",
    "Task Type",
    "Fill Details",
    "Checklist Tasks"
])

for category in ServiceCategory.objects.all():

    for service in category.services.all():

        checklists = ChecklistTemplate.objects.filter(
            module__service=service
        ).order_by(
            "module__name",
            "order"
        )

        for checklist in checklists:

            ws.append([
                category.name,
                service.name,
                checklist.module.name,
                "",
                checklist.item
            ])

wb.save("service_checklist_master.xlsx")

print("Excel exported successfully")