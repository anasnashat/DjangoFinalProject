from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import stripe
from django.urls import reverse

from donation_project import settings
from projects.models import Project


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_donation_session(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host():
        # Use a placeholder image for local development
        image_url = "https://via.placeholder.com/300"
    else:
        # Use the actual project image in production
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
        ),
        cancel_url=request.build_absolute_uri(
            reverse('project-detail', kwargs={'slug': project.slug})
        ),
        metadata={'project_id': project.id, 'user_id': request.user.id},
    )
    return redirect(donation_session.url)



@login_required
def payment_success(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'payments/success.html', {'project': project})


