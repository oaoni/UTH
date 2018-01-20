from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

# Create your views here.

from . import gene
from . import searchform


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def search(request):
    message = 'No results'
    print('request:', request)
    print('request.method:', request.method)
# if this is a POST request we need to process the form data
    if ('q' in request.GET):
        query = gene.format_query(request.GET['q'])
        print('query:', query)
        genes = gene.get_genes(query)
        if (genes):
            message = str(genes)

    elif (request.method == 'POST'):
        # create a form instance and populate it with data from the request:
        print(request.POST)
        form = searchform.SearchForm(request.POST)
        message = "message: " + str(request.POST)[4:]
        print(message)
        # check whether it's valid:
        if form.is_valid():
            sel1 = form.cleaned_data['sel1']
            sel2 = form.cleaned_data['sel2']
            nci_data = form.cleaned_data['inlineCheckbox1']
            local_data = form.cleaned_data['inlineCheckbox2']
            pubmed_data = form.cleaned_data['inlineCheckbox3']

        return HttpResponse(message)
    else:
        form = searchform.SearchForm()
        return render(request, 'index.html', {'form': form})


def a(request):
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = searchform.SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sel1 = form.cleaned_data['sel1']
            sel2 = form.cleaned_data['sel2']
            nci_data = form.cleaned_data['inlineCheckbox1']
            local_data = form.cleaned_data['inlineCheckbox2']
            pubmed_data = form.cleaned_data['inlineCheckbox3']

            message = (str(sel1) + '\n' +
                        str(sel2) + '\n' +
                        str(nci_data) + '\n' +
                        str(local_data) + '\n' +
                        str(pubmed_data))

            return HttpResponseRedirect(message)
    else:
        form = searchform.SearchForm()

    return render(request, 'index.html', {'form': form})

