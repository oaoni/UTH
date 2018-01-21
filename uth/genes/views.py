from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

# Create your views here.

from . import gene
from . import gdc_query

def index(request):
    message = ""
    return render(request, 'index.html', {'results': message})
#    template = loader.get_template("index.html")
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
        if ('nci_data' in request.POST):
            sel1 = request.POST['sel1']
            slice_at = sel1.find(']')
            sel1 = sel1[1:slice_at]
            # todo format query
            nci_query = sel1
            gdc_query(nci_query)
            # todo process query

        if ('local_data' in request.POST):
            local_data = request.POST['local_data']

        if ('pubmed_data' in request.POST and 'sel2' in request.POST):
            sel2 = request.POST['sel2']
            slice_at = sel2.find('[')
            sel2 = sel2[:slice_at-1]
            pubmed_query = sel2 + '[All Fields]'
            gene_list = gene.pubmed_get_genes(pubmed_query)
            message = gene_list

        print(message)

        return render(request, 'index.html', {'results': message})
    else:
        form = searchform.SearchForm()
        return render(request, 'index.html', {'form': form})


