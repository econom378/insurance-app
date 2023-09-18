from django.db import models
from django.utils import timezone

class InsuranceType(models.TextChoices):
    ESTATE = "Pojištění majetku",'Pojištění majetku'
    LIFE = "Životní pojištění",'Životní pojištění'
    TRAVEL = "Cestovní pojištění",'Cestovní pojištění'
    OBLIGED = "Povinné ručení",'Povinné ručení'
    ACCIDENT = "Havarijní pojištění",'Havarijní pojištění'
    INJURY = "Úrazové pojištění",'Úrazové pojištění'
    OTHER = "Jiné pojištění",'Jiné pojištění'

class ClientType(models.TextChoices):
    PLACEHOLDER = "POK",'Pojistník'
    INSURED = "POJ",'Pojištěnec'


class PolicyHolder(models.Model):
    """
        Represents a policyholder in the insurance system.

        It includes information such as the name, lastname, birth_id, cell_phone_no,
        email, street, street_no, city, country, photo, zip_code, created and updated.

        :param name: Firstname of th policyholder.
        :type name: str
        :param lastname: Lastname of th policyholder.
        :type lastname: str
        :param birth_id: The main identifier (birth id) of the policyholder.
        :type birth_id: str
        :param cell_phone_no: The cell phone number of the policyholder.
        :type cell_phone_no: str
        :param email: The email of the policyholder.
        :type email: str
        :param street: Address - street where the policyholder lives.
        :type street: str
        :param street_no: Address - street number where the policyholder lives.
        :type street_no: str
        :param city: Address - city where the policyholder lives.
        :type city: str
        :param country: Address - country where the policyholder lives.
        :type country: str
        :param photo: Photo of policyholder.
        :type photo: str
        :param zip_code: Address - zip code of the city where the policyholder lives.
        :type zip_code: str
        :param created: The date and time when the insurance was created.
        :type created: datetime.datetime
        :param updated: The date and time when the insurance was updated.
        :type updated: datetime.datetime
    """
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    birth_id = models.CharField(max_length=30, unique=True)
    cell_phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    street = models.CharField(max_length=30)
    street_no = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='pojisteni/static/pojisteni/JPG/')
    zip_code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.birth_id)


class InsuranceModel(models.Model):
    """
        Represents an insurance in the insurance system.

        This model represents an insurance that can be assigned to policyholder.
        It includes information such as the policyholder, paid_by, insurance_type, target_amount,
        insurance_object, valid_from, valid_to, created and updated.

        :param policyholder: The policyholder to whom the insurance belongs.
        :type policyholder: Policyholder
        :param paid_by: who paid the insurance
        :type paid_by: str
        :param insurance_type: the type of insurance asked by policyholder.
        :type insurance_type: str
        :param target_amount: The final price which cover events of policyholder.
        :type target_amount: int
        :param insurance_object: The object which the insurance is required for.
        :type insurance_object: str
        :param valid_from: The date when the insurance is valid from.
        :type valid_from: datetime.date
        :param valid_to: The date when the insurance is valid to.
        :type valid_to: datetime.date
        :param created: The date and time when the insurance was created.
        :type created: datetime.datetime
        :param updated: The date and time when the insurance was updated.
        :type updated: datetime.datetime

        :param InsuranceType: Choices for the 'insurance_type' field.
        :type InsuranceType: tuple of tuples
        :param ClientType: Choices for the 'paid_by' field.
        :type ClientType: tuple of tuples
    """

    policyholder = models.ForeignKey(PolicyHolder,
                                     on_delete=models.CASCADE)
    paid_by = models.CharField(max_length=20,
                                      choices=ClientType.choices,
                                      default=ClientType.INSURED)
    insurance_type = models.CharField(max_length=30,
                                      choices=InsuranceType.choices,
                                      default=InsuranceType.ESTATE)
    target_amount = models.IntegerField(default=None, blank=False)
    insurance_object = models.CharField(max_length=30, default=None)
    valid_from = models.DateField()
    valid_to = models.DateField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.insurance_type + " " + str(self.valid_from) + " " +
                str(self.valid_to))


class EventModel(models.Model):
    """
        Represents an event in the insurance system.

        This model represents an event that can be assigned to the policyholder.
        It includes information such as the policyholder, title, contract_no, event_date,
        desc, attach1, attach2, created and updated.

        :param policyholder: The policyholder to whom the insurance belongs.
        :type policyholder: Policyholder
        :param title: short description (title) of the event
        :type title: str
        :param contract_no: the number of the contract which the event is assigned to.
        :type contract_no: str
        :param event_date: The date when the event was happened.
        :type event_date: datetime.date
        :param desc: Short description of the event. What was happened.
        :type desc: str
        :param attach1: The *.pdf file created by policyholder with individual content or the form of the insurance company.
        :type attach1: str
        :param attach2: The *.pdf file created by policyholder with individual content or the form of the insurance company.
        :type attach2: str
        :param created: The date and time when the event was created.
        :type created: datetime.datetime
        :param updated: The date and time when the event was updated.
        :type updated: datetime.datetime
    """
    policyholder = models.ForeignKey(PolicyHolder,
                                     on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    contract_no = models.CharField(max_length=50)
    event_date = models.DateField()
    desc = models.TextField()
    attach1 = models.FileField(upload_to='pojisteni/static/pojisteni/FILES/',
                               blank=True, null=True)
    attach2 = models.FileField(upload_to='pojisteni/static/pojisteni/FILES/',
                               blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return (self.title + " " + self.contract_no + " " +
                str(self.event_date))