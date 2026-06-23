from django.core.management.base import BaseCommand

from projects.models import ChecklistTemplate, TaskField

class Command(BaseCommand):


    help = "Create Task Fields"

    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting existing Task Fields...")

        TaskField.objects.all().delete()

        for checklist in ChecklistTemplate.objects.select_related(
            "module",
            "module__service"
        ):

            service = checklist.module.service.name.lower()
            module = checklist.module.name.lower()
            item = checklist.item.lower()

            fields = []


            if "report" in item or "analytics" in item or "analysis" in item:

                fields = [
                    ("Report URL", "report_url", "url"),
                    ("Summary", "summary", "textarea"),
                ]

          

            elif "review response" in item:

                fields = [
                    ("Review Reply", "review_reply", "textarea"),
                ]

         

            elif "review monitoring" in item:

                fields = [
                    ("Review URL", "review_url", "url"),
                    ("Review Content", "review_content", "textarea"),
                ]

          

            elif any(
                Keyword in item for Keyword in [
                    "Keyword research",
                    "competitor",
                    "topic research",
                    "audience research",
                    "trend research",
                    "industry research",
                    "board research",
                    "nap audit",
                    "local seo audit",
                ]
            ):

                fields = [
                    ("Keyword", "Keyword", "textarea"),
                    ("Research Notes", "research_notes", "textarea"),
                ]

            
            elif any(
                Keyword in item for Keyword in [
                    "writing",
                    "content",
                    "copy",
                    "headline",
                    "caption",
                    "subject line",
                    "cta",
                    "tweet creation",
                    "thread creation",
                ]
            ):

                fields = [
                    ("Title", "Title", "text"),
                    ("Content", "content", "textarea"),
                ]

           

            elif any(
                Keyword in item for Keyword in [
                    "design",
                    "thumbnail",
                    "creative",
                    "banner",
                    "carousel",
                ]
            ):

                fields = [
                    ("Submitted_url", "Submitted_url", "url"),
                    ("Notes", "notes", "textarea"),
                ]

            

            elif any(
                Keyword in item for Keyword in [
                    "video",
                    "photography",
                    "photo editing",
                    "motion graphics",
                    "video editing",
                    "video shooting",
                ]
            ):

                fields = [
                    ("Submitted URL", "Submitted_url", "url"),
                    ("Notes", "notes", "textarea"),
                ]

            

            elif any(
                Keyword in item for Keyword in [
                    "upload",
                    "publishing",
                    "publish",
                    "scheduling",
                    "launch",
                ]
            ):

                fields = [
                    ("Submitted URL", "Submitted_url", "url"),
                ]

          

            elif service == "seo - off page":

                fields = [
                    ("Keyword", "Keyword", "text"),
                    ("Target URL", "Target_url", "url"),
                    ("Submitted URL", "Submitted_url", "textarea"),
                ]

            

            elif service == "seo - on page":

                fields = [
                    ("Target URL", "Target_url", "url"),
                    ("Changes Made", "changes_made", "textarea"),
                ]

           

            elif service == "technical seo":

                fields = [
                    ("Target URL", "Target_url", "url"),
                    ("Issue Found", "issue_found", "textarea"),
                    ("Fix Applied", "fix_applied", "textarea"),
                ]

          

            elif service in ["google ads", "meta ads"]:

                fields = [
                    ("Campaign Name", "campaign_name", "text"),
                    ("Notes", "notes", "textarea"),
                ]

            

            elif service in [
                "website development",
                "landing page development"
            ]:

                fields = [
                    ("Page URL", "page_url", "url"),
                    ("Development Notes", "development_notes", "textarea"),
                ]

            
            elif service in [
                "website content",
                "landing page content"
            ]:

                fields = [
                    ("Title", "Title", "text"),
                    ("Content", "content", "textarea"),
                ]

           
            else:

                fields = [
                    ("Notes", "notes", "textarea"),
                ]

            for order, field in enumerate(fields, start=1):

                TaskField.objects.create(
                    checklist_template=checklist,
                    label=field[0],
                    field_name=field[1],
                    field_type=field[2],
                    required=True,
                    order=order
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Task Fields Created Successfully"
            )
        )





