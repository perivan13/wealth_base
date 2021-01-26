# Представления для работы через Djongo
# from rest_framework.viewsets import ModelViewSet
#
# from .models import Item, Employee
# from .serializers import EmployeeSerializer, ItemSerializer
#
#
# class ItemViewSet(ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#
#
# class EmployeeViewSet(ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

from . import mongo


class ItemView(APIView):

    def get(self, _):
        result = []
        collection = mongo.get_conn()['main_item']
        items = collection.find()
        if collection:
            for document in items:
                document['_id'] = str(document['_id'])
                result.append(document)
        # serializer = ItemSerializer(items, many=True)
        return Response({
            'items': result
        }, status=200)

    def post(self, request):
        collection = mongo.get_conn()['main_item']
        item = request.data
        item_id = collection.insert_one(item).inserted_id
        return Response({"message": "Item '{}' created successfully."
                        .format(item_id)}, status=201)

    def delete(self, request, pk):
        collection = mongo.get_conn()['main_item']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Item with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            Response({"message": "Item with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        updated_fields = request.data
        collection = mongo.get_conn()['main_item']
        if collection:
            updated_fields.pop("_id")
            if updated_fields['components']:
                index = 1
                for component in updated_fields['components']:
                    component['id'] = index
                    index += 1
            collection.update_one({
                "_id": ObjectId(pk)
            }, {
                "$set": updated_fields
            }, upsert=False)
            return Response({"message": "Item with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            Response({"message": "Item with _id `{}` not found.".format(pk)}, status=404)


class EmployeeView(APIView):

    def get(self, _):
        result = []
        collection = mongo.get_conn()['main_employee']
        employees = collection.find()
        if collection:
            for document in employees:
                document['_id'] = str(document['_id'])
                result.append(document)
        # serializer = ItemSerializer(employees, many=True)
        return Response({
            'employees': result
        })

    def post(self, request):
        collection = mongo.get_conn()['main_employee']
        employee = request.data
        employee_id = collection.insert_one(employee).inserted_id
        return Response({"message": "Employee with _id '{}' created successfully."
                        .format(employee_id)})

    def delete(self, request, pk):
        collection = mongo.get_conn()['main_employee']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Employee with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            Response({"message": "Employee with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        updated_fields = request.data
        collection = mongo.get_conn()['main_employee']
        if collection:
            updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': updated_fields
            }, upsert=False)
            return Response({"message": "Employee with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            Response({"message": "Employee with _id `{}` not found.".format(pk)}, status=404)


class OTSSView(APIView):

    def get(self, _):
        result = []
        collection = mongo.get_conn()['main_otss']
        categories = collection.find()
        if collection:
            for document in categories:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'otss': result
        })

    def post(self, request):
        collection = mongo.get_conn()['main_otss']
        category = request.data
        category_id = collection.insert_one(category).inserted_id
        return Response({"message": "OTSS category with _id '{}' created successfully."
                        .format(category_id)})

    def delete(self, request, pk):
        collection = mongo.get_conn()['main_otss']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "OTSS category with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            Response({"message": "OTSS category with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        updated_fields = request.data
        collection = mongo.get_conn()['main_otss']
        if collection:
            updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': updated_fields
            }, upsert=False)
            return Response({"message": "OTSS category with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            Response({"message": "OTSS category with _id `{}` not found.".format(pk)}, status=404)


class UnitView(APIView):

    def get(self, _):
        result = []
        collection = mongo.get_conn()['main_unit']
        units = collection.find()
        if collection:
            for document in units:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'units': result
        })

    def post(self, request):
        collection = mongo.get_conn()['main_unit']
        unit = request.data
        unit_id = collection.insert_one(unit).inserted_id
        return Response({"message": "Unit with _id '{}' created successfully."
                        .format(unit_id)})

    def delete(self, request, pk):
        collection = mongo.get_conn()['main_unit']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Unit with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            Response({"message": "Unit with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        updated_fields = request.data
        collection = mongo.get_conn()['main_unit']
        if collection:
            updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': updated_fields
            }, upsert=False)
            return Response({"message": "Unit with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            Response({"message": "Unit with _id `{}` not found.".format(pk)}, status=404)


class TypeView(APIView):

    def get(self, _):
        result = []
        collection = mongo.get_conn()['main_type']
        types = collection.find()
        if collection:
            for document in types:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'types': result
        })

    def post(self, request):
        collection = mongo.get_conn()['main_type']
        type = request.data
        type_id = collection.insert_one(type).inserted_id
        return Response({"message": "Type with _id '{}' created successfully."
                        .format(type_id)})

    def delete(self, request, pk):
        collection = mongo.get_conn()['main_type']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Type with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            Response({"message": "Type with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        updated_fields = request.data
        collection = mongo.get_conn()['main_type']
        if collection:
            updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': updated_fields
            }, upsert=False)
            return Response({"message": "Type with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            Response({"message": "Type with _id `{}` not found.".format(pk)}, status=404)


class CategoryView(APIView):

    def get(self, _):
        result = []
        collection = mongo.get_conn()['main_category']
        categories = collection.find()
        if collection:
            for document in categories:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'categories': result
        })

    def post(self, request):
        collection = mongo.get_conn()['main_category']
        category = request.data
        category_id = collection.insert_one(category).inserted_id
        return Response({"message": "Category with _id '{}' created successfully."
                        .format(category_id)})

    def delete(self, request, pk):
        collection = mongo.get_conn()['main_category']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Category with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            Response({"message": "Category with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        updated_fields = request.data
        collection = mongo.get_conn()['main_category']
        if collection:
            updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': updated_fields
            }, upsert=False)
            return Response({"message": "Category with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            Response({"message": "Category with _id `{}` not found.".format(pk)}, status=404)

