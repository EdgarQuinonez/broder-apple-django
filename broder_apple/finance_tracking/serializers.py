from rest_framework import serializers
from finance_tracking.models import Transaction


class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    date = serializers.DateField()

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.save()

        return instance
