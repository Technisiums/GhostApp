from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.authtoken.models import Token


class UserCreateSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True, source='auth_token.key')
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(label="First Name")
    last_name = serializers.CharField(label="Last Name")
    email = serializers.EmailField(label="Email Address")
    email2 = serializers.EmailField(write_only=True, label="Confirm Email")
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'email2',
                  'password',
                  'password2',
                  'token',
                  )

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Email must be matched.")
        return value

    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get('email2')
        email1 = value
        if email1 != email2:
            raise ValidationError("Email must be matched.")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get('password')
        password2 = value
        if password1 != password2:
            raise ValidationError("password must be matched.")
        return value

    def create(self, validated_data):
        fname = validated_data['first_name']
        lname = validated_data['last_name']
        uname = validated_data['username']
        emailx = validated_data['email']
        password = validated_data['password']
        user = get_user_model().objects.create(
            first_name=fname,
            last_name=lname,
            username=uname,
            email=emailx,
        )
        user.set_password(password)
        user.save()
        data = self.get_initial()
        data['token'] = Token.objects.create(user=user)
        user.refresh_from_db()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(label="User Name")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'password',
            'token',
        ]

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = get_user_model().objects.filter(
            Q(username=username)
        ).distinct()

        if user.exists() and user.count() == 1:
            user = user.first()
        else:
            raise ValidationError("This username does not exists")

        if user:
            if not user.check_password(password):
                raise ValidationError("Invalid Credentials")
            else:
                attrs['token'] = Token.objects.get_or_create(user=user)
        return attrs


class UserSearchSerializer(serializers.ModelSerializer):
    search = serializers.CharField(write_only=True, allow_blank=False)

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'search'
                  )
        read_only_fields = ['id',
                            'first_name',
                            'last_name',
                            'username',
                            'email',
                            ]


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(label="First Name")
    last_name = serializers.CharField(label="Last Name")
    email = serializers.EmailField(label="Email Address")
    email2 = serializers.EmailField(write_only=True, label="Confirm Email")

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'email2',
                  )

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Email must be matched.")
        return value

    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get('email2')
        email1 = value
        if email1 != email2:
            raise ValidationError("Email must be matched.")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.save()
