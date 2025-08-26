# routers.py
# class AutomateRouter:
#     route_app_labels = {"anutomation"}
#
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "automate"
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "automate"
#         return None
class AutomationRouter:
    app_label = "automation"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return "automate"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return "automate"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.app_label and obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Prevent migrations for automation app
        if app_label == self.app_label:
            return False
        return None
