from django.urls import path
from partners.api.views import OfferView, PartnerView

urlpatterns = [
    path('offer/', OfferView.as_view()),
    path('offer/<int:offer_id>/', OfferView.as_view()),
    path('partner/<int:partner_id>/', PartnerView.as_view()),
    path('', PartnerView.as_view())
]