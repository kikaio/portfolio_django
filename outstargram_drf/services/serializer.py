from rest_framework import serializers
from outstargram_drf.models import *


class SerGm(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    password = serializers.CharField(
        read_only=True,
        style = {
            'input_type' : 'password'
        },
        max_length=100
    )
    is_active = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(default=False)
    is_locked = serializers.BooleanField(default=False)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        pw = validated_data.get('pw', None)
        if email is None or pw is None:
            raise serializers.ValidationError("input is invalid")
        new_user = User.object.create_user(email, pw)
        return new_user

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', None)
        if instance.password is None:
            raise serializers.ValidationError('input is invalid')
        instance.is_active = validated_data.get('is_active', True)
        instance.is_superuser = validated_data.get('is_superuser', False)
        instance.is_locked = validated_data.get('is_locked', False)
        instance.save()
        return instance


class SerAuthor(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    follow_cnt = serializers.IntegerField(default=0)
    follower_cnt = serializers.IntegerField(default=0)
    desc = serializers.CharField(default='', max_length=100)

    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, inst, validated_data):
        inst.follow_cnt = validated_data.get('follow_cnt', inst.follow_cnt)
        inst.follower_cnt = validated_data.get('follower_cnt', inst.follower_cnt)
        inst.desc = validated_data.get('desc', inst.desc)
        inst.save()
        return inst
    pass


class SerPost(serializers.ModelSerializer):

    date_registed = serializers.DateTimeField(read_only=True)
    photos = serializers.SlugRelatedField(queryset= Photo.objects.all(), slug_field='name')

    class Meta:
        model = Post
        fields = ['contents', 'author', 'date_registed', 'photos']


class SerPhoto(serializers.ModelSerializer):

    class Meta:
        model = Photo