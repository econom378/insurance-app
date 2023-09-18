from django.shortcuts import render, redirect
from .models import PolicyHolder, InsuranceModel, EventModel
from .forms import PolicyHolderForm, InsuranceModelForm, EventModelForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
import logging
from django.core.paginator import Paginator
import math, re
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


#error logging in file "pojisteni.log"
logger = logging.getLogger(__name__)

#rendering pdf report
def render_pdf_view(request):
    """
        This view renders the report as a *.pdf file either view in browser or downloadable file.

        :param total_policyholders: The number of policyholders to be populated in the report
        :type total_policyholders: int
        :param total_insurances: The number of insurances to be populated in the report
        :type total_insurances: int
        :param total_events: The number of events to be populated in the report
        :type total_events: int
        :param template: The path to template to be rendered.
        :type template: str
    """
    total_policyholders = PolicyHolder.objects.all().count()
    total_insurances = InsuranceModel.objects.all().count()
    total_events = EventModel.objects.all().count()

    template_path = 'pojisteni/pdf_report.html'
    context = {
        "obj_ph": total_policyholders,
        "obj_ins": total_insurances,
        "obj_ev": total_events
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #the file to be downloaded
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #the file to be shown as pdf in browser
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, encoding='UTF-8')
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('Vyskytly se chyby <pre>' + html + '</pre>')
    return response




#CRUD - READ policyholders
def policyholders(request):
    """
        Display a list of policyholders.

        This view retrieves a list of policyholders from the database and renders
        them using the 'policyholder_list.html' template. There is also pagination to view
        records from database more user friendly.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param page_amount: settings - how many records will be populated in one page in template
        :type: int
        :param policyholder_paginator: instance of Django class Paginator
        :type: django.core.paginator.Paginator
        :param num_of_pages: total number of pages
        :type: int
        :param pages: list generated for template related to total number of pages
        :type: list
        :param page_num: page number sent by user via url
        :type: int
        :return: A rendered HTML response displaying the list of policyholders.
        :rtype: django.http.HttpResponse
    """
    policyholders = PolicyHolder.objects.all()

    #pagination <<-----------------
    page_amount = 10
    policyholder_paginator = Paginator(policyholders, page_amount)
    num_of_pages = math.ceil(policyholder_paginator.count / page_amount)
    pages = list(range(1, num_of_pages + 1))
    page_num = request.GET.get('page')

    if page_num == None:
        page_num = 1
    else:
        page_num = int(page_num)

    page = policyholder_paginator.get_page(page_num)
    #------------------------------->>>

    template = 'pojisteni/policyholder_list.html'
    context = {
        'obj': page,
        'count': policyholder_paginator.count,
        'pages': pages,
        'page_num': page_num
    }

    return render(request, template, context)

#CRUD - READ policyholder detail
def policyholder_detail(request, pk):
    """
        Display the details of a Policyholder instance.

        This view retrieves the details of a Policyholder instance with the specified primary key (pk)
        from the database and renders them using the 'policyholder_detail.html' template.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the MyModel instance to be displayed.
        :type pk: int
        :return: A rendered HTML response displaying the details of the Policyholder instance.
        :rtype: django.http.HttpResponse
    """
    policyholder_detail = PolicyHolder.objects.get(id = pk)
    insurance = InsuranceModel.objects.filter(policyholder=policyholder_detail)
    event = EventModel.objects.filter(policyholder=policyholder_detail)
    template = 'pojisteni/policyholder_detail.html'
    context = {
        'obj': policyholder_detail,     #policyholder object
        "ins_obj": insurance,           #insurance object
        "event_obj": event              #event object
    }
    return render(request, template, context)


#CRUD - CREATE policyholder under authentification
@login_required(login_url='login')
def create_policyholder(request):
    """
        Create a new instance of Policyholder.

        This view handles the creation of a new instance of Policyholder based on user input.
        If the form is valid and the instance is successfully created, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :return: A rendered HTML response displaying the create form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    form = PolicyHolderForm()
    if request.method == 'POST':
        form = PolicyHolderForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    novy_policyholder = form.save(commit=False)
                    novy_policyholder.name = form.cleaned_data.get(
                        'name').title()
                    novy_policyholder.lastname = form.cleaned_data.get(
                        'lastname').title()
                    novy_policyholder.save()
                    #form.save_m2m() - only in case of many to many fields

                messages.success(request, 'Entry was created successfully')
                return redirect('policyholder_list')
            except Exception as e:
                messages.error(request, f'Chyba: {str(e)}')
                logger.error(f"Error occurred during entry create: {e}")
    else:
        form = PolicyHolderForm()


    template = 'pojisteni/create_policyholder.html'
    context = {
        'form': form
    }
    return render(request, template, context)


#CRUD - UPDATE policyholder under authentification
@login_required(login_url='login')
def update_policyholder(request,pk):
    """
        Update an instance of Policyholder.

        This view handles the update of an existing instance of Policyholder based on user input.
        If the form is valid and the instance is successfully updated, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance to be updated.
        :type pk: int
        :return: A rendered HTML response displaying the update form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    policyholder = PolicyHolder.objects.get(id=pk)
    form = PolicyHolderForm(instance=policyholder)
    if request.method == 'POST':
        form = PolicyHolderForm(request.POST, request.FILES,
                                instance=policyholder)
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_policyholder = form.save(commit=False)
                    updated_policyholder.name = form.cleaned_data.get(
                        'name').title()
                    updated_policyholder.lastname = form.cleaned_data.get(
                        'lastname').title()
                    updated_policyholder.save()
                    #form.save_m2m() - only in case of many to many fields

                messages.success(request, 'Entry was updated successfully')
                return redirect('policyholder_list')
            except Exception as e:
                messages.error(request, f'Chyba: {str(e)}')
                logger.error(f"Error occurred during entry update: {e}")

    else:
        form = PolicyHolderForm(instance=policyholder)

    template = 'pojisteni/update_policyholder.html'
    context = {
        'form': form,
        'obj': policyholder
    }
    return render(request, template, context)


#CRUD - DELETE policyholder under authentification
@login_required(login_url='login')
def delete_policyholder(request,pk):
    """
        Delete an instance of Policyholder.

        This view handles the delete of an existing instance of IPolicyholder based on user input.
        If the form is valid and the instance is successfully updated, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance to be deleted.
        :type pk: int
        :return: A rendered HTML response displaying the update form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    policyholder = PolicyHolder.objects.get(id=pk)
    if request.method == 'POST':
        try:
            policyholder.delete()
            messages.success(request,'Entry was deleted successfully....!!!')
            return redirect('policyholder_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            logger.error(f"Error occurred during entry delete: {e}")


    template = 'pojisteni/delete_policyholder.html'
    context = {
        'obj': policyholder
    }
    return render(request, template, context)


#CRUD - READ insurances
def insurances(request):
    """
        Display a list of insurances.

        This view retrieves a list of insurances from the database and renders
        them using the 'insurance_list.html' template. There is also pagination to view
        records from database more user friendly.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param page_amount: settings - how many records will be populated in one page in template
        :type: int
        :param policyholder_paginator: instance of Django class Paginator
        :type: django.core.paginator.Paginator
        :param num_of_pages: total number of pages
        :type: int
        :param pages: list generated for template related to total number of pages
        :type: list
        :param page_num: page number sent by user via url
        :type: int
        :return: A rendered HTML response displaying the list of insurances.
        :rtype: django.http.HttpResponse
    """
    insurances = InsuranceModel.objects.all()
    #pagination   <<--------------------
    page_amount = 10
    insurance_paginator = Paginator(insurances, page_amount)
    num_of_pages = math.ceil(insurance_paginator.count / page_amount)
    pages = list(range(1, num_of_pages + 1))
    page_num = request.GET.get('page')

    if page_num == None:
        page_num = 1
    else:
        page_num = int(page_num)

    page = insurance_paginator.get_page(page_num)
    #----------------------------->>

    template = 'pojisteni/insurance_list.html'
    context = {
        'obj': page,
        'count': insurance_paginator.count,
        'pages': pages,
        'page_num': page_num
    }

    return render(request, template, context)


#CRUD - READ detail insurance
def insurance_detail(request, pk):
    """
        Display the details of a InsuranceModel instance.

        This view retrieves the details of a InsuranceModel instance with the specified primary key (pk)
        from the database and renders them using the 'insurance_detail.html' template.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the MyModel instance to be displayed.
        :type pk: int
        :return: A rendered HTML response displaying the details of the InsuranceModel instance.
        :rtype: django.http.HttpResponse
    """
    insurance_detail = InsuranceModel.objects.get(id = pk)
    template = 'pojisteni/insurance_detail.html'
    context = {
        'obj': insurance_detail
    }
    return render(request, template, context)


#CRUD - CREATE insurance under authentification
@login_required(login_url='login')
def create_insurance(request, pk):
    """
        Create a new instance of InsuranceModel of specified policyholder.

        This view handles the creation of a new instance of InsuranceModel based on user input.
        If the form is valid and the instance is successfully created, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance for whom the insurance to be created.
        :type pk: int
        :return: A rendered HTML response displaying the create form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    form = InsuranceModelForm()
    policyholder = PolicyHolder.objects.get(id=pk)
    print(policyholder)
    print(request.POST)

    if request.method == 'POST':
        form = InsuranceModelForm(request.POST)
        print(request.POST.get('paid_by'))
        if form.is_valid():
            try:
                with transaction.atomic():
                    novy_insurance = form.save(commit=False)
                    novy_insurance.policyholder = policyholder
                    novy_insurance.save()
                    #form.save_m2m() - only in case of many to many fields

                messages.success(request, 'Entry was created successfully')
                return redirect('insurance_list')
            except Exception as e:
                messages.error(request, f'Chyba: {str(e)}')
                logger.error(f"Error occurred during entry create: {e}")
        else:
            messages.error(request,'form is not valid')
    else:
        form = InsuranceModelForm()

    template = 'pojisteni/create_insurance.html'
    context = {
        'form': form,
        'obj' : policyholder
    }
    return render(request, template, context)


#CRUD - UPDATE insurance
@login_required(login_url='login')
def update_insurance(request,pk):
    """
        Update an instance of InsuranceModel.

        This view handles the update of an existing instance of InsuranceModel based on user input.
        If the form is valid and the instance is successfully updated, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance for whom the insurance to be updated.
        :type pk: int
        :return: A rendered HTML response displaying the update form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    insurance_obj = InsuranceModel.objects.get(id=pk)
    policyholder = insurance_obj.policyholder
    form = InsuranceModelForm(instance=insurance_obj)
    if request.method == 'POST':
        form = InsuranceModelForm(request.POST,instance=insurance_obj)
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_insurance = form.save(commit=False)

                    # validace dat
                    # ...

                    updated_insurance.save()
                    #form.save_m2m() - only in case of many to many fields

                messages.success(request, 'Entry was updated successfully')
                return redirect('insurance_list')
            except Exception as e:
                messages.error(request, f'Chyba: {str(e)}')
                logger.error(f"Error occurred during entry update: {e}")

    else:
        form = InsuranceModelForm(instance=insurance_obj)

    template = 'pojisteni/update_insurance.html'
    context = {
        'form': form,
        'obj' : policyholder
    }
    return render(request, template, context)


#CRUD - DELETE insurance
@login_required(login_url='login')
def delete_insurance(request,pk):
    """
        Delete an instance of InsuranceModel of specified policyholder.

        This view handles the delete of an existing instance of InsuranceModel based on user input.
        If the form is valid and the instance is successfully updated, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance for whom the insurance to be deleted.
        :type pk: int
        :return: A rendered HTML response displaying the update form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    insurance_obj = InsuranceModel.objects.get(id=pk)
    if request.method == 'POST':
        try:
            insurance_obj.delete()
            messages.success(request,'Entry was deleted successfully....!!!')
            return redirect('insurance_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            logger.error(f"Error occurred during entry delete: {e}")


    template = 'pojisteni/delete_insurance.html'
    context = {
        'obj': insurance_obj
    }
    return render(request, template, context)



#CRUD - READ events
def events(request):
    """
        Display a list of events.

        This view retrieves a list of events from the database and renders
        them using the 'event_list.html' template. There is also pagination to view
        records from database more user friendly.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param page_amount: settings - how many records will be populated in one page in template
        :type: int
        :param policyholder_paginator: instance of Django class Paginator
        :type: django.core.paginator.Paginator
        :param num_of_pages: total number of pages
        :type: int
        :param pages: list generated for template related to total number of pages
        :type: list
        :param page_num: page number sent by user via url
        :type: int
        :return: A rendered HTML response displaying the list of events.
        :rtype: django.http.HttpResponse
    """
    events = EventModel.objects.all()
    # pagination   <<--------------------
    page_amount = 10
    event_paginator = Paginator(events,page_amount)
    num_of_pages = math.ceil(event_paginator.count / page_amount)
    pages = list(range(1,num_of_pages+1))

    page_num = request.GET.get('page')
    if page_num == None:
        page_num = 1
    else:
        page_num = int(page_num)

    page = event_paginator.get_page(page_num)
    #--------------------------------->>

    template = 'pojisteni/event_list.html'
    context = {
        'obj': page,
        'count': event_paginator.count,
        'pages': pages,
        'page_num': page_num
    }
    return render(request, template, context)


#CRUD - READ detail events
def event_detail(request, pk):
    """
        Display the details of a EventModel instance.

        This view retrieves the details of a EventModel instance with the specified primary key (pk)
        from the database and renders them using the 'event_detail.html' template.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the MyModel instance to be displayed.
        :type pk: int
        :return: A rendered HTML response displaying the details of the EventModel instance.
        :rtype: django.http.HttpResponse
    """
    event_detail = EventModel.objects.get(id = pk)
    if event_detail.attach1:
        attachment_name1 = str(event_detail.attach1.path).split("\\").pop()
    else:
        attachment_name1 = None

    if event_detail.attach2:
        attachment_name2 = str(event_detail.attach2.path).split("\\").pop()
    else:
        attachment_name2 = None

    template = 'pojisteni/event_detail.html'
    context = {
        'obj': event_detail,
        'name1':attachment_name1,
        'name2': attachment_name2
    }
    return render(request, template, context)



#CRUD - CREATE events
@login_required(login_url='login')
def create_event(request, pk):
    """
        Create a new instance of EventModel of specified policyholder.

        This view handles the creation of a new instance of EventModel based on user input.
        If the form is valid and the instance is successfully created, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance for whom the event to be created.
        :type pk: int
        :return: A rendered HTML response displaying the create form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    form = EventModelForm()
    policyholder = PolicyHolder.objects.get(id=pk)


    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    novy_event = form.save(commit=False)
                    novy_event.policyholder = policyholder

                    #validace dat
                    #...

                    novy_event.save()
                    #form.save_m2m() - only in case of many to many fields

                messages.success(request, 'Entry was created successfully')
                return redirect('event_list')
            except Exception as e:
                messages.error(request, f'Chyba: {str(e)}')
                logger.error(f"Error occurred during entry create: {e}")
    else:
        form = EventModelForm()


    template = 'pojisteni/create_event.html'
    context = {
        'form': form,
        'obj' : policyholder
    }
    return render(request, template, context)


#CRUD - UPDATE events
@login_required(login_url='login')
def update_event(request,pk):
    """
        Update an instance of EventModel.

        This view handles the update of an existing instance of EventModel based on user input.
        If the form is valid and the instance is successfully updated, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance for whom the event to be updated.
        :type pk: int
        :return: A rendered HTML response displaying the update form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    event_obj = EventModel.objects.get(id=pk)
    policyholder = event_obj.policyholder
    form = EventModelForm(instance=event_obj)
    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES,
                                  instance=event_obj)
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_event = form.save(commit=False)

                    # validace dat
                    # ...
                    updated_event.title = form.cleaned_data.get(
                        'title').capitalize()
                    updated_event.save()
                    #form.save_m2m() - only in case of many to many fields

                messages.success(request, 'Entry was updated successfully')
                return redirect('event_list')
            except Exception as e:
                messages.error(request, f'Chyba: {str(e)}')
                logger.error(f"Error occurred during entry update: {e}")

    else:
        form = EventModelForm(instance=event_obj)

    template = 'pojisteni/update_event.html'
    context = {
        'form': form,
        'obj' : policyholder
    }
    return render(request, template, context)


#CRUD - DELETE events
@login_required(login_url='login')
def delete_event(request,pk):
    """
        Delete an instance of EventModel of specified policyholder.

        This view handles the delete of an existing instance of EventModel based on user input.
        If the form is valid and the instance is successfully updated, a success message
        is displayed. If there are validation errors, they are displayed as error messages.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :param pk: The primary key of the Policyholder instance for whom the event to be deleted.
        :type pk: int
        :return: A rendered HTML response displaying the update form or a redirect response
                 with a success message.
        :rtype: django.http.HttpResponse
    """
    event_obj = EventModel.objects.get(id=pk)
    if request.method == 'POST':
        try:
            event_obj.delete()
            messages.success(request,'Entry was deleted successfully....!!!')
            return redirect('event_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            logger.error(f"Error occurred during entry delete: {e}")


    template = 'pojisteni/delete_event.html'
    context = {
        'obj': event_obj
    }
    return render(request, template, context)

#user registration
def user_register(request):
    """
        Register a new user.

        This view handles the registration of a new user. It accepts POST requests with user
        registration data and tries to create a new user account. If registration is successful,
        the user is redirected to policyholder list page and login is required, and a success message is displayed. If there are validation errors
        or registration fails, an error message is displayed.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :page: specifies the type of form - Login/Register
        :type: str
        :return: A rendered HTML response displaying the registration form or a redirect response
                 with a success message or an error message.
        :rtype: django.http.HttpResponse
    """
    page = 'register'

    template = 'pojisteni/login_register.html'

    context = {
        "page": page
    }

    if request.method == 'POST':

        user = User()
        user.username = request.POST.get('username')
        user.password1 = request.POST.get('password1')
        user.password2 = request.POST.get('password2')

        #server side password validation (password is also validated in the registration form)
        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(.{8,})$', user.password1):
            messages.error(request,"Heslo musí obsahovat jedno malé a jedno velké písmeno a musí být min. 8 znaků dlouhé...")
            return redirect('register')

        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(.{8,})$', user.password2):
            messages.error(request,"Heslo musí obsahovat jedno malé a jedno velké písmeno a musí být min. 8 znaků dlouhé...")
            return redirect('register')

        if user.password1 == user.password2:
            user.set_password(user.password1)
        else:
            messages.error(request, 'Hesla nejsou totožná!!!')
            return redirect('register')

        try:
            user.save()
            return redirect('policyholder_list')
        except:
            messages.error(request, 'Registrace selhala!!!')


    return render(request, template, context)

#user login
def user_login(request):
    """
        Login an user.

        This view handles the login of an user. It accepts POST requests with user
        login data and tries to match login data with existing user account. If login is successful,
        the user is redirected to policyholder list page, and username is displayed. If there are validation errors
        or registration fails, an error message is displayed.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :page: specifies the type of form - Login/Register
        :type: str
        :return: A rendered HTML response displaying the registration form or a redirect response
                 with a success message or an error message.
        :rtype: django.http.HttpResponse
    """

    if request.user.is_authenticated:
        return redirect('policyholder_list')

    page = 'login'

    template = "pojisteni/login_register.html"
    context = {
        "page": page
    }

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('policyholder_list')
        else:
            messages.error(request, 'USERNAME or PASSWORD does not exists!')

    return render(request, template, context)

def user_logout(request):
    """
        Log out the currently authenticated user.

        This view logs out the currently authenticated user and redirects them to the
        policyholder list page. Username in template is switched to Login/Register menu option.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :return: A redirect response to the home page with a success message.
        :rtype: django.http.HttpResponseRedirect
    """
    logout(request)
    return redirect('policyholder_list')
