from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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
                return JsonResponse({'success': False, 'error': 'Amount must be positive.'}, status=400)

            image_url = "https://via.placeholder.com/300" if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host() else request.build_absolute_uri(project.image.url)

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
                success_url=f"{request.build_absolute_uri(reverse('project-detail', kwargs={'slug': project.slug}))}?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=request.build_absolute_uri(reverse('project-detail', kwargs={'slug': project.slug})),
                metadata={'project_id': project.id, 'user_id': request.user.id, 'amount': amount},
            )

            return JsonResponse({'success': True, 'checkout_url': session.url})
        except (ValueError, TypeError, stripe.error.StripeError) as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
def payment_success(request, slug):
    project = get_object_or_404(Project, slug=slug)
    session_id = request.GET.get('session_id')
    print(f"Received session_id: {session_id}")

    if not session_id or session_id == '{CHECKOUT_SESSION_ID}':
        return JsonResponse({'success': False, 'error': 'Invalid session ID provided.'}, status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

            if not Payment.objects.filter(stripe_payment_id=payment_intent.id, user=request.user).exists():
                amount = payment_intent.amount / 100
                Payment.objects.create(
                    project=project,
                    user=request.user,
                    amount=amount,
                    status=payment_intent.status,
                    stripe_payment_id=payment_intent.id
                )

            return JsonResponse({
                'success': True,
                'amount_raised': project.amount_raised,
                'progress_percentage': project.progress_percentage
            })
        else:
            return JsonResponse({'success': False, 'error': 'Payment not completed.'}, status=400)

    except stripe.error.StripeError as e:
        return JsonResponse({'success': False, 'error': f'Stripe error: {str(e)}'}, status=400)
