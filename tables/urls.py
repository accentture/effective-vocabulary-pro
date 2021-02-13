
from django.urls import path

#to protect path
from django.contrib.auth.decorators import login_required

from . import views

#to put name to all set of paths
app_name = 'tables_app' # 'tables_app' : is used this name_app by convention

urlpatterns = [
    path('titulo/<str:action_table>', login_required(views.CreateTitleTable.as_view()), name = 'title'),
    path('menu/<int:table_id>/<str:title>', login_required(views.AccessMenuTable.as_view()), name = 'menu'),
    path('crear-vocabulario/<int:table_id>/<str:title>', login_required(views.CreateVocabulary.as_view()), name = 'create_vocabulary'),
    path('actualizar-vocabulario/<pk>/', login_required(views.UpdateVocabulary.as_view()), name = 'update_vocabulary'),
    path('eliminar-vocabulario/<pk>/', login_required(views.DeleteVocabulary.as_view()), name = 'delete_vocabulary'),
    path('lista-de-palabras/<int:table_id>/<str:title>', login_required(views.ListVocabulary.as_view()), name = 'word_list'),
    path('coleccion-tablas/', login_required(views.TableCollectionView.as_view()), name = 'table_collection'),
    path('otras-tablas/', login_required(views.OtherTables.as_view()), name = 'other_tables'),
    path('bienes/<int:table_id>/<str:asset>', login_required(views.AssetsTable.as_view()), name = 'assets'),
    path('actualizar/<pk>/', login_required(views.UpdateTable.as_view()), name = 'updatetable'),
    path('elimninar-tabla/<pk>/', login_required(views.RemoveTable.as_view()), name = 'removetable'),
    path('descarga/<str:pdfpath>', login_required(views.download_pdf), name = 'download'),
    path('subir/', login_required(views.uploadfile_view), name = 'upload'),

] 