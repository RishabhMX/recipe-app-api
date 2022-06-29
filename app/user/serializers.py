"""
Serializers for the user API View.
"""
from django.contrib.auth import ( get_user_model,authenticate)
from django.utils.translation import gettext as _

from rest_framework import serializers

 #serializers used to validate data

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model() #get current active model
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data): #overrding default serializer create command
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)  #returns validated data from serializer

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None) #retreive and remove password from dictionary
        user = super().update(instance, validated_data) #modidy default logic of update to update ony instance and validated data

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, #hides password
        trim_whitespace=False,  #recognises the whitespace if their in password
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization') #return 404 error

        attrs['user'] = user # sets user attribute as user from above
        return attrs