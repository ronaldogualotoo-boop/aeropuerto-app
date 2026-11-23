from datetime import timedelta

from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from django.utils import timezone

from aeropuerto.models import Aeronave, Aerolinea, Aeropuerto, Vuelo


class Command(BaseCommand):
    help = "Crea los grupos, usuarios de demostración y cinco registros de cada modelo."

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name="administradores")
        consultant_group, _ = Group.objects.get_or_create(name="consultores")
        permissions = Permission.objects.filter(content_type__app_label="aeropuerto")
        admin_group.permissions.set(permissions)
        consultant_group.permissions.set(
            permissions.filter(codename__startswith="view_")
            | permissions.filter(codename__in=["add_vuelo", "change_vuelo", "delete_vuelo"])
        )

        admin = self._user(
            "admin_demo",
            "admin@aeropuerto.local",
            "AdminDemo2026!",
            is_staff=True,
            is_superuser=True,
        )
        admin.groups.add(admin_group)
        for username, email, password in (
            ("consultor_demo", "consultor@aeropuerto.local", "ConsultorDemo2026!"),
            ("consultor2_demo", "consultor2@aeropuerto.local", "Consultor2Demo2026!"),
        ):
            user = self._user(username, email, password)
            user.groups.add(consultant_group)

        airports = [
            ("UIO", "Mariscal Sucre", "Quito", "Ecuador"),
            ("GYE", "José Joaquín de Olmedo", "Guayaquil", "Ecuador"),
            ("CUE", "Mariscal Lamar", "Cuenca", "Ecuador"),
            ("MEC", "Eloy Alfaro", "Manta", "Ecuador"),
            ("GPS", "Seymour", "Baltra", "Ecuador"),
        ]
        airport_objects = [
            Aeropuerto.objects.update_or_create(
                codigo_iata=code,
                defaults={
                    "nombre": name,
                    "ciudad": city,
                    "pais": country,
                    "creado_por": admin,
                },
            )[0]
            for code, name, city, country in airports
        ]

        airline_data = [
            ("EQX", "Aero Ecuador", "Ecuador"),
            ("AND", "Andes Air", "Ecuador"),
            ("PAC", "Pacífico Airlines", "Ecuador"),
            ("CND", "Cóndor Regional", "Ecuador"),
            ("GAL", "Galápagos Connect", "Ecuador"),
        ]
        airline_objects = [
            Aerolinea.objects.update_or_create(
                codigo=code,
                defaults={"nombre": name, "pais_origen": country, "creado_por": admin},
            )[0]
            for code, name, country in airline_data
        ]
        for airline in airline_objects:
            airline.aeropuertos_atendidos.set(airport_objects)

        aircraft_data = [
            ("HC-AEA", "Airbus", "A320", 180),
            ("HC-AND", "Boeing", "737-800", 160),
            ("HC-PAC", "Airbus", "A319", 140),
            ("HC-CND", "ATR", "72-600", 72),
            ("HC-GAL", "De Havilland", "Q400", 78),
        ]
        aircraft_objects = [
            Aeronave.objects.update_or_create(
                matricula=registration,
                defaults={
                    "fabricante": maker,
                    "modelo": model,
                    "capacidad": capacity,
                    "aerolinea": airline_objects[index],
                    "creado_por": admin,
                },
            )[0]
            for index, (registration, maker, model, capacity) in enumerate(aircraft_data)
        ]

        now = timezone.now().replace(second=0, microsecond=0)
        for index in range(5):
            departure = now + timedelta(days=index + 1)
            Vuelo.objects.update_or_create(
                codigo=f"EQX{100 + index}",
                defaults={
                    "aerolinea": airline_objects[index],
                    "aeronave": aircraft_objects[index],
                    "origen": airport_objects[index],
                    "destino": airport_objects[(index + 1) % len(airport_objects)],
                    "salida": departure,
                    "llegada": departure + timedelta(hours=1, minutes=15),
                    "estado": Vuelo.Estado.PROGRAMADO,
                    "creado_por": admin,
                },
            )

        self.stdout.write(self.style.SUCCESS("Grupos, cuentas y datos de aeropuerto listos."))

    @staticmethod
    def _user(username, email, password, **flags):
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": email, **flags},
        )
        user.email = email
        for flag, value in flags.items():
            setattr(user, flag, value)
        user.set_password(password)
        user.save()
        return user
