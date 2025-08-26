from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from saas import models
from automation import utils


@receiver(post_save, sender=models.Subscription)
def handle_subscription_save(sender, instance, created, **kwargs):
    try:
        # TODO: it will move to post method
        workflow = instance.service.workflow
        workflow["name"] = instance.service.name+"---"+instance.created_by.username
        if created:
            response = utils.create_workflow(workflow)
            instance.workflow_id = response.get("id")
            instance.save(update_fields=["workflow_id"])
            return

        if not created:
            if instance.status == models.Status.CONFIRMED and instance.workflow_id:
                utils.active_workflow(instance.workflow_id)

            elif instance.status in (models.Status.CANCELLED, models.Status.PENDING) and instance.workflow_id:
                utils.deactivate_workflow(instance.workflow_id)

    except Exception as e:
        print(f"❌ Subscription workflow sync failed: {e}")


@receiver(pre_delete, sender=models.Subscription)
def handle_subscription_delete(sender, instance, **kwargs):
    try:
        if instance.workflow_id:
            utils.delete_workflow(instance.workflow_id)
        print("deleted subscription")
    except Exception as e:
        print(f"❌ Failed to delete workflow {instance.workflow_id} from automation: {e}")
