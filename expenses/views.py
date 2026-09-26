from .models import Expense
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expenses(request):
    if request.method == 'POST':
        expense = Expense.objects.create(
            user=request.user,
            title=request.data.get('title'),
            amount=request.data.get('amount'),
            category=request.data.get('category'),
            date=request.data.get('date')
        )
        return Response({
            'message': 'Expense created successfully',
            'id': expense.id
        }, status=201)
    
    expenses = Expense.objects.filter(user=request.user)
    data = []

    for expense in expenses:
        data.append({
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date
        })
    return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summary(request):

    expenses = Expense.objects.filter(
        user=request.user
    )

    total = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    categories = {}

    for expense in expenses:

        if expense.category not in categories:
            categories[expense.category] = 0

        categories[expense.category] += float(
            expense.amount
        )

    return Response({
        "total": total,
        "categories": categories
    })