from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import stripe
from django.urls import reverse
from donation_project import settings
from payments.models import Payment
from projects.models import Project


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_donation_session(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except (ValueError, TypeError):
            return redirect('project-detail', slug=slug)

        if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host():
            image_url = "https://via.placeholder.com/300"
        else:
            image_url = request.build_absolute_uri(project.image.url)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Donation to {project.title}',
                        'images': [image_url],
                    },
                    'unit_amount': int(amount * 100),  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('donation-success', kwargs={'slug': project.slug})
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(
                reverse('project-detail', kwargs={'slug': project.slug})
            ),
            metadata={'project_id': project.id, 'user_id': request.user.id, 'amount': amount},
        )

        return redirect(session.url)

    return redirect('project-detail', slug=slug)

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


    return render(request, 'donations/success.html', {'project': project})


