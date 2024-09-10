from django.shortcuts import render, redirect
from .models import ConsultancyCategory, Booking, TimeSlot, Date, PaymentRecord
from .forms import BookingForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# Public Home Page
def category_list(request):
    categories = ConsultancyCategory.objects.all()
    return render(request, 'booking/category_list.html', {'categories': categories})

# Booking Slot View - Restricted to Authenticated Users
@login_required
def book_slot(request, category_id):
    category = ConsultancyCategory.objects.get(id=category_id)
    time_slots = TimeSlot.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['date']
            selected_slot_id = request.POST.get('time_slot')
            selected_slot = TimeSlot.objects.get(id=selected_slot_id)
            if not Date.objects.filter(date=booking_date).exists():
                form.add_error('date', 'The selected date is not available for booking.')
            elif Booking.objects.filter(date=booking_date, category=category, time_slot=selected_slot).exists():
                form.add_error('time_slot', 'This time slot is already booked.')
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.category = category
                booking.time_slot = selected_slot
                booking.save()
                return redirect('initiate_payment', booking_id=booking.id)
    else:
        form = BookingForm()

    dates = Date.objects.all().order_by('date')
    return render(request, 'booking/book_slot.html', {
        'form': form,
        'category': category,
        'time_slots': time_slots,
        'dates': dates
    })

# Confirmation Page
@login_required
def confirmation(request):
    return render(request, 'booking/confirmation.html')

# User Registration - Public
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking/register.html', {'form': form})

# User Login - Public
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('category_list')
    else:
        form = AuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})

# User Logout - Restricted to Authenticated Users
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Payment Initiation - Restricted to Authenticated Users
@login_required
def initiate_payment(request, booking_id):
    client = razorpay.Client(auth=(keyID, keySecret))
    booking = Booking.objects.get(id=booking_id)
    order_amount = 100  # Amount in paise, adjust as needed
    razorpay_order = client.order.create({
        'amount': order_amount,
        'currency': 'INR',
        'payment_capture': '1'
    })
    
    context = {
        'order_id': razorpay_order['id'],
        'amount': order_amount,
        'currency': 'INR',
        'razorpay_key': keyID,
        'booking_id': booking_id
    }
    
    return render(request, 'booking/payment.html', context)

# Payment Callback - Restricted to Authenticated Users
@csrf_exempt
@login_required
def payment_callback(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        booking_id = request.POST.get('booking_id')
        booking = Booking.objects.get(id=booking_id)
        booking_date = booking.date
        booking_slot = booking.time_slot.slot
        date_instance = Date.objects.get(date=booking_date)
        date_instance.mark_slot_as_booked(booking_slot)
        client = razorpay.Client(auth=(keyID, keySecret))
        try:
            client.utility.verify_payment_signature({
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature
            })
            PaymentRecord.objects.create(
                user=request.user,
                booking_id=booking_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                amount=booking.amount,
                currency='INR',
                status='Success'
            )
            booking.is_booked = True
            booking.save()
            return redirect('success_page', booking_id=booking_id)
        
        except Exception as e:
            PaymentRecord.objects.create(
                user=request.user,
                booking_id=booking_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                amount=booking.amount,
                currency='INR',
                status='Failure'
            )
            return JsonResponse({'status': 'failure', 'message': str(e)})
    return JsonResponse({'status': 'failure', 'message': 'Invalid request'})

# Payment History - Restricted to Authenticated Users
@login_required
def payment_history(request):
    payment_histories = PaymentRecord.objects.filter(user=request.user)
    return render(request, 'payment_history.html', {'payment_histories': payment_histories})

# Payment Success Page - Restricted to Authenticated Users
@login_required
def success_page(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    payment_record = PaymentRecord.objects.filter(booking_id=booking_id).last()

    context = {
        'booking': booking,
        'payment_record': payment_record,
    }

    return render(request, 'success.html', context)

# Download PDF - Restricted to Authenticated Users
@login_required
def download_pdf(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    payment_record = PaymentRecord.objects.filter(booking_id=booking_id).last()
    
    context = {
        'booking': booking,
        'payment_record': payment_record,
    }

    html = render_to_string('pdf_template.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking_id}.pdf"'
    
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response

# Admin Views - Restricted to Superusers
@login_required
@user_passes_test(lambda u: u.is_superuser)
def upcoming_bookings(request):
    bookings = Booking.objects.filter(is_booked=True).select_related('category', 'time_slot')
    payment_records = PaymentRecord.objects.all()

    return render(request, 'upcoming_bookings.html', {
        'bookings': bookings,
        'payment_records': payment_records
    }) 

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_slots(request):
    dates = Date.objects.all().order_by('date')

    if request.method == "POST":
        last_date = dates.last().date if dates.exists() else datetime.today().date()
        for i in range(1, 8):
            Date.objects.create(date=last_date + timedelta(days=i))

        return redirect('manage_slots')

    return render(request, 'admin/manage_slots.html', {'dates': dates})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def set_all_unavailable(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        try:
            date_obj = Date.objects.get(date=selected_date)
            date_obj.slot_10_1030 = 'Unavailable'
            date_obj.slot_1030_11 = 'Unavailable'
            date_obj.slot_11_1130 = 'Unavailable'
            date_obj.slot_1130_12 = 'Unavailable'
            date_obj.slot_12_1230 = 'Unavailable'
            date_obj.slot_1230_1 = 'Unavailable'
            date_obj.slot_1_130 = 'Unavailable'
            date_obj.slot_130_2 = 'Unavailable'
            date_obj.slot_2_230 = 'Unavailable'
            date_obj.slot_230_3 = 'Unavailable'
            date_obj.slot_3_330 = 'Unavailable'
            date_obj.slot_330_4 = 'Unavailable'
            date_obj.slot_4_430 = 'Unavailable'
            date_obj.save()
        except Date.DoesNotExist:
            return HttpResponse('Date not found.')

        return redirect('manage_slots')

    return render(request, 'admin/set_all_unavailable.html')
