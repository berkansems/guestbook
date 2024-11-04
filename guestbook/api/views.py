from rest_framework import generics
from rest_framework.response import Response
from .models import User, Entry
from .serializers import EntrySerializer, UserSerializer
from django.db.models import Count


class CreateEntryView(generics.CreateAPIView):
    serializer_class = EntrySerializer


class GetEntriesView(generics.ListAPIView):
    serializer_class = EntrySerializer
    pagination_class = None  # To be handled manually for pagination

    def get_queryset(self):
        return Entry.objects.order_by('-created_date')

    def list(self, request, *args, **kwargs):
        page_size = 3
        page_number = int(request.query_params.get('page', 1))
        entries = self.get_queryset()
        total_entries = entries.count()
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        paginated_entries = entries[start_index:end_index]

        response_data = {
            "count": total_entries,
            "page_size": page_size,
            "total_pages": (total_entries + page_size - 1) // page_size,
            "current_page_number": page_number,
            "entries": EntrySerializer(paginated_entries, many=True).data,
        }
        return Response(response_data)


class GetUsersView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.annotate(total_count=Count('entries')).order_by('-total_count')


class EntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    lookup_field = 'id'
