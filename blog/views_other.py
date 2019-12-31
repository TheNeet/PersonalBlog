from django.shortcuts import render

def happy_new_year(req):
    return render(req, 'happyNewYear/happyNewYear.html')

def happy_new_yearLH(req):
    return render(req, 'happyNewYear/happyNewYearLH.html')