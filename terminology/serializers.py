from rest_framework import serializers
from .models import Handbook, HandbookVersion, HandbookElement
from datetime import date


class HandbookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Handbook
        fields = ('id', 'code', 'name', )


# class HandbookVersionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = HandbookVersion
#         fields = ('version', 'effective_date', )


class HandbookElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = HandbookElement
        fields = ('code', 'value', )