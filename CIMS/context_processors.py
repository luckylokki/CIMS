from inventory.models import MainDomain
def domain(request):
    domain = MainDomain.objects.all()
    return {"domain": domain}