from django.test import TestCase, Client, override_settings
from django.urls import reverse
from clinicalsApp.models import Patient, ClinicalData
from clinicalsApp.forms import PatientForm, ClinicalDataForm


# ─── Model Tests ────────────────────────────────────────────────────────────────

class PatientModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_patient_creation(self):
        self.assertEqual(self.patient.firstName, "John")
        self.assertEqual(self.patient.lastName, "Doe")
        self.assertEqual(self.patient.age, 30)

    def test_patient_str_representation(self):
        """Patient object should be representable as a string."""
        patient_str = str(self.patient)
        self.assertIn("Patient object", patient_str)

    def test_patient_id_auto_generated(self):
        self.assertIsNotNone(self.patient.id)

    def test_multiple_patients(self):
        Patient.objects.create(firstName="Jane", lastName="Smith", age=25)
        self.assertEqual(Patient.objects.count(), 2)


class ClinicalDataModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )
        self.bp_data = ClinicalData.objects.create(
            componentName="bp",
            componentValue="120/80",
            patient=self.patient,
        )

    def test_clinical_data_creation(self):
        self.assertEqual(self.bp_data.componentName, "bp")
        self.assertEqual(self.bp_data.componentValue, "120/80")
        self.assertEqual(self.bp_data.patient, self.patient)

    def test_measured_datetime_auto_set(self):
        self.assertIsNotNone(self.bp_data.measuredDateTime)

    def test_cascade_delete(self):
        """Deleting a patient should delete all related clinical data."""
        ClinicalData.objects.create(
            componentName="heart rate",
            componentValue="72",
            patient=self.patient,
        )
        self.assertEqual(ClinicalData.objects.count(), 2)
        self.patient.delete()
        self.assertEqual(ClinicalData.objects.count(), 0)

    def test_component_name_choices(self):
        valid_choices = ["hw", "bp", "heart rate"]
        for choice in valid_choices:
            data = ClinicalData.objects.create(
                componentName=choice,
                componentValue="test",
                patient=self.patient,
            )
            self.assertEqual(data.componentName, choice)

    def test_height_weight_value_format(self):
        hw_data = ClinicalData.objects.create(
            componentName="hw",
            componentValue="5.8/150",
            patient=self.patient,
        )
        parts = hw_data.componentValue.split("/")
        self.assertEqual(len(parts), 2)


# ─── Form Tests ─────────────────────────────────────────────────────────────────

class PatientFormTest(TestCase):
    def test_valid_form(self):
        form = PatientForm(data={
            "firstName": "John",
            "lastName": "Doe",
            "age": 30,
        })
        self.assertTrue(form.is_valid())

    def test_missing_first_name(self):
        form = PatientForm(data={
            "firstName": "",
            "lastName": "Doe",
            "age": 30,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("firstName", form.errors)

    def test_missing_age(self):
        form = PatientForm(data={
            "firstName": "John",
            "lastName": "Doe",
            "age": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

    def test_invalid_age_type(self):
        form = PatientForm(data={
            "firstName": "John",
            "lastName": "Doe",
            "age": "abc",
        })
        self.assertFalse(form.is_valid())


class ClinicalDataFormTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_valid_form(self):
        form = ClinicalDataForm(data={
            "componentName": "bp",
            "componentValue": "120/80",
            "patient": self.patient.id,
        })
        self.assertTrue(form.is_valid())

    def test_missing_component_value(self):
        form = ClinicalDataForm(data={
            "componentName": "bp",
            "componentValue": "",
            "patient": self.patient.id,
        })
        self.assertFalse(form.is_valid())

    def test_invalid_component_name(self):
        form = ClinicalDataForm(data={
            "componentName": "invalid",
            "componentValue": "120/80",
            "patient": self.patient.id,
        })
        self.assertFalse(form.is_valid())


# ─── View Tests ──────────────────────────────────────────────────────────────────

class PatientListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_patient_list_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_patient_list_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "clinicalsApp/patient_list.html")

    def test_patient_list_contains_patient(self):
        response = self.client.get("/")
        self.assertContains(response, "John")
        self.assertContains(response, "Doe")

    def test_patient_list_empty(self):
        Patient.objects.all().delete()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["patient_list"]), 0)

    def test_patient_list_multiple_patients(self):
        Patient.objects.create(firstName="Jane", lastName="Smith", age=25)
        response = self.client.get("/")
        self.assertEqual(len(response.context["patient_list"]), 2)


class PatientCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_page_status_code(self):
        response = self.client.get("/create/")
        self.assertEqual(response.status_code, 200)

    def test_create_page_template(self):
        response = self.client.get("/create/")
        self.assertTemplateUsed(response, "clinicalsApp/patient_form.html")

    def test_create_patient_post(self):
        response = self.client.post("/create/", {
            "firstName": "John",
            "lastName": "Doe",
            "age": 30,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.first()
        self.assertEqual(patient.firstName, "John")

    def test_create_patient_invalid_data(self):
        response = self.client.post("/create/", {
            "firstName": "",
            "lastName": "Doe",
            "age": 30,
        })
        self.assertEqual(response.status_code, 200)  # re-renders form
        self.assertEqual(Patient.objects.count(), 0)


class PatientUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_update_page_status_code(self):
        response = self.client.get(f"/update/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)

    def test_update_patient_post(self):
        response = self.client.post(f"/update/{self.patient.pk}", {
            "firstName": "Johnny",
            "lastName": "Doe",
            "age": 31,
        })
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.firstName, "Johnny")
        self.assertEqual(self.patient.age, 31)

    def test_update_nonexistent_patient(self):
        response = self.client.get("/update/9999")
        self.assertEqual(response.status_code, 404)


class PatientDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_delete_confirmation_page(self):
        response = self.client.get(f"/delete/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "clinicalsApp/patient_confirm_delete.html"
        )

    def test_delete_patient_post(self):
        response = self.client.post(f"/delete/{self.patient.pk}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Patient.objects.count(), 0)

    def test_delete_nonexistent_patient(self):
        response = self.client.post("/delete/9999")
        self.assertEqual(response.status_code, 404)


class AddDataViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_add_data_page_status_code(self):
        response = self.client.get(f"/addData/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)

    def test_add_data_page_template(self):
        response = self.client.get(f"/addData/{self.patient.pk}")
        self.assertTemplateUsed(
            response, "clinicalsApp/clinicaldata_form.html"
        )

    def test_add_data_shows_patient_info(self):
        response = self.client.get(f"/addData/{self.patient.pk}")
        self.assertContains(response, "John")
        self.assertContains(response, "Doe")

    def test_add_clinical_data_post(self):
        response = self.client.post(f"/addData/{self.patient.pk}", {
            "componentName": "bp",
            "componentValue": "120/80",
            "patient": self.patient.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ClinicalData.objects.count(), 1)
        data = ClinicalData.objects.first()
        self.assertEqual(data.componentName, "bp")
        self.assertEqual(data.patient, self.patient)

    def test_add_heart_rate_data(self):
        self.client.post(f"/addData/{self.patient.pk}", {
            "componentName": "heart rate",
            "componentValue": "72",
            "patient": self.patient.id,
        })
        self.assertEqual(ClinicalData.objects.count(), 1)
        data = ClinicalData.objects.first()
        self.assertEqual(data.componentName, "heart rate")

    def test_add_height_weight_data(self):
        self.client.post(f"/addData/{self.patient.pk}", {
            "componentName": "hw",
            "componentValue": "5.8/150",
            "patient": self.patient.id,
        })
        self.assertEqual(ClinicalData.objects.count(), 1)


class AnalyzeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_analyze_page_status_code(self):
        response = self.client.get(f"/analyze/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)

    def test_analyze_page_template(self):
        response = self.client.get(f"/analyze/{self.patient.pk}")
        self.assertTemplateUsed(response, "clinicalsApp/generateReport.html")

    def test_analyze_with_bp_data(self):
        ClinicalData.objects.create(
            componentName="bp",
            componentValue="120/80",
            patient=self.patient,
        )
        response = self.client.get(f"/analyze/{self.patient.pk}")
        self.assertContains(response, "120/80")

    def test_analyze_bmi_calculation(self):
        ClinicalData.objects.create(
            componentName="hw",
            componentValue="5.8/150",
            patient=self.patient,
        )
        response = self.client.get(f"/analyze/{self.patient.pk}")
        self.assertContains(response, "BMI")
        # Verify BMI is in response data
        data = response.context["data"]
        bmi_entries = [d for d in data if d.componentName == "BMI"]
        self.assertEqual(len(bmi_entries), 1)
        self.assertIsNotNone(bmi_entries[0].componentValue)

    def test_analyze_no_data(self):
        response = self.client.get(f"/analyze/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["data"]), 0)

    def test_analyze_multiple_entries(self):
        ClinicalData.objects.create(
            componentName="bp",
            componentValue="120/80",
            patient=self.patient,
        )
        ClinicalData.objects.create(
            componentName="heart rate",
            componentValue="72",
            patient=self.patient,
        )
        ClinicalData.objects.create(
            componentName="hw",
            componentValue="5.8/150",
            patient=self.patient,
        )
        response = self.client.get(f"/analyze/{self.patient.pk}")
        data = response.context["data"]
        # 3 original entries + 1 BMI = 4
        self.assertEqual(len(data), 4)

    def test_analyze_hw_without_slash(self):
        """Height/weight entry without slash should not produce BMI."""
        ClinicalData.objects.create(
            componentName="hw",
            componentValue="150",
            patient=self.patient,
        )
        response = self.client.get(f"/analyze/{self.patient.pk}")
        data = response.context["data"]
        bmi_entries = [d for d in data if d.componentName == "BMI"]
        self.assertEqual(len(bmi_entries), 0)


# ─── URL Routing Tests ──────────────────────────────────────────────────────────

class URLRoutingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create(
            firstName="John", lastName="Doe", age=30
        )

    def test_index_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_url(self):
        response = self.client.get("/create/")
        self.assertEqual(response.status_code, 200)

    def test_update_url(self):
        response = self.client.get(f"/update/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)

    def test_delete_url(self):
        response = self.client.get(f"/delete/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)

    def test_add_data_url(self):
        response = self.client.get(f"/addData/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)

    def test_analyze_url(self):
        response = self.client.get(f"/analyze/{self.patient.pk}")
        self.assertEqual(response.status_code, 200)
