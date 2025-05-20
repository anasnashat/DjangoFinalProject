from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import stripe

from projects.models import Project


# Create your views here.


@login_required
def create_donation_session(request, slug):
    project = get_object_or_404(Project, slug=slug)

    donation_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Donation to {project.title}',
                    'images': [project.image],
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


