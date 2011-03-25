from django.shortcuts import render_to_response
from sarpaminfohub.infohub.results_table import ResultsTable
from sarpaminfohub.infohub.drug_searcher import DrugSearcher
from sarpaminfohub.infohub.django_backend import DjangoBackend
from sarpaminfohub.infohub.test_backend import TestBackend
from sarpaminfohub.infohub.formulation_table import FormulationTable
from sarpaminfohub.infohub.formulation_graph import FormulationGraph
from django.core.urlresolvers import reverse
from sarpaminfohub.infohub.supplier_catalogue_table import SupplierCatalogueTable
from sarpaminfohub.infohub.product_table import ProductTable
from sarpaminfohub.infohub.menu import Menu
from sarpaminfohub.infohub.forms import SearchForm
from django.template import RequestContext
from copy import deepcopy
from django.conf import settings

def get_backend(name):
    if name == "test":
        backend = TestBackend()
    else:
        backend = DjangoBackend()

    return backend

def search(request):
    search_term = request.GET.get('search', None)
    
    initial_form_values = {'search' : search_term} 

    if search_term is not None:
        backend_name = request.GET.get('backend', "django")
        
        backend = get_backend(backend_name)
            
        drug_searcher = DrugSearcher(backend)
        rows = drug_searcher.get_formulations_that_match(search_term)
    
        results_table = ResultsTable(rows, search_term)
        search_results_tab = get_search_results_tab()
        menu = Menu([search_results_tab])
    else:
        menu = None
        results_table = None
        
    search_form = SearchForm(initial = initial_form_values)
    extra_context = {
                'search_form': search_form,
                'results_table': results_table,
                'menu' : menu,
                'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
                'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE},
    return render_to_response(
                        'search.html', 
                        dictionary=extra_context,
                        context_instance=RequestContext(request))
    
def formulation(request, formulation_id, backend_name="django"):
    backend = get_backend(backend_name)

    drug_searcher = DrugSearcher(backend)
    rows = drug_searcher.get_prices_for_formulation_with_id(formulation_id)

    # Don't like that, but results is being changed in the constructor of the table.
    rows_graph = deepcopy(rows)

    formulation_name = drug_searcher.get_formulation_name_with_id(formulation_id)
    formulation_msh = drug_searcher.get_formulation_msh_with_id(formulation_id)

    formulation_table = FormulationTable(rows)
    formulation_graph = FormulationGraph(rows_graph, formulation_msh)

    search_form = SearchForm()

    products_href = reverse('formulation_products', args=[str(formulation_id),
                                                           backend_name])
    formulation_tab = get_formulation_tab(None)
    products_tab = get_products_tab(products_href)
    menu = Menu([formulation_tab, products_tab])
    extra_context = {
                'formulation_table': formulation_table,
                'formulation_graph': formulation_graph,
                'formulation_msh': formulation_msh,
                'menu' : menu,
                'search_form' : search_form,
                'sub_title' : formulation_name,
                'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
                'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE}
    return render_to_response(
                        'formulation.html',
                        extra_context,
                        RequestContext(request))

def formulation_products(request, formulation_id, backend_name="django"):
    backend = get_backend(backend_name)
    
    drug_searcher = DrugSearcher(backend)
    
    rows = drug_searcher.get_product_registrations_based_on_formulation_with_id(formulation_id)
    
    supplier_table = ProductTable(rows)
    search_form = SearchForm()

    formulation_name = drug_searcher.get_formulation_name_with_id(formulation_id)
    formulation_href = reverse('formulation', args=[str(formulation_id),
                                                    backend_name])

    formulation_tab = get_formulation_tab(formulation_href)
    products_tab = get_products_tab()
    menu = Menu([formulation_tab, products_tab])
    extra_context = {
            'supplier_table' : supplier_table,
            'search_form' : search_form,
            'menu' : menu,
            'sub_title' : formulation_name,
            'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
            'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE}
    return render_to_response(
                'formulation_products.html',
                extra_context,            
                RequestContext(request))

def supplier_catalogue(request, supplier_id, backend_name="django"):
    backend = get_backend(backend_name)

    drug_searcher = DrugSearcher(backend)

    rows = drug_searcher.get_products_from_supplier_with_id(supplier_id)

    supplier_catalogue_table = SupplierCatalogueTable(rows)
    search_form = SearchForm()
    
    catalogue_tab = get_catalogue_tab()
    menu = Menu([catalogue_tab])

    supplier_name = drug_searcher.get_name_of_supplier_with_id(supplier_id)
    extra_context = {
                'supplier_catalogue_table':supplier_catalogue_table,
                'menu': menu,
                'search_form' : search_form,
                'sub_title' : supplier_name,
                'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
                'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE},    
    return render_to_response(
                    'supplier_catalogue.html',
                    extra_context,
                    context_instance=RequestContext(request))

def get_formulation_tab(formulation_href=None):
    return get_tab(formulation_href, "Procurement Prices")

def get_products_tab(products_href=None):
    return get_tab(products_href, "Products")

def get_catalogue_tab():
    return get_tab(None, "Product Catalogue")

def get_search_results_tab():
    return get_tab(None, "Search Results")

def get_tab(href, text):
    return {'href' : href, 'text' : text}
