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


class PhotoUrlField(serializers.RelatedField):

    def to_representation(self, value):
        req = self.context.get('request', None)
        url = value.photo.url
        if not req :
            return url
        return  f'{req.get_host()}{url}'

    pass


class SerPost(serializers.ModelSerializer):

    date_registed = serializers.DateTimeField(read_only=True)
    # photos = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field='photo.url',
    #     required=False,
    #     default=None,
    #     read_only=True,
    # )

    photos = PhotoUrlField(
        many=True,
        required=False,
        default=None,
        read_only=True,
    )

    class Meta:
        model = Post
        fields = ['contents', 'user', 'date_registed', 'photos']


class SerComment(serializers.ModelSerializer):

    date_registed = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['user', 'post', 'contents', 'date_registed', 'reply']
    pass

class SerPhoto(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'post', 'photo']
    pass


class SerFollowRelation(serializers.ModelSerializer):

    class Meta:
        model = FollowRelation
        fields = ['follower', 'followee']

    def is_valid(self, raise_exception=False):
        f_wer = int(self.fields['follower'])
        f_wee = int(self.fields['followee'])
        if f_wer == f_wee:
            raise serializers.ValidationError('follower must be different with followee')
        if f_wer <= 0 or f_wee <=0 :
            raise serializers.ValidationError('Invalid values')
        folower = Author.objects.get(id = f_wer)
        folowee = Author.objects.get(id = f_wee)
        if not folower or not folowee:
            raise serializers.ValidationError('not exists users')
        return super().is_valid(raise_exception)

    def check_follow_input(self, f_wer, f_wee):
        if f_wee <1 or f_wer<1:
            raise serializers.ValidationError('Invalid values')
        author_wer = Author.objects.get(id=f_wer)
        author_wee = Author.objects.get(id=f_wer)
        if not author_wer or not author_wee:
            raise serializers.ValidationError('not exists users')
        return author_wer, author_wee

    def create(self, validated_data):
        f_wer = validated_data.get('follower', 0)
        f_wee = validated_data.get('followee', 0)
        author_wer, author_wee = self.check_follow_input(f_wer, f_wee)
        author_wer.follower_cnt = author_wee.follow_cnt + 1
        author_wee.follower_cnt = author_wee.follower_cnt + 1
        author_wer.save()
        author_wee.save()
        return super().create(validated_data)
    pass

class SerPostLike(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = '__all__'
    pass


class SerCommentLike(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'
