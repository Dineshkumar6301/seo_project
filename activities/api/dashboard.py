from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q, Count
from django.db.models.functions import TruncDate

from activities.models import Activity


class ClientDashboardAPI(APIView):

    def get(self, request):

        qs = Activity.objects.all()

        # =====================================
        # CLIENT FILTER
        # =====================================
        if hasattr(request.user, "client"):

            qs = qs.filter(
                project__client=request.user.client
            )

        # =====================================
        # PAGINATION
        # =====================================
        try:

            page = max(
                1,
                int(request.GET.get("page", 1))
            )

            limit = min(
                50,
                max(
                    1,
                    int(request.GET.get("limit", 10))
                )
            )

        except (ValueError, TypeError):

            page = 1
            limit = 10

        # =====================================
        # FILTERS
        # =====================================
        filter_type = request.GET.get(
            "type",
            ""
        ).strip()

        start_date = request.GET.get(
            "start_date",
            ""
        ).strip()

        end_date = request.GET.get(
            "end_date",
            ""
        ).strip()

        search = request.GET.get(
            "search",
            ""
        ).strip()

        service = request.GET.get(
            "service",
            ""
        ).strip()

        status = request.GET.get(
            "status",
            ""
        ).strip()

        project = request.GET.get(
            "project",
            ""
        ).strip()

        today = now().date()

        # =====================================
        # DATE FILTERS
        # =====================================
        if start_date and end_date:

            qs = qs.filter(
                date__range=[
                    start_date,
                    end_date
                ]
            )

        elif filter_type == "today":

            qs = qs.filter(
                date=today
            )

        elif filter_type == "month":

            qs = qs.filter(
                date__month=today.month,
                date__year=today.year
            )
        elif filter_type == "week":

            start_week = today - timedelta(days=today.weekday())

            end_week = start_week + timedelta(days=6)

            qs = qs.filter(
                date__range=[start_week, end_week]
            )
        elif filter_type == "year":

            qs = qs.filter(
                date__year=today.year
            )

    
        if search:

            search = search.strip()

            qs = qs.filter(

                Q(user__email__icontains=search)

                |

                Q(user__first_name__icontains=search)

                |

                Q(user__last_name__icontains=search)

                |

                Q(project__name__icontains=search)

                |

                Q(category__icontains=search)

                |

                Q(service_name__icontains=search)

                |

                Q(task_type__icontains=search)

            )

        # =====================================
        # PROJECT
        # =====================================
        if project:

            qs = qs.filter(
                project__id=project
            )

        # =====================================
        # SERVICE
        # =====================================
        if service:

            qs = qs.filter(
                service_name__iexact=service
            )

        # =====================================
        # KPI BASE QUERY
        # =====================================
        base_qs = qs

        total = base_qs.count()

        approved = base_qs.filter(
            status="approved"
        ).count()

        pending = base_qs.filter(
            status="pending"
        ).count()

        rejected = base_qs.filter(
            status="rejected"
        ).count()


        chart_qs = (

            base_qs

            .annotate(
                day=TruncDate("date")
            )

            .values("day")

            .annotate(
                count=Count("id")
            )

            .order_by("day")
        )

        chart_labels = [
            str(row["day"])
            for row in chart_qs
        ]

        chart_data = [
            row["count"]
            for row in chart_qs
        ]

        # =====================================
        # STATUS FILTER
        # =====================================
        if status:

            qs = qs.filter(
                status=status
            )

        qs = qs.order_by("-date")

     
        total_count = qs.count()

        start = (page - 1) * limit

        end = start + limit

        total_pages = max(
            1,
            (total_count + limit - 1) // limit
        )


        table = list(

            qs.values(

                "id",

                "category",

                "service_name",

                "task_type",

                "status",

                "date",

                "dynamic_data",

                "project__name",

                "user__first_name",

                "user__last_name",

            )[start:end]

        )
        # =====================================
        # FORMAT TABLE DATA
        # =====================================

        for row in table:

            dynamic_data = (
                row.get("dynamic_data")
                or {}
            )

            # FRONTEND SUPPORT
            row["data"] = dynamic_data

            # =================================
            # PROOF LINKS
            # =================================
            row["SUBMITTED_URL"] = (

                dynamic_data.get(
                    "submitted_url"
                )

                or

                dynamic_data.get(
                    "SUBMITTED_URL"
                )

                or

                dynamic_data.get(
                    "proof_links"
                )

                or

                ""
            )

        # =================================
        # DATE FORMAT
        # =================================
        if row.get("date"):

            row["date"] = str(
                row["date"]
            )
            
        return Response({

            "kpi": {

                "total": total,

                "approved": approved,

                "pending": pending,

                "rejected": rejected,

            },

            "chart": {

                "labels": chart_labels,

                "data": chart_data,

            },

            "table": table,

            "pagination": {

                "page": page,

                "pages": total_pages,

            },

        })