import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from saas.models import Service


class Command(BaseCommand):
    help = 'Create n number of Service instances with realistic data'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Number of services to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing services before creating new ones',
        )

    def handle(self, *args, **options):
        count = options['count']

        if options['clear']:
            Service.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Cleared all existing services.')
            )

        service_templates = [
            {
                "name": "Facebook Post Automation",
                "description": "Automatically schedule and post content to Facebook pages with custom timing and engagement tracking.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "trigger", "name": "Schedule Trigger"},
                        {"id": 2, "type": "content_generation", "name": "Generate Content"},
                        {"id": 3, "type": "post", "name": "Post to Facebook"},
                        {"id": 4, "type": "analytics", "name": "Track Engagement"}
                    ],
                    "triggers": ["time_based", "content_ready"],
                    "settings": {
                        "max_posts_per_day": 5,
                        "preferred_times": ["09:00", "12:00", "17:00"],
                        "auto_hashtags": True
                    }
                }
            },
            {
                "name": "Instagram Story Publisher",
                "description": "Create and publish Instagram stories with automated templates, music, and branded overlays.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "template_selection", "name": "Select Template"},
                        {"id": 2, "type": "content_overlay", "name": "Add Content"},
                        {"id": 3, "type": "branding", "name": "Apply Branding"},
                        {"id": 4, "type": "publish", "name": "Publish Story"}
                    ],
                    "triggers": ["manual", "scheduled"],
                    "settings": {
                        "template_categories": ["business", "lifestyle", "promotional"],
                        "auto_music": True,
                        "brand_watermark": True
                    }
                }
            },
            {
                "name": "WhatsApp Business Automation",
                "description": "Send automated WhatsApp messages, handle customer inquiries, and manage business communications.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "message_queue", "name": "Queue Messages"},
                        {"id": 2, "type": "personalization", "name": "Personalize Content"},
                        {"id": 3, "type": "send", "name": "Send Messages"},
                        {"id": 4, "type": "response_tracking", "name": "Track Responses"}
                    ],
                    "triggers": ["customer_action", "time_based", "event_based"],
                    "settings": {
                        "message_templates": 15,
                        "auto_reply": True,
                        "business_hours_only": True,
                        "max_messages_per_contact": 3
                    }
                }
            },
            {
                "name": "Email Marketing Sequences",
                "description": "Create automated email campaigns with A/B testing, personalization, and advanced analytics.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "segmentation", "name": "Segment Audience"},
                        {"id": 2, "type": "template_selection", "name": "Choose Template"},
                        {"id": 3, "type": "personalization", "name": "Personalize Emails"},
                        {"id": 4, "type": "send", "name": "Send Campaign"},
                        {"id": 5, "type": "analytics", "name": "Analyze Performance"}
                    ],
                    "triggers": ["user_signup", "purchase", "abandoned_cart", "scheduled"],
                    "settings": {
                        "ab_testing": True,
                        "send_time_optimization": True,
                        "unsubscribe_handling": True,
                        "drip_campaigns": True
                    }
                }
            },
            {
                "name": "E-commerce Order Processing",
                "description": "Automate order fulfillment, inventory management, and customer notifications for online stores.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "order_validation", "name": "Validate Order"},
                        {"id": 2, "type": "inventory_check", "name": "Check Inventory"},
                        {"id": 3, "type": "payment_processing", "name": "Process Payment"},
                        {"id": 4, "type": "fulfillment", "name": "Fulfill Order"},
                        {"id": 5, "type": "notification", "name": "Notify Customer"}
                    ],
                    "triggers": ["new_order", "payment_received"],
                    "settings": {
                        "auto_inventory_reorder": True,
                        "shipping_integration": ["fedex", "ups", "dhl"],
                        "customer_notifications": True,
                        "fraud_detection": True
                    }
                }
            },
            {
                "name": "LinkedIn Content Scheduler",
                "description": "Schedule professional LinkedIn posts, articles, and engagement activities for business growth.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "content_planning", "name": "Plan Content"},
                        {"id": 2, "type": "professional_review", "name": "Review Content"},
                        {"id": 3, "type": "scheduling", "name": "Schedule Posts"},
                        {"id": 4, "type": "engagement", "name": "Track Engagement"}
                    ],
                    "triggers": ["content_ready", "optimal_time", "manual"],
                    "settings": {
                        "industry_hashtags": True,
                        "professional_tone_check": True,
                        "connection_targeting": True,
                        "analytics_reporting": True
                    }
                }
            },
            {
                "name": "Twitter Engagement Bot",
                "description": "Automatically engage with relevant tweets, follow users, and build your Twitter presence.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "content_discovery", "name": "Find Relevant Content"},
                        {"id": 2, "type": "engagement_scoring", "name": "Score Engagement Value"},
                        {"id": 3, "type": "automated_interaction", "name": "Like/Retweet/Reply"},
                        {"id": 4, "type": "follow_management", "name": "Manage Follows"}
                    ],
                    "triggers": ["keyword_mention", "hashtag_tracking", "user_activity"],
                    "settings": {
                        "daily_limits": {"likes": 100, "follows": 50, "replies": 20},
                        "keyword_filters": True,
                        "spam_detection": True,
                        "engagement_quality_check": True
                    }
                }
            },
            {
                "name": "YouTube Video Processor",
                "description": "Automatically upload, optimize, and promote YouTube videos with SEO and thumbnail generation.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "video_processing", "name": "Process Video"},
                        {"id": 2, "type": "thumbnail_generation", "name": "Generate Thumbnails"},
                        {"id": 3, "type": "seo_optimization", "name": "Optimize for SEO"},
                        {"id": 4, "type": "upload", "name": "Upload to YouTube"},
                        {"id": 5, "type": "promotion", "name": "Promote Video"}
                    ],
                    "triggers": ["video_ready", "scheduled_upload"],
                    "settings": {
                        "auto_thumbnails": True,
                        "seo_keywords": True,
                        "cross_platform_sharing": True,
                        "analytics_tracking": True,
                        "monetization_ready": True
                    }
                }
            },
            {
                "name": "Customer Support Chatbot",
                "description": "AI-powered chatbot that handles customer inquiries, tickets, and provides 24/7 support.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "message_analysis", "name": "Analyze Message"},
                        {"id": 2, "type": "intent_recognition", "name": "Recognize Intent"},
                        {"id": 3, "type": "response_generation", "name": "Generate Response"},
                        {"id": 4, "type": "escalation_check", "name": "Check for Escalation"},
                        {"id": 5, "type": "ticket_creation", "name": "Create Ticket if Needed"}
                    ],
                    "triggers": ["customer_message", "support_request"],
                    "settings": {
                        "ai_confidence_threshold": 0.8,
                        "human_handoff": True,
                        "multilingual_support": ["en", "es", "fr"],
                        "sentiment_analysis": True,
                        "knowledge_base_integration": True
                    }
                }
            },
            {
                "name": "Inventory Management System",
                "description": "Track inventory levels, automate reordering, and manage supplier communications.",
                "workflow": {
                    "steps": [
                        {"id": 1, "type": "stock_monitoring", "name": "Monitor Stock Levels"},
                        {"id": 2, "type": "reorder_calculation", "name": "Calculate Reorder Points"},
                        {"id": 3, "type": "supplier_communication", "name": "Contact Suppliers"},
                        {"id": 4, "type": "order_placement", "name": "Place Orders"},
                        {"id": 5, "type": "delivery_tracking", "name": "Track Deliveries"}
                    ],
                    "triggers": ["low_stock", "scheduled_check", "supplier_update"],
                    "settings": {
                        "reorder_automation": True,
                        "supplier_integration": True,
                        "demand_forecasting": True,
                        "cost_optimization": True,
                        "multi_warehouse_support": True
                    }
                }
            }
        ]

        created_services = []

        for i in range(count):

            if i < len(service_templates):
                template = service_templates[i]
            else:

                base_template = random.choice(service_templates)
                template = {
                    "name": f"{base_template['name']} v{random.randint(2, 5)}",
                    "description": f"Enhanced version: {base_template['description']}",
                    "workflow": base_template['workflow'].copy()
                }

                template['workflow']['version'] = f"v{random.randint(2, 5)}.{random.randint(0, 9)}"
                template['workflow']['last_updated'] = timezone.now().isoformat()

            try:
                service = Service.objects.create(
                    name=template['name'],
                    description=template['description'],
                    workflow=template['workflow']
                )
                created_services.append(service)

                if random.choice([True, False]):
                    random_days = random.randint(1, 30)
                    service.created_at = timezone.now() - timezone.timedelta(days=random_days)
                    service.save()

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating service {i + 1}: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(created_services)} services!')
        )

        if created_services:
            self.stdout.write('\nCreated services:')
            for service in created_services[:5]:
                self.stdout.write(f'  • {service.name}')

            if len(created_services) > 5:
                self.stdout.write(f'  ... and {len(created_services) - 5} more')

            self.stdout.write(f'\nTotal services in database: {Service.objects.count()}')
