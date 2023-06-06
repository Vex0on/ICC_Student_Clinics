from .validators import *
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.is_superuser:
            token["is_superuser"] = True
        else:
            token["is_superuser"] = False

        return token


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"

    email = serializers.EmailField(
        validators=[validate_email],
        required=False
    )

    password = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        required=False,
    )

    profile_picture = serializers.ImageField(
        validators=[validate_image],
        required=False,
    )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get("email"),
            username=validated_data.get("email"),
        )
        user.set_password(validated_data.get("password"))
        user.save()

        return user


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = "__all__"

    phone_number = serializers.CharField(validators=[validate_phone_number],
                                         required=False,)

    index_number = serializers.CharField(validators=[validate_index_number],
                                         required=False,)

    pesel = serializers.CharField(validators=[validate_pesel],
                                  required=False,)

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        with transaction.atomic():
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()

            student = Student.objects.create(user=user, **validated_data)

        return student


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = "__all__"

    email = serializers.EmailField(
        validators=[validate_email],
        required=False
    )

    profile_picture = serializers.ImageField(
        validators=[validate_image],
        required=False,
    )

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)

        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()

        return instance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    pesel = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    index_number = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"

    phone_number = serializers.CharField(validators=[validate_phone_number],
                                         required=False,)

    index_number = serializers.CharField(validators=[validate_index_number],
                                         required=False,)

    pesel = serializers.CharField(validators=[validate_pesel],
                                  required=False,)


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        with transaction.atomic():
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()

            doctor = Doctor.objects.create(user=user, **validated_data)

        return doctor

    phone_number = serializers.CharField(validators=[validate_phone_number],
                                         required=False,)

    pesel = serializers.CharField(validators=[validate_pesel],
                                  required=False,)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class DoctorUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    pesel = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    specialization = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"


    phone_number = serializers.CharField(validators=[validate_phone_number],
                                         required=False,)

    pesel = serializers.CharField(validators=[validate_pesel],
                                  required=False,)


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"


class MedicationUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Medication
        fields = "__all__"


class UseMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseMedication
        fields = "__all__"


class UseMedicationUpdateSerializer(serializers.ModelSerializer):
    date_of_use = serializers.DateField(required=False)
    medication = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UseMedication
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


class PrescriptionUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    useMedication = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"


class VisitUpdateSerializer(serializers.ModelSerializer):
    date_of_visit = serializers.DateTimeField(required=False)
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    prescription = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Visit
        fields = "__all__"
