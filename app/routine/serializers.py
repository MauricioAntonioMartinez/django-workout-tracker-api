from core.models import Exercise, Routine, RoutineDay, SetRoutine, SerieRoutine, Serie
from rest_framework import serializers
from exercise.serializers import ExerciseSerializer


class AddRoutineWorkout(serializers.Serializer):
    date = serializers.DateField()
    name = serializers.CharField(max_length=255, trim_whitespace=True)


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerieRoutine
        fields = ('id', 'reps', 'weight', 'comment')
        read_only_fields = ('id',)


class SetSerializer(serializers.ModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all()
    )
    series = SerieSerializer(many=True)

    class Meta:
        model = SetRoutine
        fields = ['id', 'series', 'exercise']
        read_only_fields = ('id',)
        extra_keyargs = {
            "exercise": {
                "write_only": True
            }
        }


class SetDetailSerializer(SetSerializer):
    exercise = ExerciseSerializer()
    series = serializers.SerializerMethodField(
        method_name='get_series')

    def get_series(self, instance):
        serializer = SerieSerializer(SerieRoutine.objects.filter(
            father_set=instance), many=True)
        return serializer.data


class RoutineDaySerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True)

    class Meta:
        model = RoutineDay
        fields = ('id', 'name', 'sets')
        read_only_fields = ('id',)


class RoutineDetailSerializer(RoutineDaySerializer):
    sets = serializers.SerializerMethodField(
        method_name='get_sets')

    def get_sets(self, instance):
        print(instance)
        serializer = SetDetailSerializer(SetRoutine.objects.filter(
            routine=instance), many=True)
        return serializer.data


class RoutineSerializer(serializers.ModelSerializer):
    routines = RoutineDaySerializer(many=True)

    class Meta:
        model = Routine
        fields = ('id', 'name', 'routines')
        read_only_fields = ('id',)

    def create(self, validated_data):
        routine_days = validated_data.pop('routines')
        routine = Routine.objects.create(name=validated_data['name'],
                                         user=self.context['request'].user)
        for routine_day in routine_days:
            sets = routine_day.pop('sets')
            routine_created = RoutineDay.objects.create(
                name=routine_day['name'], routine=routine)
            for st in sets:
                print(st)
                series = st.pop('series')
                set_created = SetRoutine.objects.create(routine=routine_created,
                                                        exercise=st['exercise'])
                for sr in series:
                    SerieRoutine.objects.create(father_set=set_created, **sr)

        return routine

    def update(self, instance, validated_data):
        routine_days = validated_data.pop('routines')
        instance.name = validated_data.get('name', instance.name)

        for routine in instance.routines.all():
            routine.delete()

        for routine_day in routine_days:
            sets = routine_day.pop('sets')
            routine_created = RoutineDay.objects.create(
                name=routine_day['name'], routine=instance)
            for st in sets:
                print(st)
                series = st.pop('series')
                set_created = SetRoutine.objects.create(routine=routine_created,
                                                        exercise=st['exercise'])
                for sr in series:
                    SerieRoutine.objects.create(father_set=set_created, **sr)
        return instance
# TODO: see what the heck is happening here

# !DEPRECATED
#


class RoutineDetailSerializer(RoutineSerializer):
    routines = RoutineDetailSerializer(many=True)

    class Meta:
        model = Routine
        fields = ('id', 'name', 'routines')
        read_only_fields = ('id',)
