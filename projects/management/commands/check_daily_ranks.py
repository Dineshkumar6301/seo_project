from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from activities.models import Activity
from projects.models import KeywordRank, KeywordRankResult

import time
import requests

from urllib.parse import urlparse

from django.conf import settings


class Command(BaseCommand):

    help = "Check 5 keyword ranks daily using SerpApi"

    def handle(self, *args, **kwargs):

        # ---------------------------------------------------------
        # GET OLDEST UNCHECKED APPROVED ACTIVITY
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # GET ACTIVITIES FOR SAME DATE
        # ---------------------------------------------------------

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

            keyword = (
                data.get("Keyword")
                or data.get("keyword")
            )

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

        # ---------------------------------------------------------
        # CHECK KEYWORD RANK
        # ---------------------------------------------------------

        for activity in selected_activities:

            data = activity.dynamic_data or {}

            keyword = (
                data.get("Keyword")
                or data.get("keyword")
            )

            website = (
                data.get("Target_url")
                or data.get("target_url")
                or activity.project.client.website
            )

            try:

                if not settings.SERPAPI_API_KEY:

                    self.stdout.write(
                        self.style.ERROR(
                            "SERPAPI_API_KEY is missing"
                        )
                    )

                    return

                # -------------------------------------------------
                # CALL SERPAPI
                # -------------------------------------------------

                response = None

                for attempt in range(2):

                    try:

                        response = requests.get(
                            "https://serpapi.com/search.json",
                            params={
                                "engine": "google",
                                "q": keyword,
                                "google_domain": "google.co.in",
                                "gl": "in",
                                "hl": "en",
                                "num": 100,
                                "api_key": settings.SERPAPI_API_KEY,
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

                # -------------------------------------------------
                # PARSE SERPAPI RESPONSE
                # -------------------------------------------------

                api_data = response.json()

                if api_data.get("error"):

                    print(
                        f"{keyword} -> "
                        f"SerpApi Error: "
                        f"{api_data.get('error')}"
                    )

                    continue

                serp_results = api_data.get(
                    "organic_results",
                    [],
                )

                if not serp_results:

                    print(
                        f"{keyword} -> "
                        f"No Organic Results"
                    )

                    continue

                # -------------------------------------------------
                # CLEAN TARGET DOMAIN
                # -------------------------------------------------

                website_value = str(
                    website or ""
                ).strip()

                if not website_value:

                    print(
                        f"{keyword} -> "
                        f"Website Missing"
                    )

                    continue

                if not website_value.startswith(
                    (
                        "http://",
                        "https://",
                    )
                ):

                    website_value = (
                        "https://"
                        + website_value
                    )

                domain = (
                    urlparse(website_value)
                    .netloc
                    .replace("www.", "")
                    .lower()
                    .split(":")[0]
                )

                if not domain:

                    print(
                        f"{keyword} -> "
                        f"Invalid Website: {website}"
                    )

                    continue

                # -------------------------------------------------
                # FIND DOMAIN RANK
                # -------------------------------------------------

                rank_found = None

                ranking_url = None

                for item in serp_results:

                    result_url = item.get(
                        "link",
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
                            .split(":")[0]
                        )

                        if (
                            result_domain == domain
                            or result_domain.endswith(
                                "." + domain
                            )
                        ):

                            rank_found = item.get(
                                "position"
                            )

                            ranking_url = result_url

                            break

                # -------------------------------------------------
                # FINAL RANK
                # -------------------------------------------------

                final_rank = (
                    rank_found
                    if rank_found is not None
                    else 999
                )

                found = (
                    rank_found is not None
                )

                # -------------------------------------------------
                # DATABASE TRANSACTION
                # -------------------------------------------------

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

                    # ---------------------------------------------
                    # DELETE OLD RESULTS
                    # ---------------------------------------------

                    KeywordRankResult.objects.filter(
                        keyword_rank=keyword_rank
                    ).delete()

                    # ---------------------------------------------
                    # CREATE SERP RESULTS
                    # ---------------------------------------------

                    result_objs = []

                    for item in serp_results:

                        result_url = item.get(
                            "link",
                            "",
                        )

                        result_domain = ""

                        if result_url:

                            result_domain = (
                                urlparse(result_url)
                                .netloc
                                .replace("www.", "")
                                .lower()
                            )

                        result_objs.append(
                            KeywordRankResult(
                                keyword_rank=keyword_rank,

                                serp_rank=item.get(
                                    "position"
                                ),

                                result_type="organic",

                                title=item.get(
                                    "title",
                                    "",
                                ),

                                description=item.get(
                                    "snippet",
                                    "",
                                ),

                                domain=result_domain,

                                url=result_url,

                                breadcrumb=item.get(
                                    "displayed_link",
                                    "",
                                ),
                            )
                        )

                    if result_objs:

                        KeywordRankResult.objects.bulk_create(
                            result_objs
                        )

                    # ---------------------------------------------
                    # UPDATE ACTIVITY
                    # ---------------------------------------------

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

                # -------------------------------------------------
                # PRINT RESULT
                # -------------------------------------------------

                if found:

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{activity.project.name} | "
                            f"{keyword} -> "
                            f"RANK {final_rank}"
                        )
                    )

                else:

                    self.stdout.write(
                        self.style.WARNING(
                            f"{activity.project.name} | "
                            f"{keyword} -> "
                            f"NOT FOUND (999)"
                        )
                    )

            # -----------------------------------------------------
            # ERRORS
            # -----------------------------------------------------

            except requests.exceptions.Timeout:

                print(
                    f"{keyword} -> "
                    f"SerpApi Timeout"
                )

                continue

            except requests.exceptions.HTTPError as e:

                status_code = (
                    e.response.status_code
                    if e.response is not None
                    else "UNKNOWN"
                )

                response_text = (
                    e.response.text
                    if e.response is not None
                    else str(e)
                )

                print(
                    f"{keyword} -> "
                    f"SerpApi HTTP Error "
                    f"{status_code}: "
                    f"{response_text[:500]}"
                )

                continue

            except requests.exceptions.RequestException as e:

                print(
                    f"{keyword} -> "
                    f"SerpApi Request Error: "
                    f"{str(e)}"
                )

                continue

            except Exception as e:

                print(
                    f"{keyword} -> "
                    f"Error: "
                    f"{type(e).__name__}: "
                    f"{str(e)}"
                )

                continue

        self.stdout.write(
            self.style.SUCCESS(
                "Daily rank check completed"
            )
        )