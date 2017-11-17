from django.core.management.base import BaseCommand, CommandError
import os
from Dashboard.models import *
from tqdm import tqdm
import pdb
import sys
from importlib import import_module

class Command(BaseCommand):
	help = 'Migrate all the Dashboard extensions.'
	def getSideBarName(self, sbname):
		# To-Do; come up with cleaner solution
		return os.path.exists(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))+'/'+sbname.replace('.','/')+'.py')

	def handle(self, *args, **options):
		### Clear the tables.
		Extension.objects.all().delete()
		path = "Dashboard/Extensions/"
		for extension in tqdm([x for x in os.listdir(path) if os.path.isdir(path+x)]):
			if extension[0] != "_" and extension != "ExtensionLib":
				init_f = "Dashboard/Extensions/"+extension+"/__init__.py"
				if not os.path.exists(init_f):
					open(init_f, 'a').close()
				# if os.path.exists("Dashboard.Extensions."+extension+".config"):
				config="Dashboard.Extensions."+extension+".config"
				fname="Dashboard.Extensions."+extension+".main"
				sbname = "Dashboard.Extensions."+extension+".sidebar"
				if not self.getSideBarName(sbname):
					sbname = ''
				config = import_module(config)
				model = Extension(file_name=fname, extension_name=config.name, description=config.description, sidebar_name=sbname)
				model.save()
			# previous_step = None
			# for i in range(len(steps)):
			# 	step = steps[i]
			# 	step = FlowStep(function_name=step.__name__, model=model, step_number=i)
			# 	if previous_step != None:
			# 		previous_step.next_step = step
			# 	step.save()
			# 	# previous_step.save()