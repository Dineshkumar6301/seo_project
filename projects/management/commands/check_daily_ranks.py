
from django.core.management.base import BaseCommand
from django.utils import timezone
from activities.models import Activity
from projects.models import (
    KeywordRank,
    KeywordRankResult
)

import requests
from urllib.parse import urlparse


class Command(BaseCommand):

    help = "Check 5 keyword ranks daily"

    def handle(self, *args, **kwargs):

        oldest_activity = Activity.objects.filter(
            status="approved",
            rank_checked=False
        ).order_by(
            "date",
            "id"
        ).first()

        if not oldest_activity:

            self.stdout.write(
                self.style.SUCCESS(
                    "No pending keywords found"
                )
            )
            return

        target_date = oldest_activity.date

        all_activities = Activity.objects.filter(
            status="approved",
            rank_checked=False,
            date=target_date
        ).order_by(
            "id"
        )

        selected_activities = []

        for activity in all_activities:

            data = activity.dynamic_data or {}

            keyword = data.get("Keyword")

            if not keyword:

                activity.rank_checked = True

                activity.save(
                    update_fields=[
                        "rank_checked"
                    ]
                )

                continue

            selected_activities.append(
                activity
            )

            if len(selected_activities) == 5:
                break

        if not selected_activities:

            self.stdout.write(
                self.style.SUCCESS(
                    "No valid keywords found"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Checking Date: {target_date}"
            )
        )

        for activity in selected_activities:

            data = activity.dynamic_data or {}

            keyword = data.get("Keyword")

            website = (
                data.get("Target_url")
                or activity.project.client.website
            )

            try:

                response = requests.post(
                    "https://api.apyhub.com/extract/serp/rank?location=in&language=en",
                    headers={
                        "apy-token": "APY0bkk9F6VgGb2oBgEQGKQTLnG0KL8MRwHb4NMzMoBhSonvORBfaPdRxtIcx4MRM",
                        "Content-Type": "application/json"
                    },
                    json={
                        "keyword": keyword
                    },
                    timeout=60
                )

                api_data = response.json()

                if "error" in api_data:

                    print(
                        f"API Error: {api_data.get('error')}"
                    )

                    continue

                domain = (
                    urlparse(website)
                    .netloc
                    .replace("www.", "")
                    .lower()
                )

                rank_found = None
                ranking_url = None

                keyword_rank = KeywordRank.objects.create(
                    project=activity.project,
                    activity=activity,
                    keyword=keyword,
                    website=website,
                    api_response=api_data
                )

                for item in api_data.get(
                    "data",
                    []
                ):

                    KeywordRankResult.objects.create(
                        keyword_rank=keyword_rank,
                        serp_rank=item.get(
                            "rank"
                        ),
                        result_type=item.get(
                            "type",
                            ""
                        ),
                        title=item.get(
                            "title",
                            ""
                        ),
                        description=item.get(
                            "description",
                            ""
                        ),
                        domain=item.get(
                            "domain",
                            ""
                        ),
                        url=item.get(
                            "url",
                            ""
                        ),
                        breadcrumb=item.get(
                            "breadcrumb",
                            ""
                        )
                    )

                    result_url = item.get(
                        "url",
                        ""
                    )

                    if not result_url:
                        continue

                    result_domain = (
                        urlparse(result_url)
                        .netloc
                        .replace("www.", "")
                        .lower()
                    )

                    if result_domain == domain:

                        rank_found = item.get(
                            "rank"
                        )

                        ranking_url = result_url

                keyword_rank.rank = (
                    rank_found
                    if rank_found
                    else 999
                )

                keyword_rank.found = (
                    rank_found is not None
                )

                keyword_rank.ranking_url = (
                    ranking_url
                )

                keyword_rank.save()

                activity.rank_checked = True

                activity.rank_checked_at = (
                    timezone.now()
                )

                activity.last_rank = (
                    rank_found
                    if rank_found
                    else 999
                )

                activity.save()

                print(
                    f"{activity.project.name} | "
                    f"{keyword} -> "
                    f"{rank_found if rank_found else 'Not Ranking'}"
                )

            except Exception as e:

                print(
                    f"{keyword} -> Error: {str(e)}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Daily rank check completed"
            )
        )