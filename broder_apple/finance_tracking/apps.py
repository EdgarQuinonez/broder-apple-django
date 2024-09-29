from django.apps import AppConfig


class FinanceTrackingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "finance_tracking"

    def ready(self):
        import finance_tracking.signals
