from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from activities.models import Activity
from projects.models import KeywordRank, KeywordRankResult

import time
import requests

from urllib.parse import urlparse

from seo import settings


class Command(BaseCommand):

    help = "Check 5 keyword ranks daily"

    def handle(self, *args, **kwargs):

        oldest_activity = (
            Activity.objects
            .filter(
                status="approved",
                rank_checked=False,
            )
            .order_by("date", "id")
            .first()
        )

        if not oldest_activity:
            self.stdout.write(
                self.style.SUCCESS(
                    "No pending keywords found"
                )
            )
            return

        target_date = oldest_activity.date

        all_activities = (
            Activity.objects
            .filter(
                status="approved",
                rank_checked=False,
                date=target_date,
            )
            .order_by("id")
        )

        selected_activities = []

        for activity in all_activities:

            data = activity.dynamic_data or {}

            keyword = data.get("Keyword")

            if not keyword:

                activity.rank_checked = True

                activity.rank_checked_at = timezone.now()

                activity.save(
                    update_fields=[
                        "rank_checked",
                        "rank_checked_at",
                    ]
                )

                continue

            selected_activities.append(activity)

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

                response = None

                for attempt in range(2):

                    try:

                        response = requests.post(
                            "https://api.apyhub.com/extract/serp/rank?location=in&language=en",
                            headers={
                                "apy-token": settings.APYHUB_API_KEY,
                                "Content-Type": "application/json",
                            },
                            json={
                                "keyword": keyword,
                            },
                            timeout=60,
                        )

                        response.raise_for_status()

                        break

                    except requests.exceptions.Timeout:

                        print(
                            f"{keyword} -> "
                            f"Timeout "
                            f"(Attempt {attempt + 1})"
                        )

                        if attempt == 0:

                            time.sleep(2)

                            continue

                        raise

                if response is None:

                    print(
                        f"{keyword} -> "
                        f"No API Response"
                    )

                    continue

                print(
                    "STATUS:",
                    response.status_code,
                )

                print(
                    "BODY:",
                    response.text,
                )

                api_data = response.json()

                if (
                    not api_data
                    or "error" in api_data
                    or not api_data.get("data")
                ):

                    print(
                        f"{keyword} -> "
                        f"Invalid API Response"
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

                serp_results = []

                for item in api_data.get("data", []):

                    serp_results.append(item)

                    result_url = item.get(
                        "url",
                        "",
                    )

                    if (
                        rank_found is None
                        and result_url
                    ):

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

                final_rank = (
                    rank_found
                    if rank_found is not None
                    else 999
                )

                found = (
                    rank_found is not None
                )

                with transaction.atomic():

                    keyword_rank, created = (
                        KeywordRank.objects
                        .update_or_create(
                            activity=activity,
                            defaults={
                                "project": activity.project,
                                "keyword": keyword,
                                "website": website,
                                "rank": final_rank,
                                "found": found,
                                "ranking_url": ranking_url,
                                "api_response": api_data,
                            },
                        )
                    )

                    KeywordRankResult.objects.filter(
                        keyword_rank=keyword_rank
                    ).delete()

                    result_objs = []

                    for item in serp_results:

                        result_objs.append(
                            KeywordRankResult(
                                keyword_rank=keyword_rank,
                                serp_rank=item.get(
                                    "rank"
                                ),
                                result_type=item.get(
                                    "type",
                                    "",
                                ),
                                title=item.get(
                                    "title",
                                    "",
                                ),
                                description=item.get(
                                    "description",
                                    "",
                                ),
                                domain=item.get(
                                    "domain",
                                    "",
                                ),
                                url=item.get(
                                    "url",
                                    "",
                                ),
                                breadcrumb=item.get(
                                    "breadcrumb",
                                    "",
                                ),
                            )
                        )

                    if result_objs:

                        KeywordRankResult.objects.bulk_create(
                            result_objs
                        )

                    activity.rank_checked = True

                    activity.rank_checked_at = (
                        timezone.now()
                    )

                    activity.last_rank = final_rank

                    activity.save(
                        update_fields=[
                            "rank_checked",
                            "rank_checked_at",
                            "last_rank",
                        ]
                    )

                print(
                    f"{activity.project.name} | "
                    f"{keyword} -> "
                    f"{final_rank}"
                )

            except requests.exceptions.Timeout:

                print(
                    f"{keyword} -> "
                    f"API Timeout"
                )

                continue

            except requests.exceptions.RequestException as e:

                print(
                    f"{keyword} -> "
                    f"API Error: {str(e)}"
                )

                continue

            except Exception as e:

                print(
                    f"{keyword} -> "
                    f"Error: {type(e).__name__}: "
                    f"{str(e)}"
                )

                continue

        self.stdout.write(
            self.style.SUCCESS(
                "Daily rank check completed"
            )
        )