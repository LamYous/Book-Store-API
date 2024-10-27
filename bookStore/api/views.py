from django.shortcuts import render
from .models import Book, Category, Order
from .serializers import BookSerializer, CategorySerializer, OrderSerailizer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

#Create new book
@api_view(['POST'])
@permission_classes([IsAdminUser])
def Create_book(request):
    data = request.data
    serializer = BookSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"books": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Get all books
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()

    serializer = BookSerializer(books, many=True)
    return Response({'books': serializer.data})

#Get a specific book by ID
@api_view(['GET'])
def book_detail(request, book_id):
    try: 
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"Error":"Book not found!"},status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book, many=False)
    return Response({'book':serializer.data})

#Update a specific book by ID
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'Error': 'Book not found!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a specific book by ID
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Book.DoesNotExist:
        return Response({"Error":"Book not found!"}, status=status.HTTP_404_NOT_FOUND)

# Create a new Category
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"category":serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Get all categories
@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)

    return Response({"Categorys": serializer.data})

# GET a specific category by ID
@api_view(['GET'])
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error":"Category not found!"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, many=False)
    return Response({"category": serializer.data})

# Update a specific category by ID
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error":"Category not found!"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = CategorySerializer(category, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Delete a specific category by ID
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Category.DoesNotExist:
        return Response({'error':'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    

# create a new order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    book_id = request.data.get('book')
    quantity = request.data.get('quantity')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not dound!'}, status=status.HTTP_404_NOT_FOUND)
    
    if book.stock < quantity:
        return Response({'error':'Not enought stock'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        book.stock -= quantity
        book.save()

        order = Order.objects.create(
            user = request.user, 
            book = book,
            quantity = quantity,
            status = 'pending',
        )

        serializer = OrderSerailizer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# Get all orders for a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user = request.user)
    total_orders = orders.count()
    serializer = OrderSerailizer(orders, many=True)
    return Response({"orders":serializer.data, 'total orders':total_orders}, status=status.HTTP_200_OK)
    
# Get a specific order by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user = request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not faund!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerailizer(order, many=False)
    return Response({"order":serializer.data})
    
#Update a Specific order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error':'Order not faund!'})
    
    quantity = request.data.get('quantity')
    if quantity:
        if quantity > order.book.stock + order.quantity:
            return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #update the book stack and order quantity
            order.book.stock += order.quantity
            order.book.stock -= quantity
            order.quantity = quantity
            order.book.save()
                
    serializer = OrderSerailizer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"order":serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Delete a Specific Order
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order.book.stock += order.quantity
        order.book.save()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({'error':'Order not faund!'})
