from django.core.management.base import BaseCommand
from projects.models import (
Service,
ServiceModule,
ChecklistTemplate
)

CHECKLISTS = {


"SEO - ON PAGE": {

    "Audit": [
        "Website Audit",
        "Competitor Analysis",
        "Keyword Mapping",
        "Technical SEO Audit",
    ],

    "On Page Optimization": [
        "Title Tag Optimization",
        "Meta Description Optimization",
        "Heading Optimization",
        "Internal Linking",
        "Image Optimization",
        "Schema Implementation",
    ],

    "Reporting": [
        "Ranking Report",
        "Optimization Report",
    ]
},

"SEO - OFF PAGE": {

    "Backlinks": [
        "Profile Creation",
        "Directory Submission",
        "Citation Building",
        "Blog Comments",
        "Classified Submission",
        "Social Bookmarking",
    ],

    "Outreach": [
        "Guest Posting",
        "Blogger Outreach",
        "Link Outreach",
        "Article Submission",
    ],

    "Reporting": [
        "Backlink Report",
        "Authority Report",
    ]
},

"GMB MANAGEMENT": {

    "Setup": [
        "GBP Audit",
        "Business Information Review",
        "Category Optimization",
    ],

    "Optimization": [
        "Service Update",
        "Product Update",
        "Photo Upload",
        "Weekly Post Creation",
    ],

    "Reviews": [
        "Review Monitoring",
        "Review Response",
    ],

    "Reporting": [
        "GBP Insights Report",
    ]
},

"INSTAGRAM": {

    "Strategy": [
        "Competitor Research",
        "Content Calendar",
        "Hashtag Research",
    ],

    "Design": [
        "Post Design",
        "Story Design",
        "Reel Design",
    ],

    "Publishing": [
        "Post Upload",
        "Reel Upload",
        "Story Upload",
    ],

    "Reporting": [
        "Reach Report",
        "Engagement Report",
    ]
},

"FACEBOOK": {

    "Content": [
        "Post Design",
        "Caption Writing",
        "Hashtag Research",
    ],

    "Publishing": [
        "Post Publishing",
        "Story Publishing",
    ],

    "Engagement": [
        "Comment Monitoring",
        "Inbox Monitoring",
    ],

    "Reporting": [
        "Page Insights Report",
    ]
},

"LINKEDIN": {

    "Strategy": [
        "Industry Research",
        "Competitor Analysis",
    ],

    "Content": [
        "Thought Leadership Post",
        "Company Update Post",
    ],

    "Publishing": [
        "Post Publishing",
    ],

    "Reporting": [
        "LinkedIn Analytics",
    ]
},

"TWITTER": {

    "Research": [
        "Trending Topic Research",
        "Competitor Monitoring",
    ],

    "Content": [
        "Tweet Creation",
        "Thread Creation",
    ],

    "Publishing": [
        "Tweet Scheduling",
    ],

    "Reporting": [
        "Engagement Analysis",
    ]
},

"YOUTUBE": {

    "Research": [
        "Keyword Research",
        "Topic Research",
    ],

    "Production": [
        "Script Writing",
        "Thumbnail Design",
        "Video Editing",
    ],

    "Upload": [
        "Title Optimization",
        "Description Optimization",
        "Tags Optimization",
        "End Screen Setup",
    ],

    "Reporting": [
        "Watch Time Analysis",
        "Subscriber Growth",
    ]
},

"BLOGS": {

    "Research": [
        "Keyword Research",
        "Topic Research",
    ],

    "Writing": [
        "Blog Writing",
        "SEO Optimization",
    ],

    "Publishing": [
        "Upload Blog",
        "Internal Linking",
    ],

    "Reporting": [
        "Traffic Report",
    ]
},

"ARTICLES": {

    "Research": [
        "Topic Research",
        "Competitor Research",
    ],

    "Writing": [
        "Article Writing",
        "Article Editing",
    ],

    "Publishing": [
        "Upload Article",
    ],

    "Reporting": [
        "Performance Review",
    ]
},

"CONTENT": {

    "Planning": [
        "Content Strategy",
        "Keyword Research",
    ],

    "Creation": [
        "Content Drafting",
        "Content Review",
    ],

    "Distribution": [
        "Publish Content",
        "Share Content",
    ],

    "Reporting": [
        "Content Performance",
    ]
},

"PHOTOS": {

    "Planning": [
        "Shot Planning",
        "Location Planning",
    ],

    "Production": [
        "Photography",
        "Photo Editing",
        "Client Review",
    ],

    "Delivery": [
        "Final Export",
        "Delivery To Client",
    ]
},

"VIDEOS": {

    "Planning": [
        "Concept Planning",
        "Script Review",
    ],

    "Production": [
        "Video Shooting",
        "Video Editing",
        "Motion Graphics",
    ],

    "Delivery": [
        "Final Export",
        "Video Upload",
    ],

    "Reporting": [
        "Performance Review",
    ]
},
"GOOGLE ADS": {

    "Account Setup": [
        "Google Ads Access",
        "Analytics Linking",
        "Search Console Linking",
        "Tag Manager Linking",
    ],

    "Tracking": [
        "Conversion Setup",
        "Phone Call Tracking",
        "Form Tracking",
        "WhatsApp Tracking",
    ],

    "Campaign Setup": [
        "Keyword Research",
        "Audience Research",
        "Campaign Structure",
        "Ad Group Creation",
        "Ad Copy Creation",
        "Extensions Setup",
    ],

    "Optimization": [
        "Search Terms Review",
        "Negative Keywords",
        "Bid Optimization",
        "Audience Optimization",
        "Conversion Optimization",
        "Landing Page Review",
    ],

    "Reporting": [
        "Weekly Report",
        "Monthly Report",
    ]
},
"META ADS": {

    "Account Setup": [
        "Meta Business Manager Access",
        "Ad Account Access",
        "Pixel Access",
        "Domain Verification",
    ],

    "Tracking": [
        "Pixel Installation",
        "Conversion Events Setup",
        "CAPI Setup",
    ],

    "Campaign Setup": [
        "Audience Research",
        "Creative Upload",
        "Ad Copy Creation",
        "Campaign Launch",
    ],

    "Optimization": [
        "CTR Analysis",
        "CPA Analysis",
        "Audience Optimization",
        "Creative Testing",
        "Budget Optimization",
    ],

    "Reporting": [
        "Weekly Report",
        "Monthly Report",
    ]
},
"TECHNICAL SEO": {

    "Audit": [
        "Website Crawl Audit",
        "Index Coverage Audit",
        "Core Web Vitals Audit",
        "Mobile Usability Audit",
    ],

    "Technical Fixes": [
        "Robots.txt Review",
        "Sitemap Audit",
        "Canonical Audit",
        "Redirect Audit",
        "Broken Link Audit",
    ],

    "Monitoring": [
        "Search Console Errors",
        "Crawl Errors",
        "Index Monitoring",
    ],

    "Reporting": [
        "Technical SEO Report",
    ]
},
"Graphic Design": {

    "Design Request": [
        "Requirement Collection",
        "Reference Collection",
    ],

    "Design Creation": [
        "Social Media Post Design",
        "Banner Design",
        "Ad Creative Design",
        "Carousel Design",
        "Thumbnail Design",
    ],

    "Review": [
        "Internal Review",
        "Client Approval",
    ],

    "Delivery": [
        "Final Export",
        "Source File Delivery",
    ]
},
"LOCAL SEO": {

    "Audit": [
        "Local SEO Audit",
        "NAP Audit",
        "Competitor Analysis",
    ],

    "Optimization": [
        "Citation Building",
        "Local Keyword Optimization",
        "Location Page Optimization",
    ],

    "Reviews": [
        "Review Monitoring",
        "Review Response",
    ],

    "Reporting": [
        "Local Ranking Report",
    ]
},
"LANDING PAGE CONTENT": {

    "Research": [
        "Keyword Research",
        "Competitor Analysis",
    ],

    "Writing": [
        "Headline Writing",
        "Landing Page Copy Writing",
        "CTA Creation",
    ],

    "Optimization": [
        "SEO Optimization",
        "Conversion Optimization",
    ],

    "Review": [
        "Content Review",
        "Client Approval",
    ]
},
"WEBSITE CONTENT": {

    "Planning": [
        "Page Structure Planning",
        "Keyword Mapping",
    ],

    "Writing": [
        "Homepage Content",
        "Service Page Content",
        "About Us Content",
        "Contact Page Content",
    ],

    "Optimization": [
        "SEO Optimization",
        "Internal Linking",
    ],

    "Review": [
        "Content Review",
    ]
},
"WEBSITE DEVELOPMENT": {

    "Planning": [
        "Requirement Gathering",
        "Sitemap Creation",
        "Wireframe Creation",
    ],

    "Design": [
        "Homepage Design",
        "Inner Page Design",
        "Mobile Design",
    ],

    "Development": [
        "Frontend Development",
        "Backend Development",
        "CMS Setup",
    ],

    "Testing": [
        "Mobile Testing",
        "Speed Testing",
        "Cross Browser Testing",
    ],

    "Launch": [
        "DNS Configuration",
        "SSL Setup",
        "Analytics Setup",
        "Website Launch",
    ]
},
"LANDING PAGE DEVELOPMENT": {

    "Planning": [
        "Requirement Gathering",
        "Wireframe Creation",
    ],

    "Design": [
        "Landing Page Design",
    ],

    "Development": [
        "Page Development",
        "Form Integration",
        "Tracking Setup",
    ],

    "Testing": [
        "Mobile Testing",
        "Speed Testing",
    ],

    "Launch": [
        "Publish Landing Page",
    ]
},
"WEBSITE MAINTENANCE": {

    "Maintenance": [
        "Plugin Updates",
        "Theme Updates",
        "Security Check",
        "Backup Verification",
    ],

    "Monitoring": [
        "Uptime Monitoring",
        "Performance Monitoring",
    ],

    "Reporting": [
        "Maintenance Report",
    ]
},
"PINTREST": {

    "Research": [
        "Keyword Research",
        "Board Research",
    ],

    "Content": [
        "Pin Design",
        "Pin Description Writing",
    ],

    "Publishing": [
        "Pin Upload",
        "Board Optimization",
    ],

    "Reporting": [
        "Pinterest Analytics",
    ]
},

"Threads": {

    "Research": [
        "Trend Research",
        "Competitor Monitoring",
    ],

    "Content": [
        "Thread Creation",
        "Engagement Content",
    ],

    "Publishing": [
        "Thread Publishing",
    ],

    "Reporting": [
        "Threads Analytics",
    ]
},

"EMAIL MARKETING":{
    "Strategy" :[
        "Audience Segmentation",
        "Campaign Planning",

    ],

    "Content" :[
        "Subject Line Writing",
        "Email Copy Writing",
        "CTA Creation",

    ],

    "Setup" :[
        "Template Design",
        "Automation Setup",
        "List Management",
    ],

    "Optimization":[

        "Open Rate Analysis",
        "Click Rate Analysis",
        "A/B Testing",
    ],

    "Reporting":[

    
        "Campaign Report"
    ],
     

},


}

class Command(BaseCommand):


    help = "Seed Service Modules and Checklist Templates"

    def handle(self, *args, **kwargs):

        created_modules = 0
        created_checklists = 0

        for service_name, modules in CHECKLISTS.items():

            try:
                service = Service.objects.get(
                    name=service_name
                )

            except Service.DoesNotExist:

                self.stdout.write(
                    self.style.WARNING(
                        f"Service not found: {service_name}"
                    )
                )
                continue

            module_order = 1

            for module_name, tasks in modules.items():

                module, module_created = ServiceModule.objects.get_or_create(
                    service=service,
                    name=module_name,
                    defaults={
                        "order": module_order
                    }
                )

                if module_created:
                    created_modules += 1

                task_order = 1

                for task_name in tasks:

                    _, task_created = ChecklistTemplate.objects.get_or_create(
                        module=module,
                        item=task_name,
                        defaults={
                            "order": task_order
                        }
                    )

                    if task_created:
                        created_checklists += 1

                    task_order += 1

                module_order += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created_modules} modules and {created_checklists} checklist templates."
            )
        )




























