from rest_framework import serializers

from .models import Handbook, HandbookElement


class HandbookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Handbook
        fields = ('id', 'code', 'name', )


class HandbookElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = HandbookElement
        fields = ('code', 'value', )
