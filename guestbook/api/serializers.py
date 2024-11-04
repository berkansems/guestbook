from rest_framework import serializers
from .models import User, Entry


class EntrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'subject', 'message', 'created_date', 'name']

    def create(self, validated_data):
        name = validated_data.pop('name')
        user, _ = User.objects.get_or_create(name=name)  # Get or create the user
        entry = Entry.objects.create(user=user, **validated_data)  # Create entry with associated user
        return entry


class UserSerializer(serializers.ModelSerializer):
    last_entry = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'last_entry']

    def get_last_entry(self, obj):
        last_entry = obj.entries.order_by('-created_date').first()
        if last_entry:
            return f"{last_entry.subject} | {last_entry.message}"
        return None
