from django.shortcuts import render

def happy_new_year(req):
    return render(req, 'happyNewYear/happyNewYear.html')