
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from datetime import date
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'current_date': date.today(),
            'year': datetime.now().year,
        }
    )



def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Port, WritingAContract, ShippingCost, Payment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

@login_required
def area(request):
    contracts = WritingAContract.objects.filter(customer_addendum=request.user, completed=False)
    ports = Port.objects.all()
    payments = Payment.objects.filter(contract__customer_addendum=request.user)

    if request.method == 'POST' and request.POST.get('contract_form') == '1':
        cargo_quantity = request.POST.get('cargo_quantity')
        type_of_cargo = request.POST.get('type_of_cargo')
        port_id_with_cargo = request.POST.get('port_id_with_cargo')
        port_final_destination = request.POST.get('port_final_destination')
        temperature_mode = request.POST.get('temperature_mode')
        temperature_value = request.POST.get('temperature_value')
        temperature_unit = request.POST.get('temperature_unit')
        in_work = request.POST.get('in_work') == 'on'
        completed = request.POST.get('completed') == 'on'
        user_id = request.user.id

        # Combine temperature_mode, temperature_value, and temperature_unit
        if temperature_value is not None:
            temperature_mode += f' {temperature_value} {temperature_unit}'

        try:
            with transaction.atomic():
                contract = WritingAContract.objects.create(
                    cargo_quantity=cargo_quantity,
                    type_of_cargo=type_of_cargo,
                    port_id_with_cargo_id=port_id_with_cargo,
                    port_final_destination_id=port_final_destination,
                    temperature_mode=temperature_mode,
                    in_work=in_work,
                    completed=completed,
                    customer_addendum_id=user_id,
                    user_id=user_id
                )

                shipping_cost = ShippingCost.objects.get(cargo_type=contract.type_of_cargo)

                Payment.objects.create(
                    payment_date=None,
                    amount=Decimal(contract.cargo_quantity) * shipping_cost.cost_per_unit,
                    payment_made=False,
                    contract=contract
                )

                messages.success(request, 'Contract created successfully.')

        except ValidationError as e:
            messages.error(request, f'Validation Error: {e}')
        except Exception as e:
            messages.error(request, f'Error: {e}')

        return redirect('area')

    if request.method == 'POST' and request.POST.get('contract_form') == '0':
        payment_id = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(pk=payment_id)
            payment.payment_date = timezone.now().date()
            payment.payment_made = True
            payment.save()
            messages.success(request, 'Payment successful.')
            return redirect('area')
        except Payment.DoesNotExist:
            messages.error(request, 'Payment not found.')

    return render(request, 'app/area.html', {'contracts': contracts, 'ports': ports, 'payments': payments})



from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import CustomUser



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # ��������� ����������� ��������
                return redirect('home')  # ��������������� �� home.html
            else:
                # �������� ������� ������, ����������� ������
                return render(request, 'app/login.html', {'error_message': 'error'})
    else:
        form = AuthenticationForm()
    # ���������� ����� �����
    return render(request, 'app/login.html', {'form': form})



from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import CustomUser
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            company_name = form.cleaned_data['company_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']  # Добавлено извлечение значения для email
            
            user = CustomUser.objects.create_user(username=username, password=password, email=email)
            user.company_name = company_name
            user.first_name = first_name
            user.last_name = last_name  # Добавлено сохранение значения для last_name
            user.save()

            messages.success(request, 'You have successfully created an account. Please log in.')
            
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})



from django.contrib import messages

def delete_port(request, port_id):
    try:
        port = Port.objects.get(port_table_id=port_id)
        port.delete()
        messages.success(request, f'Port "{port.port_name}" has been deleted successfully.')
    except Port.DoesNotExist:
        messages.error(request, 'Port does not exist.')
    return redirect('admin_panel')

from django.shortcuts import render, redirect
from .models import Port
from .forms import EditPortForm

def edit_port(request, port_id):
    try:
        port = Port.objects.get(port_table_id=port_id)
    except Port.DoesNotExist:
        messages.error(request, 'Port does not exist.')
        return redirect('admin_panel')

    if request.method == 'POST':
        form = EditPortForm(request.POST, instance=port)
        if form.is_valid():
            form.save()
            messages.success(request, f'Port "{port.port_name}" has been updated successfully.')
            return redirect('admin_panel')
    else:
        form = EditPortForm(instance=port)

    return render(request, 'app/edit_port.html', {'form': form, 'port': port})



def delete_ship(request, ship_id):
    try:
        ship = Ship.objects.get(ship_table_id=ship_id)
        ship.delete()
        messages.success(request, f'Ship "{ship.name_of_vessel}" has been deleted successfully.')
    except Ship.DoesNotExist:
        messages.error(request, 'Ship does not exist.')
    return redirect('admin_panel')

from .forms import EditShipForm

def edit_ship(request, ship_id):
    try:
        ship = Ship.objects.get(ship_table_id=ship_id)
    except Ship.DoesNotExist:
        messages.error(request, 'Ship does not exist.')
        return redirect('admin_panel')

    if request.method == 'POST':
        form = EditShipForm(request.POST, instance=ship)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ship "{ship.name_of_vessel}" has been updated successfully.')
            return redirect('admin_panel')
    else:
        form = EditShipForm(instance=ship)

    return render(request, 'app/edit_ship.html', {'form': form, 'ship': ship})

import random
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone  # Import timezone module
from .models import RouteShip, CrewPayment ,WritingAContract

from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404

def change_order_completed(request, route_id):
    try:
        route = RouteShip.objects.get(pk=route_id)

        if not route.order_completed:
            route.order_completed = True
            route.save()
            
            # Check if order_completed is set to True and ship exists
            if route.order_completed and route.ship_table:
                # Calculate amount_crew based on random value, time_to_port, and crew size
                current_time = timezone.now() 
                time_to_port = route.time_to_port
                days_until_port = max((current_time - time_to_port).days, 1)

                amount_crew = max(random.randint(600, 1000) * days_until_port * route.ship_table.crew, Decimal('0.00'))

                # Create CrewPayment entry for the ship
                CrewPayment.objects.create(
                    payment_date=current_time.date(),
                    amount_crew=amount_crew,
                    ship_table=route.ship_table
                )

                messages.success(request, f'Route {route.route_key} has been marked as completed, '
                                          f'CrewPayment has been created with amount_crew={amount_crew}.')
            else:
                messages.warning(request, f'Route {route.route_key} is already marked as completed.')
    except RouteShip.DoesNotExist:
        messages.error(request, 'Route does not exist.')

    return redirect('admin_panel')





from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import WritingAContract

@login_required
def view_area(request):
    user = request.user
    area = WritingAContract.objects.filter(user=user)
    return render(request, 'area.html', {'area': area})




from django.shortcuts import render, redirect
from .models import Port, Ship, WritingAContract, Assignment, RouteShip , ShipRepair , CrewPayment

from django.shortcuts import render
from django.http import HttpResponse

def port_view(request):
    ports = Port.objects.all()
    if request.method == 'POST':
        if 'port_form' in request.POST:
            port_name = request.POST.get('port_name')
            port_latitude = request.POST.get('port_latitude')
            port_longitude = request.POST.get('port_longitude')
            # Создание и сохранение нового объекта Port
            Port.objects.create(port_name=port_name, port_latitude=port_latitude, port_longitude=port_longitude)
    context = {
        'ports': ports,   
    }

    return render(request, 'app/port.html', context)


def contact(request):
    contracts = WritingAContract.objects.all()

    paid_contracts = WritingAContract.objects.filter(payments__payment_made=True)
    if request.method == 'POST':
       if 'contract_form' in request.POST:
            cargo_quantity = request.POST.get('cargo_quantity')
            type_of_cargo = request.POST.get('type_of_cargo')
            port_id_with_cargo = request.POST.get('port_id_with_cargo')
            port_final_destination = request.POST.get('port_final_destination')
            customer_addendum = request.POST.get('customer_addendum')
            temperature_mode = request.POST.get('temperature_mode')
            in_work = request.POST.get('in_work') == 'on'
            completed = request.POST.get('completed') == 'on'
            user = request.POST.get('user')  # Ассоциируйте с соответствующим пользователем

            WritingAContract.objects.create(
                cargo_quantity=cargo_quantity,
                type_of_cargo=type_of_cargo,
                port_id_with_cargo_id=port_id_with_cargo,
                port_final_destination_id=port_final_destination,
                customer_addendum_id=customer_addendum,
                temperature_mode=temperature_mode,
                in_work=in_work,
                completed=completed,
                user_id=user
            )
            

        
       
    context = {
        'contracts': paid_contracts,
    }

    return render(request, 'app/contact.html', context)

    
def ship_view (request):
    ships = Ship.objects.all()
    ports = Port.objects.all()
    ship_repairs = ShipRepair.objects.all()
    ship_id = None
    if request.method == 'POST':
        if 'ship_form' in request.POST:
            # Обработка формы для Ship
            name_of_vessel = request.POST.get('name_of_vessel')
            ship_tonnage = request.POST.get('ship_tonnage')
            ship_type = request.POST.get('ship_type')
            home_port_id = request.POST.get('home_port')  
            average_speed = request.POST.get('average_speed')
            crew = request.POST.get('crew')
           # Получение объекта Port
            home_port = Port.objects.get(pk=home_port_id)

            # Создание объекта Ship с объектом Port
            Ship.objects.create(
                name_of_vessel=name_of_vessel, 
                ship_tonnage=ship_tonnage, 
                ship_type=ship_type, 
                home_port=home_port,  
                average_speed=average_speed,
                crew=crew
            )
        elif 'ship_repair_form' in request.POST:
              ship_id = request.POST.get('ship_id')
              repair_end_date = request.POST.get('repair_end_date')
              cost_repair = request.POST.get('cost_repair')

        try:
              ship = Ship.objects.get(pk=ship_id)
               

        
              if  RouteShip.objects.filter(ship_table=ship, order_completed=False).exists():
                 print("Error: Ship has an active route. Cannot proceed with repair.")
              else:
                 repair_start_date = date.today()
                 ShipRepair.objects.create(
                  ship=ship,
                repair_start_date=repair_start_date,
                repair_end_date=repair_end_date,
                cost_repair=cost_repair
                  )
              
                
        except Ship.DoesNotExist:
                 print("Error: Ship not found")
    context = {

        'ships': ships,
        'ship_repairs': ship_repairs,
        'ports': ports,
       
    }

    return render(request, 'app/ship.html', context)

from django.contrib import messages

def admin_panel(request):
    
    # Data Retrieval
    ships = Ship.objects.all()
    ports = Port.objects.all()
    contracts = WritingAContract.objects.all()
    crew  = CrewPayment.objects.all()
    routes = RouteShip.objects.all()
    ship_id = None
    assignments = Assignment.objects.all()
    paid_contracts = WritingAContract.objects.filter(payments__payment_made=True)
    if request.method == 'POST':

        
        if 'create_route_ships' in request.POST:
            ship_id = request.POST.get('ship_id')
            if ship_id:
               ship_id = int(ship_id)
               create_route_ships_logic(ship_id, generate_route_key)
               return redirect('admin_panel')

             # Обработка формы для Port

        if 'contract_form' in request.POST:
            cargo_quantity = request.POST.get('cargo_quantity')
            type_of_cargo = request.POST.get('type_of_cargo')
            port_id_with_cargo = request.POST.get('port_id_with_cargo')
            port_final_destination = request.POST.get('port_final_destination')
            customer_addendum = request.POST.get('customer_addendum')
            temperature_mode = request.POST.get('temperature_mode')
            in_work = request.POST.get('in_work') == 'on'
            completed = request.POST.get('completed') == 'on'
            user = request.POST.get('user')  # Ассоциируйте с соответствующим пользователем

            WritingAContract.objects.create(
                cargo_quantity=cargo_quantity,
                type_of_cargo=type_of_cargo,
                port_id_with_cargo_id=port_id_with_cargo,
                port_final_destination_id=port_final_destination,
                customer_addendum_id=customer_addendum,
                temperature_mode=temperature_mode,
                in_work=in_work,
                completed=completed,
                user_id=user
            )
        
        elif 'assignment_form' in request.POST:
             contract_id = request.POST.get('contract')
             ship_table_id = request.POST.get('ship_table')

             try:
                contract = WritingAContract.objects.get(pk=contract_id, completed=False)
                ship_table = Ship.objects.get(pk=ship_table_id)

                latest_assignment = Assignment.objects.filter(ship_table=ship_table, contract__completed=False).order_by('-id').first()
                current_load = ship_table.ship_tonnage if not latest_assignment else latest_assignment.vessel_load_calculation
                new_load = max(0, current_load - contract.cargo_quantity)

                print("Contract:", contract)
                print("Ship Table:", ship_table)
                print("New Vessel Load Calculation:", new_load)

                Assignment.objects.create(
                   contract=contract,
                   ship_table=ship_table,
                  vessel_load_calculation=new_load
                )
                contract.in_work = True
                contract.save()

             except (WritingAContract.DoesNotExist, Ship.DoesNotExist) as e:
                print("Error:", e)
                return redirect('admin_panel')

             
        
        # Обработка формы для RouteShip
        elif 'route_form' in request.POST:
            ship_table = request.POST.get('ship_table')
            from_the_port = request.POST.get('from_the_port')
            to_the_port = request.POST.get('to_the_port')
            voyage_duration = request.POST.get('voyage_duration')
            time_to_port = request.POST.get('time_to_port')
            order_completed = request.POST.get('order_completed') == 'on'

            RouteShip.objects.create(
                ship_table_id=ship_table,
                from_the_port_id=from_the_port,
                to_the_port_id=to_the_port,
                voyage_duration=voyage_duration,
                time_to_port=time_to_port,
                order_completed=order_completed
            )
                    # Получение объекта судна для обработки
            ship = Ship.objects.get(pk=ship_table_id)

    # Context Preparation
    context = {

        'routes': routes,
         'CrewPayment': CrewPayment,
         'assignments': assignments,
         'contracts': paid_contracts,
         'ships': ships,
         'ports': ports

    }

    return render(request, 'app/admin_panel.html', context)
   




from django.shortcuts import render, redirect
from .models import Port, Ship, WritingAContract, Assignment, RouteShip
from django.utils import timezone
from geopy.distance import geodesic
from datetime import timedelta

from django.db.models import Sum

from django.db import transaction
from django.db.models import Max


def generate_route_key(path_index, stop_index):
    return f"{stop_index}-{path_index}"



def create_route_ships_logic(ship_id, generate_route_key):
    ship = Ship.objects.get(pk=ship_id)
    contracts = WritingAContract.objects.filter(
        assignment__ship_table=ship,
        completed=False
    ).order_by('contract_id').distinct()

    with transaction.atomic():
        last_route = RouteShip.objects.filter(ship_table=ship).order_by('-route_key').first()

        if not last_route:
            path_index = 1
        else:
            last_route_parts = last_route.route_key.split('-')
            path_index = int(last_route_parts[0]) + 1 if len(last_route_parts) > 0 else 1

        last_time_to_port = timezone.now()
        created_paths = set()

        for contract in contracts:
            current_path = f"{contract.port_id_with_cargo_id}-{contract.port_final_destination_id}"

            if current_path not in created_paths:
                stop_index = 1
                if ship.home_port_id != contract.port_id_with_cargo_id:
                    last_time_to_port, stop_index, path_index = create_route(ship, ship.home_port_id, contract.port_id_with_cargo_id, last_time_to_port, path_index, stop_index, generate_route_key)

                last_time_to_port, stop_index, path_index = create_route(ship, contract.port_id_with_cargo_id, contract.port_final_destination_id, last_time_to_port, path_index, stop_index, generate_route_key)

                ship.home_port_id = contract.port_final_destination_id
                created_paths.add(current_path)

        # Здесь path_index увеличивается на 1 для каждого нового маршрута
        path_index += 1

        assignments_to_delete = Assignment.objects.filter(ship_table_id=ship_id)
        assignments_to_delete.delete()

    return redirect('admin_panel')


def create_route(ship, from_port_id, to_port_id, last_time_to_port, path_index, stop_index, generate_route_key):
    from_port = Port.objects.get(pk=from_port_id)
    to_port = Port.objects.get(pk=to_port_id)

    from_coords = (from_port.port_latitude, from_port.port_longitude)
    to_coords = (to_port.port_latitude, to_port.port_longitude)

    distance = geodesic(from_coords, to_coords).kilometers
    voyage_duration = calculate_voyage_duration(distance, ship.average_speed)

    time_to_port = last_time_to_port + timedelta(hours=voyage_duration)
    route_key = generate_route_key(path_index, stop_index)

    while RouteShip.objects.filter(route_key=route_key).exists():
        stop_index += 1
        route_key = generate_route_key(path_index, stop_index)

    RouteShip.objects.create(
        ship_table=ship,
        from_the_port=from_port,
        to_the_port=to_port,
        voyage_duration=voyage_duration,
        time_to_port=time_to_port,
        order_completed=False,
        route_key=route_key
    )

    # Увеличиваем path_index при каждом новом маршруте
    path_index += 1

    return time_to_port, stop_index, path_index


def calculate_voyage_duration(distance, average_speed):
    average_speed_float = float(average_speed)
    return distance / average_speed_float if average_speed_float else 0


from django.shortcuts import render, redirect
from .models import RouteShip

from django.shortcuts import render
from .models import RouteShip

def route_ships_page(request):
    routes = RouteShip.objects.all()

    # Группировка маршрутов по ключу маршрута
    route_groups = {}
    for route in routes:
        route_key = route.route_key.split('-')[0]  # Получаем часть маршрута до тире
        if route_key not in route_groups:
            route_groups[route_key] = {'route_key': route_key, 'routes': []}
        route_groups[route_key]['routes'].append(route)

    return render(request, 'app/route_ships_page.html', {'route_groups': route_groups.values()})


from django.shortcuts import render, redirect, get_object_or_404
from .models import RouteShip

def change_completed(request, pk):
    if request.method == 'POST':
        route_ship = get_object_or_404(RouteShip, pk=pk)
        route_ship.order_completed = True
        route_ship.save()
        return redirect('route_ships_page')  # Перенаправляем на нужную страницу после изменения

    return redirect('route_ships_page')  # Перенаправляем на нужную страницу в случае некорректного запроса





import plotly.graph_objects as go
import pandas as pd
from django.shortcuts import render
from .models import WritingAContract

def get_contract_data():
    # Query data from Django ORM
    contracts = WritingAContract.objects.all()

    # Convert data to a pandas DataFrame
    df_contracts = pd.DataFrame(list(contracts.values()))

    return df_contracts

def generate_pie_chart(df_contracts):
    # Group by cargo type and calculate count and sum of cargo_quantity
    grouped_data = df_contracts.groupby('type_of_cargo').agg({'cargo_quantity': ['count', 'sum']}).reset_index()

    # Rename columns for clarity
    grouped_data.columns = ['type_of_cargo', 'order_count', 'total_cargo_quantity']

    # Calculate percentage of orders for each cargo type
    grouped_data['order_percentage'] = grouped_data['order_count'] / grouped_data['order_count'].sum() * 100

    # Create a pie chart
    fig_pie = go.Figure()

    # Add trace for each cargo type
    for index, row in grouped_data.iterrows():
        fig_pie.add_trace(go.Pie(labels=[row['type_of_cargo']],
                                 values=[row['order_percentage']],
                                 textinfo='label+percent',
                                 hoverinfo='label+value+percent',
                                 name=row['type_of_cargo']))

    # Update layout for better visualization
    fig_pie.update_layout(title='Orders by Cargo Type')

 
    plot_div_pie = fig_pie.to_html(full_html=False)

    return plot_div_pie



def get_monthly_data(queryset, date_column='payment_date', amount_column='amount'):
    queryset[date_column] = pd.to_datetime(queryset[date_column])
    queryset['month'] = queryset[date_column].dt.to_period('M')
    monthly_data = queryset.groupby('month')[amount_column].sum().reset_index()
    monthly_data['month'] = monthly_data['month'].astype(str)
    return monthly_data


def get_contract_data():
    contracts = WritingAContract.objects.all()
    df_contracts = pd.DataFrame(list(contracts.values()))
    return df_contracts

def generate_vertical_bar_chart(df_contracts):
    # Calculate total orders and total tons
    total_orders = len(df_contracts)
    total_tons = df_contracts['cargo_quantity'].sum()

    # Calculate the percentage of each category
    df_percentage = df_contracts.groupby('type_of_cargo')['cargo_quantity'].sum() / total_tons * 100
    df_percentage = df_percentage.reset_index()

    # Create vertical bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(x=df_percentage['type_of_cargo'], y=df_percentage['cargo_quantity'], marker_color=['green', 'red', 'blue']))

    fig.update_layout(title='Cargo Distribution',
                      xaxis_title='Cargo Type',
                      yaxis_title='Tons',
                      barmode='stack',  # Stack bars on top of each other
                      bargap=0.2)  # Adjust the bargap as needed

    return fig.to_html(full_html=False)

def statistics(request):
    payments = Payment.objects.all()
    ship_repairs = ShipRepair.objects.all()
    crew_payments = CrewPayment.objects.all()

    df_payments = pd.DataFrame(list(payments.values()))
    df_ship_repairs = pd.DataFrame(list(ship_repairs.values()))
    df_crew_payments = pd.DataFrame(list(crew_payments.values()))

    monthly_payment_data = get_monthly_data(df_payments, 'payment_date', 'amount')
    monthly_ship_repair_data = get_monthly_data(df_ship_repairs, 'repair_start_date', 'cost_repair')
    monthly_crew_payment_data = get_monthly_data(df_crew_payments, 'payment_date', 'amount_crew')

    # Create bar chart with three traces (payments, ship repairs, crew payments)
    fig = go.Figure()

    # Payments (Green)
    fig.add_trace(go.Bar(x=monthly_payment_data['month'], y=monthly_payment_data['amount'], name='Payments', marker_color='green'))

    # Ship Repairs (Red)
    fig.add_trace(go.Bar(x=monthly_ship_repair_data['month'], y=monthly_ship_repair_data['cost_repair'], name='Ship Repairs', marker_color='red'))

    # Crew Payments (Gray)
    fig.add_trace(go.Bar(x=monthly_crew_payment_data['month'], y=monthly_crew_payment_data['amount_crew'], name='Crew Payments', marker_color='gray'))

    # Update layout for better visualization
    fig.update_layout(title='Monthly Statistics',
                      xaxis_title='Month',
                      yaxis_title='Amount',
                      barmode='group',
                      bargap=0.5)  # Adjust the bargap as needed

    df_contracts = get_contract_data()
    plot_div_pie = generate_pie_chart(df_contracts)
    plot_div_vertical_bar = generate_vertical_bar_chart(df_contracts)

    # Convert Plotly objects to HTML
    plot_div = fig.to_html(full_html=False)

    context = {
        'plot_div': plot_div,
        'plot_div_vertical_bar': plot_div_vertical_bar,
        'selected_month': request.GET.get('selected_month', ''),
    }

    return render(request, 'app/statistics.html', context)

