from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer, owner field not editable.
    get_is_owner needs access to request via context to determine
    if a given user owns the profile (is_owner).
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'is_owner', 'created_at',
            'updated_at', 'name', 'content', 'image'
        ]
