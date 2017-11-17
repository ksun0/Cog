from django.db import models
import uuid

class Extension(models.Model):
    '''
    Represents a flow of steps that comprise
    an extension.
    '''
    file_name = models.CharField(max_length=200)
    sidebar_name = models.CharField(max_length=200)
    extension_name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def json_encode(self):
        return {
                "Title": self.extension_name,
                "Description": self.description,
                "uuid": self.uuid
                }


# # In order to select steps of flow model, use below
# # select * from Dashboard_flowstep where model_id =27 order by step_number;
# class FlowModel(models.Model):
#     '''
#     Represents a flow of steps that comprise
#     an extension.
#     '''
#     file_name = models.CharField(max_length=200)
#     extension_name = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)
#     unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     def json_encode(self):
#         return {
#                 "Title": self.extension_name,
#                 "Description": self.description,
#                 "uuid": self.unique_id
#                 }

# class FlowInstance(models.Model):
#     step = models.IntegerField(default=0, null=False)
#     flow_model = models.ForeignKey(FlowModel, on_delete=models.CASCADE)

# class FlowStep(models.Model):
#     '''
#     A single step in an extension.
#     '''
#     function_name = models.CharField(max_length=200)
#     unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     model = models.ForeignKey(FlowModel)
#     step_number = models.IntegerField()
#     # In future create linked list for db scan optimization
#     # next_step = models.OneToOneField('self', on_delete=models.CASCADE, null=True)
