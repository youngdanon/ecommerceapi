from rest_framework.views import APIView, Response
from partners.api.serializers import OfferSerializer, PartnerSerializer
from partners.models import Offer, Partner


class OfferView(APIView):
    def get(self, request, **kwargs):
        offer_id = kwargs.get('offer_id')
        offer = Offer.objects.filter(id=offer_id)
        if len(offer) < 1:
            return Response(status=404)
        serializer = OfferSerializer(offer[0])
        print(serializer.data)
        return Response({'offer': serializer.data}, status=200)

    def post(self, request):
        data = request.data
        serializer = OfferSerializer(data=data)
        if serializer.is_valid():
            offer = Offer.objects.create(**data)
            return Response({'offer': OfferSerializer(offer)}, status=200)
        else:
            return Response({'details': serializer.errors}, exception=True, status=409)

    def patch(self, request, **kwargs):
        if offer_id := kwargs.get('offer_id'):
            offer = Offer.objects.filter(id=offer_id)
            if len(offer) < 1:
                return Response(status=404)
            offer = offer[0]
            if action := request.data.get('action'):
                if action == 'transition':
                    new_transitions_amount = offer.transitions_amount + 1
                    serializer = OfferSerializer(offer, data={'transitions_amount': new_transitions_amount},
                                                 partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        offer = Offer.objects.get(id=offer_id)
                        return Response({'offer': OfferSerializer(offer).data})
                    else:
                        return Response({'details': serializer.errors}, status=409, exception=True)
                elif action == 'order':
                    new_order_amount = offer.orders_amount + 1
                    product = offer.product
                    partner = offer.partner
                    new_balance = float(partner.balance) + float(product.price) * 0.1
                    partner_serializer = PartnerSerializer(partner, data={'balance': new_balance}, partial=True)
                    if partner_serializer.is_valid():
                        partner_serializer.save()
                    serializer = OfferSerializer(offer, data={'orders_amount': new_order_amount},
                                                 partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        offer = Offer.objects.get(id=offer_id)
                        return Response({'offer': OfferSerializer(offer).data})
        return Response(status=400, exception=True)

    def delete(self, request, offer_id):
        offer = Offer.objects.filter(id=offer_id)
        if len(offer) < 1:
            return Response({'details': 'Offer not found'}, exception=True, status=404)
        offer.delete()
        return Response(status=204)


class PartnerView(APIView):
    def get(self, request, **kwargs):
        if partner_id := kwargs.get('partner_id'):
            partner = Partner.objects.filter(id=partner_id)
            if len(partner) > 0:
                serializer = PartnerSerializer(partner[0])
                data = serializer.data
                return Response({'partner': data}, status=200)
            else:
                return Response({'details': 'Not found'}, status=404)

        else:
            partners = Partner.objects.all()
            serializer = PartnerSerializer(partners, many=True)
            data = serializer.data
            return Response({'partners': data}, status=200)

    def post(self, request):
        data = request.data
        serializer = PartnerSerializer(data=data)
        if serializer.is_valid():
            partner = Partner.objects.create(**data)
            data = PartnerSerializer(partner).data
            return Response(data, status=200)
        else:
            return Response({'details': serializer.errors}, status=409)

    def patch(self, request, partner_id):
        data = request.data
        partner = Partner.objects.filter(id=partner_id)
        if len(partner) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)

        serializer = PartnerSerializer(partner, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'partner': serializer.data}, status=201)
        else:
            return Response({'details': serializer.errors}, exception=True, status=400)

    def delete(self, request, partner_id):
        partner = Partner.objects.filter(id=partner_id)
        if len(partner) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        partner.delete()
        return Response(status=204)
