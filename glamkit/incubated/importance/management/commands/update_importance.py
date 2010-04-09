from django.db.models.loading import get_models
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Updates the importance of the models decorated with '@calculate_importance'"
    
    requires_model_validation = True
    can_import_settings = False
    
    def handle(self, **options):
        for model in get_models():
            if hasattr(model, "calculate_importance") and hasattr(model, "importance_field"):
                for obj in model.objects.all():
                    setattr(obj, model.importance_field, obj.calculate_importance())
                    obj.save()