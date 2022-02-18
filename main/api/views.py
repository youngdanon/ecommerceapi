from rest_framework.views import APIView, Response
from main.models import Product, ProductImage
from main.api.serializers import ProductSerializer, ProductImageSerializer


class ProductView(APIView):
    def get(self, request, **kwargs):
        if sku := kwargs.get('sku'):
            product = Product.objects.filter(SKU=sku)
            if len(product) > 0:
                serializer = ProductSerializer(product[0])
                data = serializer.data
                return Response({'products': data}, status=200)
            else:
                return Response({'details': 'Not found'}, status=404)

        elif category := request.query_params.get('category'):
            products = Product.objects.filter(category=category, is_active=True)
            if len(products) > 0:
                serializer = ProductSerializer(products, many=True)
                data = serializer.data
                return Response(data, status=200)
            else:
                return Response({'details': 'Not found'}, status=404)
        else:
            products = Product.objects.filter(is_active=True)
            serializer = ProductSerializer(products, many=True)
            data = serializer.data
            return Response({'products': data}, status=200)

    def post(self, request):
        data = request.data
        preview_image = request.data.get['file']
        data.update({'preview_image': preview_image})
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = Product.objects.create(**data)
            data = ProductSerializer(product).data
            return Response(data, status=200)
        else:
            return Response({'details': serializer.errors}, status=409)

    def patch(self, request, product_id):
        data = request.data
        product = Product.objects.filter(id=product_id)
        if len(product) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)

        serializer = ProductSerializer(product, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'details': serializer.errors}, exception=True, status=400)

    def delete(self, request, sku):
        product = Product.objects.filter(SKU=sku)
        if len(product) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product.delete()
        return Response(status=204)


class ProductImageView(APIView):

    def get(self, request, sku):
        product_id = Product.objects.filter(SKU=sku)
        if len(product_id) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product_id = product_id[0]
        images = [product_image.image.url for product_image in ProductImage.objects.filter(product=product_id)]
        return Response({'images': images})

    def post(self, request, sku):
        product_id = Product.objects.filter(SKU=sku)
        image = request.data.get['file']
        default_image = image.resize((1000, 1000))

        if len(product_id) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product_id = product_id[0]
        data = {'image': default_image, 'product': product_id}
        serializer = ProductImageSerializer(data)
        if serializer.is_valid():
            ProductImage.objects.create(**data)
            return Response(status=200)
        else:
            return Response({'details': serializer.errors}, exception=True, status=409)
