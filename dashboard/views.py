from django.shortcuts import render


def demo(request):

    return render(request, 'dashboard/auxiliary/demo.html', {})
