from rest_framework import serializers
from .models import Handbook, HandbookVersion
from datetime import date


class HandbookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Handbook
        fields = ('id', 'code', 'name', )

    # def get_versions(self, obj):

    #     # Фильтруем версии справочника, которые действуют до find_date
    #     versions = obj.versions.all()
    #     return HandbookVersionSerializer(versions, many=True).data

class HandbookVersionSerializer(serializers.ModelSerializer):
#    handbook = HandbookSerializer()

    class Meta:
        model = HandbookVersion
        fields = ('version', 'effective_date', )

    #def get_version(self, obj):
    #    return obj.handbook.name