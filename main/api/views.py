from rest_framework.views import APIView, Response
from main.models import Product, ProductImage
from main.api.serializers import ProductSerializer, ProductImageSerializer
from PIL import Image


class ProductView(APIView):
    @staticmethod
    def add_images(data):
        if isinstance(data, list):
            for i in range(len(data)):
                try:
                    image = ProductImage.objects.filter(product=data[i]['id'])[0].image.url
                except:
                    image = ""
                data[i].update({'image': image})
        elif isinstance(data, dict):
            images = ProductImage.objects.filter(product=data['id'])
            data.update({'images': [product_image.image.url for product_image in images]})

        return data

    def get(self, request, **kwargs):
        if sku := kwargs.get('sku'):
            product = Product.objects.filter(SKU=sku)
            if len(product) > 0:
                serializer = ProductSerializer(product[0])
                data = self.add_images(serializer.data)
                return Response({'products': data}, status=200)
            else:
                return Response({'details': 'Not found'}, status=404)

        elif category := request.query_params.get('category'):
            products = Product.objects.filter(category=category, is_active=True)
            if len(products) > 0:
                serializer = ProductSerializer(products, many=True)
                data = self.add_images(serializer.data)
                return Response(data, status=200)
            else:
                return Response({'details': 'Not found'}, status=404)
        else:
            products = Product.objects.filter(is_active=True)
            serializer = ProductSerializer(products, many=True)
            data = self.add_images(serializer.data)
            return Response({'products': data}, status=200)

    def post(self, request):
        data = request.data
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

    def delete(self, request, product_id):
        product = Product.objects.filter(id=product_id)
        if len(product) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product.delete()
        return Response(status=204)


class ProductImageView(APIView):
    @staticmethod
    def crop_to_square_image(image):
        image = Image.open(image)
        width, height = image.size
        if width > height:
            right = int((width - height) / 2)
            left = right
            top = 0
            bottom = 0
            image.crop((left, top, right, bottom))
        else:
            right = 0
            left = 0
            top = int((width - height) / 2)
            bottom = top
            image.crop((left, top, right, bottom))

        small_image = image
        small_image.thumbnail((400, 400))

        return image, small_image

    def get(self, request, sku):
        product_id = Product.objects.filter(SKU=sku)
        if len(product_id) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product_id = product_id[0]
        images = [product_image.image.url for product_image in ProductImage.objects.filter(product=product_id)]
        return Response({'images': images})

    def post(self, request, sku):
        product_id = Product.objects.filter(SKU=sku)
        image = request.data.get('file')



        if len(product_id) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product_id = product_id[0]
        data = {'image': image, 'product': product_id}
        serializer = ProductImageSerializer(data)
        if serializer.is_valid():
            ProductImage.objects.create(**data)
            return Response(status=200)
        else:
            return Response({'details': serializer.errors}, exception=True, status=409)

    def delete(self, request, sku):
        product_id = Product.objects.filter(SKU=sku)
        if len(product_id) < 1:
            return Response({'details': 'Product not found'}, exception=True, status=404)
        product_id = product_id[0]
        image = ProductImage.objects.get(product=product_id)
        image.delete()
        return Response(status=204)
