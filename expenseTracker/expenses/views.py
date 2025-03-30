from django.shortcuts import render

# Create your views here.
from .serializers import (
    OccasionSerializer,
    EventSerializer, 
    PaymentSerializer,
    EventUtilizerSerializer,
    UtlizersCreateSerializer
)
from .models import Occasion, Event, Utlizers, Payment
from rest_framework import viewsets, permissions, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Sum
from users.models import CustomUser
from django.db import transaction

class OccasionManagementView(viewsets.ViewSet):
    """View for Managing Occassion related operation"""
    permission_classes = [permissions.IsAuthenticated,]
    

    def list(self, request):
        print("user_id",  request.user.id)
        occasions = Occasion.objects.filter(created_by = request.user)
        serializer = OccasionSerializer(occasions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
            request_body=OccasionSerializer,
            responses={201:OccasionSerializer()}
    )
    def create(self, request):
        """Create an occassion"""
        print("request_body", request.data)
        serializer = OccasionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED )
        return Response(serializer.errors, status = status. HTTP_400_BAD_REQUEST)
    

    # def retrieve(self, request, pk=None):
    #     occasions = get_object_or_404(Occasion, pk=pk, created_by = request.user)
    #     serializer = OccasionSerializer(occasions)
    #     return Response (serializer.data)
    
    @swagger_auto_schema(
            request_body=OccasionSerializer,
            responses={200:OccasionSerializer()}
    )
    def update(self, request, pk=None):
        """Update an existing Occassion"""
        occasions = get_object_or_404(Occasion, pk=pk, created_by = request.user)
        serializer = OccasionSerializer(occasions, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Delete an Existing Occassion"""
        occasions = get_object_or_404(Occasion, pk=pk, created_by = request.user)
        if occasions:
            events = Event.objects.filter(occasion=occasions)
            for event in events:
                event.delete()
        occasions.delete()
        return Response({"message":"occassion deleted successfully"}, status = status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def occassion_summary(self, request, pk=None):
        """Get an occassion summary with event and expenditure"""
        try:
            occasion = Occasion.objects.get(pk=pk)
        except Occasion.DoesNotExist:
            return Response({'error': 'Occasion not found'}, status=status.HTTP_404_NOT_FOUND)
        
        events = Event.objects.filter(occasion=occasion)
        event_data = []
        total_expenditure = 0

        for event in events:
            utilizer_details = Utlizers.objects.filter(event = event).values("utlizer__id","utlizer__email", "amount")
            print("utilizer_details",utilizer_details)
            event_data.append(
                {
                    "event_id":event.id,
                    "event_name":event.name,
                    "total_spent":event.total_amount,
                    'expender':event.expender.email,
                    'utilizer_details':list(utilizer_details)
                }
            )

            total_expenditure = total_expenditure+event.total_amount

        return Response(
            {
                'id':occasion.id,
                'occassion_name':occasion.name,
                'total_expenditure':total_expenditure,
                "events":event_data
            }
        )


class EventViewSet(viewsets.ViewSet):
    """View for Managing Event Expenditure"""

    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
            request_body=EventUtilizerSerializer,
            responses={200:OccasionSerializer()}
    )
    def create(self, request):
        """Create an event with utilizers"""
        occasion_id = request.data.get('occasion')
        name = request.data.get('name')
        expender = request.data.get('expender')
        total_amount = request.data.get('total_amount')
        utilizers_data = request.data.get('utilizers_data')
        if occasion_id:
            try:
                occasion = Occasion.objects.get(id = occasion_id)
            except Occasion.DoesNotExist:
                return Response({'error': 'Occasion not found'}, status=status.HTTP_404_NOT_FOUND)
            request.data['occasion'] = occasion_id
        else:
            occasion = None

        try:
            expender = CustomUser.objects.get(id = expender)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Expender not found'}, status=status.HTTP_404_NOT_FOUND)
        
        total_utilizer_amount = sum(int(utilizer["amount"]) for utilizer in utilizers_data)
      
        if total_utilizer_amount > int(total_amount):
            return Response({"error":"Total shared amount more than total"}, status = status.HTTP_400_BAD_REQUEST)

        
        event = Event.objects.create(
            name = name,
            occasion = occasion,
            created_by = request.user,
            expender = expender,
            total_amount = total_amount
        )
        
        print("event========>", event)

        created_utilizers = []
        if utilizers_data:
            for utilizer_user in utilizers_data:
                user_id = utilizer_user.get('utlizer')
                user_amount = utilizer_user.get('amount')
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    return Response({"error":f"User with {user_id} not found"}, status = status.HTTP_404_NOT_FOUND)

                utilizer = Utlizers.objects.create(event=event, utlizer=user, amount=user_amount)
                created_utilizers.append(utilizer)

        return Response({
            "message":"Event with Expenditure created successfully",
            "data":{
                "id":event.id,
                "name":event.name,
                "occassion":occasion_id,
                "total_amount":event.total_amount,
                "expender":expender.id,
                "utilizers":utilizers_data
            },
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Get event detail with it's all utilizers"""
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        
        utilizers = Utlizers.objects.filter(event = event).values_list("utlizer__email", flat = True)
        participants = list(set([event.expender.email] + list(utilizers)))
        print("event", event.name)
        try:
            print(event.occasion)

        except Exception as e:
            import traceback
            traceback.print_exc()
        return Response(
            {
                "name":event.name,
                "occassion":event.occasion.id,
                "expender":event.expender.id,
                "total_amount":event.total_amount,
                "participants":participants
            }
        )


    @swagger_auto_schema(
            request_body=EventUtilizerSerializer,
            responses={200:OccasionSerializer()}
    )
    def update(self, request, pk=None):
        """Update existing event with utilizers"""
        occasion_id = request.data.get('occasion')
        print("occasion_id",occasion_id)
        name = request.data.get('name')
        expender = request.data.get('expender')
        total_amount = request.data.get('total_amount')
        utilizers_data = request.data.get('utilizers_data')
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if occasion_id:
            try:
                occasion = Occasion.objects.get(pk=occasion_id)
            except Occasion.DoesNotExist:
                return Response({'error': 'Occasion not found'}, status=status.HTTP_404_NOT_FOUND)
            request.data['occasion'] = occasion_id

        try:
            expender = CustomUser.objects.get(id = expender)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Expender not found'}, status=status.HTTP_404_NOT_FOUND)
        
        total_utilizer_amount = sum(int(utilizer["amount"]) for utilizer in utilizers_data)
        if total_utilizer_amount > int(total_amount):
            return Response({"error": "Total shared amount more than total"}, status=status.HTTP_400_BAD_REQUEST)

        event.name = name
        event.total_amount = total_amount
        event.expender = expender
        event.save()

        if utilizers_data:
            # Clear existing utilizers
            Utlizers.objects.filter(event=event).delete()

            # Create new utilizers
            created_utilizers = []
            for utilizer_user in utilizers_data:
                user_id = utilizer_user.get('utlizer')
                user_amount = utilizer_user.get('amount')
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    return Response({"error": f"User with {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)

                utilizer = Utlizers.objects.create(event=event, utlizer=user, amount=user_amount)
                created_utilizers.append(utilizer)


        return Response({
            "message": "Event with Expenditure updated successfully",
            "data": request.data,
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    @action(detail=True, methods=['get'])
    def payments(self, requesr, pk=None):
        """Get all the payment list for an event"""
        event = get_object_or_404(Event, id = pk)
        payments = Payment.objects.filter(event_id = event.id)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)    

class UtilizerViewSet(viewsets.ViewSet):
    """View for creating utilizers """
    permission_classes = [permissions.IsAuthenticated,]

    @swagger_auto_schema(
        request_body=UtlizersCreateSerializer(many=True),
        responses={200: OccasionSerializer(many=True)}
    )
    def create(self, request):
        utilizers_data = request.data
        print("utilizers_data=================>",utilizers_data)
        if not isinstance(utilizers_data, list):
            return Response({'error': 'Expected a list of utilizers'}, status=status.HTTP_400_BAD_REQUEST)

        for utilizer_data in utilizers_data:
            event_id = utilizer_data.get('event')  # Ensure this field is present in each utilizer data
            if not event_id:
                return Response({'error': 'event_id is required for each utilizer'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                event = Event.objects.get(id=event_id)
                Utlizers.objects.filter(event=event).delete()
                # utilizer_data['event'] = event_id
            except Event.DoesNotExist:
                return Response({'error': f'Event with id {event_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UtlizersCreateSerializer(data=utilizers_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ViewSet):
    """View for clearing payment of a user related to an event"""

    def list(self, request):
        """Returns payment made and received by the user for all events"""
        user = request.user

        payment_made = Payment.objects.filter(payer= user)
        payment_received = Payment.objects.filter(payee = user)

        payments = payment_made | payment_received
        serializer = PaymentSerializer(payments, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
            request_body=PaymentSerializer,
            responses={200:OccasionSerializer()}
    )
    @action(detail=False, methods=['post'])
    def clear_expense(self, request,pk=None):
        """Clear an expense for an event"""
        payer_id = request.data.get('payer')
        payee_id = request.data.get('payee')
        event_id = request.data.get('event')
        amount = request.data.get('amount')


        if not all([payer_id,payee_id,event_id,amount]):
            return Response ({"error":"Missing Required Fields"}, status = status.HTTP_400_BAD_REQUEST)
        

        try:
            event = Event.objects.get(id = event_id)
        except Event.DoesNotExist:
            return Response({"error":"Event not found"}, status = status.HTTP_404_NOT_FOUND)
        

        try:
            utilizer = Utlizers.objects.get(event = event, utlizer = payee_id)
        except Utlizers.DoesNotExist:
            return Response({"error":"Payer was not part of Event"}, status = status.HTTP_404_NOT_FOUND)


        # total_due = Utlizers.objects.filter(event = event, utlizer_id = payee_id).aggregate(total = Sum('amount'))['total'] or 0
        total_due = utilizer.amount
        total_paid = Payment.objects.filter(event = event, payer_id = payer_id,payee_id = payee_id).aggregate(total = Sum('amount'))['total'] or 0


        balance_due = total_due - total_paid

        if balance_due <= 0 :
            return Response({"error":"No outstanding balance for this user to clear"}, status = status.HTTP_400_BAD_REQUEST)
        
        if int(amount) > balance_due:
            return Response({"error":"Payment Exceed"}, status = status.HTTP_400_BAD_REQUEST) 
        

        payment = Payment.objects.create(
            payer_id = payer_id,
            payee_id = payee_id,
            event = event,
            amount = amount
        )


        serializer = PaymentSerializer(payment)

        return Response({"message":"Payment Recorded Successfully","data":serializer.data},status = status.HTTP_200_OK)