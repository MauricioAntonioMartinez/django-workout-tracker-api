
from core.models import Exercise, Serie, Set, Workout
from exercise.serializers import ExerciseSerializer
from rest_framework import serializers


class WorkoutSerializer(serializers.ModelSerializer):

    #sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'workout_date',)
        read_only_fields = ('id',)


class SerieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Serie
        fields = ('id', 'reps', 'weight', 'comment')
        read_only_fields = ('id',)


class SetSerializer(serializers.ModelSerializer):

    exercise = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all()
    )

    series = SerieSerializer(many=True)

    class Meta:
        model = Set
        fields = ['id', 'exercise', 'series']
        read_only_fields = ('id',)

        extra_keyargs = {
            "exercise": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        new_series = validated_data.pop('series')

        _set = Set.objects.create(**validated_data)
        for serie in new_series:
            Serie.objects.create(father_set=_set, **serie)
        return _set


class SetDetailSerializer(SetSerializer):
    series = SerieSerializer(many=True, read_only=True)
    exercise = ExerciseSerializer()
