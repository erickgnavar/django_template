from django.shortcuts import render
from django.views import generic


class HomeView(generic.TemplateView):

    template_name = "pages/home.html"


def contact(request):
    return render(request, "pages/contact.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def cookies(request):
    return render(request, "pages/cookies.html")


def faq(request):
    return render(request, "pages/faq.html")
