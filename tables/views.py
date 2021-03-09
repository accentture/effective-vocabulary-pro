# ============================================== documentation recomended:  http://ccbv.co.uk/

from django.shortcuts import render, redirect

#http response
from django.http import HttpResponse, Http404

# importing generic Views
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView 

# models
from tables.models import Word, Table
from user.models import User

#form
from tables.forms import WordForm, TableForm

#to upload pdf file
from django.core.files.storage import FileSystemStorage

# to dowload pdf
from django.http import FileResponse

#to redirect with CreateView
from django.urls import reverse, reverse_lazy

import os
# ************************************************* it doesn´t serve now 

def obtain_owner_table(table_id):
    table = Table.objects.filter(id = table_id)
    owner_table_id = table[0].user_id
    return owner_table_id

def obtain_relation_word(table_id):
    relation_word = Word.objects.filter(table_id = table_id)

    return 

def obtain_pdf_path(datatable):
        pdfname = str(datatable[0].pdf_doc).split('/')
        pdfpath = ''
        print('----------------- check pdf--------', pdfname)

        if pdfname[0] != '':
            pdfpath = datatable[0].pdf_doc.path

        return pdfpath

class xxxTitleTable(TemplateView) : 
    template_name = 'table/title.html'

    def get(self, request, *args, **kwargs) :
        table_form = TableForm()  

        context = {
            'form': table_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs): 

        if request.method == 'POST' :
            table_form = TableForm(request.POST, request.FILES)
            
            if table_form.is_valid():
                table = table_form.save(commit = False)
                table.user_id = request.user.id
                table.save()

            return redirect('app_name:menu', table_id = table.id, title = table.title)

class CreateTitleTable(CreateView):
    template_name = 'table/title.html'
    model = Table
    form_class = TableForm

    #if I want to pass all fields
    #fields = ('__all__')

    # to redirectionate after to save all data
    #success_url = '.' # . : redirect to the same path
    #success_url = reverse_lazy('tables_app:other_tables') #import to evit spaces in the param
    def get_success_url(self):
        return reverse_lazy('tables_app:menu', kwargs = {
            'table_id': self.object.id,
            'title':self.object.title
        })

    # CONCLUSION: never to make two saved in a single code
    # it is used when values entered were correct, it is done checking params established in models
    def form_valid(self, form): # form contain all data entered in the form
        form.instance.user = self.request.user

        # super : it is used to override method provided by django
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTitleTable, self).get_context_data(**kwargs)
        context['action_table'] = self.kwargs['action_table']

        return context
     


class AccessMenuTable(TemplateView) :
    template_name = 'table/main menu.html'

    def obtainAssetsTable(self, table_id):
        assets = Table.objects.filter(id = table_id)
        return assets

    def get(self, request, *args, **kwargs) : 
        table_id = kwargs['table_id']
        title = kwargs['title']
        data_table = self.obtainAssetsTable(table_id)
        owner_table = obtain_owner_table(table_id)
        pdfpath = obtain_pdf_path(data_table)

        return render(request, self.template_name, {
            'table_id': table_id,
            'title': title,
            'pdfpath':pdfpath,
            'pdf_doc':data_table[0].pdf_doc,
            'link':data_table[0].link,
            'owner_table':owner_table
        })

class xxxCreateVocabularyTable(View):
    #django know that method use : get, post, put, delete; it is thanks to dispacht() method

    def get(self, request, *args, **kwargs) : # **kwargs : keys of aditional arguments
        form = WordForm()
        table_id = kwargs['table_id']
        title = kwargs['title']    

        return render(request, 'table/create vocabulary.html', {
            'form': form,
            'table_id': table_id,
            'title':title
        })

    def post(self, request, *args, **kwargs):
        table_id = kwargs['table_id']
        title = kwargs['title']

        if request.method == 'POST' : 
            form = WordForm(request.POST)

            if form.is_valid() :
                #form contain all data saved in database
                                # commit = False : it evits make the first save to database
                form = form.save(commit = False) #save : to save data in database

                #accesing to an attribute of this model saved in database
                form.table_id = table_id
                form.save()

                return redirect('tables_app:create_vocabulary', table_id = table_id, title = title)
             
class CreateVocabulary(CreateView):
    template_name = 'table/create vocabulary.html'
    model = Word
    form_class = WordForm

    def get_context_data(self, **kwargs):
        owner_table_id = obtain_owner_table(self.kwargs['table_id'])

        context = super(CreateVocabulary, self).get_context_data(**kwargs)
        context['table_id'] = self.kwargs['table_id']
        context['title'] = self.kwargs['title']
        context['owner_table'] = owner_table_id

        return context

    #post is executed after to form_valid
    def _post(self, request): # request is used to get data sent by the form
        pass

    def form_valid(self, form):
        form.instance.table_id = self.kwargs['table_id']
        return super().form_valid(form)       

    def get_success_url(self):
        return reverse_lazy('tables_app:create_vocabulary', kwargs = {
            'table_id': self.kwargs['table_id'],
            'title': self.kwargs['title']
        })


#to use here ListView
class ListVocabulary(ListView):
    #to specify name of model to get
    model = Word

    template_name = 'table/word list.html'
    
    #setting name of param to send to context
    context_object_name = 'word_collection'

    def get_queryset(self, *args, **kwargs) :
        table_id = self.kwargs['table_id']
        kword = self.request.GET.get('kword',)

        if kword:
            return Word.objects.filter(table_id = table_id, english_word = kword)

        return Word.objects.filter(table_id = table_id)
    
    #overwriting context
    def get_context_data(self, **kwargs):

        # doing subqueries
        owner_table = obtain_owner_table(self.kwargs['table_id'])
        word_id = obtain_relation_word(self.kwargs['table_id'])

        context = super(ListVocabulary, self).get_context_data(**kwargs)
        context['table_id'] = self.kwargs['table_id']
        context['title'] = self.kwargs['title']
        context['owner_table'] = owner_table

        return context

class UpdateVocabulary(UpdateView):
    template_name = 'table/update vocabulary.html'
    model = Word
    form_class = WordForm
    success_url = reverse_lazy('tables_app:table_collection')


class DeleteVocabulary(DeleteView):
    model = Word
    template_name = 'table/remove vocabulary.html'
    success_url = reverse_lazy('tables_app:table_collection')

class TableCollectionView(ListView) :
    template_name = 'table_collection/table_collection.html'
    context_object_name = 'tables'
    paginate_by = 10
    def get_queryset(self, *args, **kwargs) : 
        return Table.objects.filter(user_id = self.request.user.id)


class OtherTables(ListView) :
    model = Table
    template_name = 'table_collection/table_collection_other_users.html'

    # to paginate queries of database
    paginate_by = 10
    context_object_name = 'tables_and_users'

    def obtain_ids_of_users(self, query_tables):
        for table in query_tables:
            print('-------id----------',table.user_id)

        return

    def get_queryset(self, *args, **kwargs):

        tables = Table.objects.exclude(user_id = self.request.user.id)
        
        users = User.objects.filter(id__in = tables.values_list('id', flat = True))
        query = {
            "tables": tables,
            #"users": User.objects.filter(id__in = tables.values_list('id', flat = True))
        }
        query = [tables, users]


        return tables



class AssetsTable(View):
    template_name = 'table/assets table.html'     


    def get(self, request, *args, **kwargs):
        table_id = kwargs['table_id']
        asset = kwargs['asset']
        datatable = Table.objects.filter(id = table_id)
        owner_table_id = obtain_owner_table(self.kwargs['table_id'])

        pdfpath = obtain_pdf_path(datatable)

        context = {
            'title':datatable[0].title,
            'table_id':datatable[0].id,
            'link':datatable[0].link ,
            'asset':asset,
            'pdfpath':pdfpath,
            'owner_table':owner_table_id
        }
        return render(request, self.template_name, context)

class UpdateTable(UpdateView):
    template_name = 'table/title.html'
    model = Table
    form_class = TableForm
    #success_url = reverse_lazy('tables_app:assets')

    def adsfasdfget_context_data(self, **kwargs):
        context = super(UpdatePdfTable, self).get_context_data(**kwargs)

        context['table_id'] = self.kwargs['table_id']
        context['title'] = self.kwargs['title']

        return context

    #if an error 403 is through, it is an segurity error
    def get_success_url(self):
        project = self.object
        return reverse_lazy('tables_app:table_collection')    

    
class RemoveTable(DeleteView):
    model = Table
    template_name = 'table/remove table.html'
    success_url = reverse_lazy('tables_app:table_collection')

def download_pdf(request, pdfpath) :
    if os.path.exists(pdfpath):
        with open(pdfpath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(pdfpath)
            return response
    raise Http404




def uploadfile_view(request):
    # https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
    if request.method == 'POST':
        f = request.FILES['file']
        fs = FileSystemStorage()
        filename, ext = str(f).split('.')
        file = fs.save(str(f), f)
        fileurl = fs.url(file)
        size = fs.size(file)

        return render(request, 'demo_upload_files.html', {
            'fileUrl':fileurl,
            'fileName':filename,
            'ext':ext,
            'size':size
        })
    else :
        return render(request, 'demo_upload_files.html',{})


