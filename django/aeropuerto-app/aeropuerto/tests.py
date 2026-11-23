from datetime import timedelta

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from aeropuerto.models import Aeronave, Aerolinea, Aeropuerto, Vuelo


class AirportAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="admin_demo",
            password="AdminDemo2026!",
            is_superuser=True,
            is_staff=True,
        )
        cls.consultor = User.objects.create_user(
            username="consultor_demo", password="ConsultorDemo2026!"
        )
        group = Group.objects.create(name="consultores")
        group.permissions.set(
            Permission.objects.filter(
                content_type__app_label="aeropuerto",
                codename__in=[
                    "view_aeropuerto",
                    "view_aerolinea",
                    "view_aeronave",
                    "view_vuelo",
                    "add_vuelo",
                    "change_vuelo",
                    "delete_vuelo",
                ],
            )
        )
        cls.consultor.groups.add(group)
        cls.airport = Aeropuerto.objects.create(
            codigo_iata="UIO",
            nombre="Mariscal Sucre",
            ciudad="Quito",
            pais="Ecuador",
            creado_por=cls.admin,
        )
        cls.destination = Aeropuerto.objects.create(
            codigo_iata="GYE",
            nombre="José Joaquín de Olmedo",
            ciudad="Guayaquil",
            pais="Ecuador",
            creado_por=cls.admin,
        )
        cls.airline = Aerolinea.objects.create(
            codigo="EQX", nombre="Aero Ecuador", pais_origen="Ecuador", creado_por=cls.admin
        )
        cls.aircraft = Aeronave.objects.create(
            matricula="HC-ABC",
            fabricante="Airbus",
            modelo="A320",
            capacidad=150,
            aerolinea=cls.airline,
            creado_por=cls.admin,
        )
        cls.flight = Vuelo.objects.create(
            codigo="EQX100",
            aerolinea=cls.airline,
            aeronave=cls.aircraft,
            origen=cls.airport,
            destino=cls.destination,
            salida=timezone.now() + timedelta(days=2),
            llegada=timezone.now() + timedelta(days=2, hours=1),
            creado_por=cls.admin,
        )

    def test_anonymous_user_is_redirected_from_create_view_to_login(self):
        response = self.client.get(reverse("vuelos:vuelo_create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('vuelos:vuelo_create')}",
        )

    def test_registration_saves_email_and_logout_uses_post(self):
        response = self.client.post(
            reverse("registro"),
            {
                "username": "nuevo_usuario",
                "email": "nuevo@example.com",
                "password1": "VueloSeguro2026!9",
                "password2": "VueloSeguro2026!9",
            },
            follow=True,
        )
        self.assertTrue(User.objects.filter(username="nuevo_usuario", email="nuevo@example.com").exists())
        self.assertContains(response, "Tu cuenta se creó correctamente.")
        self.client.force_login(User.objects.get(username="nuevo_usuario"))
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        response = self.client.post(reverse("logout"), follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_consultant_can_view_but_cannot_edit_other_users_flight(self):
        self.client.force_login(self.consultor)
        self.assertEqual(self.client.get(self.flight.get_absolute_url()).status_code, 200)
        self.assertEqual(
            self.client.get(reverse("vuelos:vuelo_update", args=[self.flight.pk])).status_code,
            403,
        )

    def test_consultant_can_create_and_edit_own_flight(self):
        self.client.force_login(self.consultor)
        response = self.client.post(
            reverse("vuelos:vuelo_create"),
            {
                "codigo": "EQX200",
                "aerolinea": self.airline.pk,
                "aeronave": self.aircraft.pk,
                "origen": self.airport.pk,
                "destino": self.destination.pk,
                "salida": (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
                "llegada": (timezone.now() + timedelta(days=3, hours=1)).strftime("%Y-%m-%dT%H:%M"),
                "estado": Vuelo.Estado.PROGRAMADO,
            },
            follow=True,
        )
        flight = Vuelo.objects.get(codigo="EQX200")
        self.assertEqual(flight.creado_por, self.consultor)
        self.assertContains(response, "Vuelo creado correctamente.")
        self.assertEqual(
            self.client.get(reverse("vuelos:vuelo_update", args=[flight.pk])).status_code,
            200,
        )

    def test_group_permissions_control_create_buttons(self):
        self.client.force_login(self.consultor)
        response = self.client.get(reverse("vuelos:vuelo_list"))
        self.assertContains(response, "Programar vuelo")
        self.assertNotContains(response, "Agregar aeropuerto")
        self.client.force_login(self.admin)
        response = self.client.get(reverse("aeropuertos:aeropuerto_list"))
        self.assertContains(response, "Agregar aeropuerto")

    def test_delete_requires_post_confirmation(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("vuelos:vuelo_delete", args=[self.flight.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Vuelo.objects.filter(pk=self.flight.pk).exists())
        response = self.client.post(reverse("vuelos:vuelo_delete", args=[self.flight.pk]))
        self.assertRedirects(response, reverse("vuelos:vuelo_list"))
        self.assertFalse(Vuelo.objects.filter(pk=self.flight.pk).exists())

    def test_flight_validation_rejects_same_origin_and_destination(self):
        from aeropuerto.forms import VueloForm

        form = VueloForm(
            data={
                "codigo": "BAD100",
                "aerolinea": self.airline.pk,
                "aeronave": self.aircraft.pk,
                "origen": self.airport.pk,
                "destino": self.airport.pk,
                "salida": (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
                "llegada": (timezone.now() + timedelta(days=3, hours=1)).strftime("%Y-%m-%dT%H:%M"),
                "estado": Vuelo.Estado.PROGRAMADO,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("destino", form.errors)
