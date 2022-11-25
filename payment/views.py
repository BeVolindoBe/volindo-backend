from os import environ

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from payment.models import ExternalAgent, Payment
from payment.serializers import ExternalAgentSerializer


class NewExternalAgent(CreateAPIView):

    host = environ['HOST']
    endpoint = '/payments/{}/'

    def post(self, request):
        body = ExternalAgentSerializer(data=request.data)
        if body.is_valid():
            data = body.validated_data
            agent, created = ExternalAgent.objects.get_or_create(**data)
            payment = Payment.objects.create(agent=agent)
            response = {
                'message': 'OK',
                'payment_link': '{}{}'.format(self.host, self.endpoint.format(str(payment.id)))
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 400, 'message': 'Invalid agent information'},
                status=status.HTTP_400_BAD_REQUEST
            )


def payment_link(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    context = {
        'payment': payment       
    }
    return render(request, 'payment/payment.html', context=context)
