from Dashboard.Extensions.ExtensionLib.QAFramework import *
from .forms import *
import pdb
def main():
	request = yield
	yield ask(TestForm, 'form', request)
	request = yield
	print(request.response_data)
	