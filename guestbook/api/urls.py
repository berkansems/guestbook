from django.urls import path
from .views import CreateEntryView, GetEntriesView, GetUsersView, EntryDetailView

urlpatterns = [
    path('entries/', CreateEntryView.as_view(), name='create-entry'),
    path('entries/list/', GetEntriesView.as_view(), name='get-entries'),
    path('entries/<int:id>/', EntryDetailView.as_view(), name='get-entry-detail'),  # Add this line
    path('users/', GetUsersView.as_view(), name='get-users'),
]
