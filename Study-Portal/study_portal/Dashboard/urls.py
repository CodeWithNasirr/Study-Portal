from django.urls import path,reverse,include
from . import views
urlpatterns = [
    path("",views.Home,name="Home"),
    path("notes",views.Note,name="Note"),
    path("delete_notes/<int:id>",views.DeleteNote,name="DeleteNote"),
    path("details_notes/<int:pk>",views.DetailsNote.as_view(),name="Details-Note"),
    path("home_work",views.Home_Work,name="Home-Work"),
    path("delete_work/<int:id>",views.DeleteHome_Work,name="DeleteWork"),
    path("Youtube",views.Youtube,name="Youtube"),
    path("todo",views.todo,name="Todo"),
    path("Delete_Todo/<int:id>",views.DeleteTodo,name="Delete-Todo"),
    path("book",views.Book,name="Book"),
    path("dictionary",views.Desc,name="Dictionary"),
    path("wiki",views.Wiki,name="Wikipidia"),
    path("conversion",views.Conversion,name="conversion"),
]  