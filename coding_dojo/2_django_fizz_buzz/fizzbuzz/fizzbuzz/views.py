from django.http import HttpResponse

def view_for_hg(request):
	return HttpResponse('Hello HanGi')
