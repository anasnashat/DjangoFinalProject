from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import stripe
from django.urls import reverse

from donation_project import settings
from .models import Payment
from projects.models import Project


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_donation_session(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host():
        image_url = "https://via.placeholder.com/300"
    else:
        image_url = request.build_absolute_uri(project.image.url)

    donation_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Donation to {project.title}',
                    'images': [image_url],
                },
                'unit_amount': 1000,
            },
            'quantity': 1,
        }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment-success', kwargs={'slug': project.slug})
        ) + "?session_id={CHECKOUT_SESSION_ID}",

        cancel_url=request.build_absolute_uri(
            reverse('project-detail', kwargs={'slug': project.slug})
        ),
        metadata={'project_id': project.id, 'user_id': request.user.id},
    )
    return redirect(donation_session.url)



@login_required
def payment_success(request, slug):
    project = get_object_or_404(Project, slug=slug)
    session_id = request.GET.get('session_id')

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        # print(session)
        if session.payment_status == 'paid':
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

            if not Payment.objects.filter(stripe_payment_id=payment_intent.id, user=request.user).exists():
                payment  = Payment.objects.create(
                    project=project,
                    user=request.user,
                    amount=payment_intent.amount / 100,
                    status=payment_intent.status,
                    stripe_payment_id=payment_intent.id
                )

                print(payment)
            print("exist")


    return render(request, 'payments/success.html', {'project': project})


