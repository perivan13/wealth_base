import os
import socket

from bson import ObjectId
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from . import excel_exporter, for_android
from . import mongo
from . import templater
from . import utils


def index(request):
    return render(request, 'index.html')


class ItemView(APIView):

    def get(self, _):
        """
        :param _: Default to none.
        :return: Item list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_item']
        items = collection.find()
        if collection:
            for document in items:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({'items': result}, status=200,
                        headers={'Access-Control-Allow-Origin': '*'})

    def post(self, request):
        """
        :param request: Request entity, contains request payload.
        :return: Response message: "message": "Item '{}' created successfully.",
                response status 201.
        """
        collection = mongo.get_conn()['main_item']
        item = request.data
        prep_item = utils.prepare_data(item)
        item_id = collection.insert_one(prep_item).inserted_id
        return Response({"message": "Item '{}' created successfully."
                        .format(item_id)}, status=201)

    def delete(self, request, pk):
        """
        :param request: Request entity, contains request payload.
        :param pk: entity primary key.
        :return: Response message: "message": "Item with id `{}` has been deleted.",
                response status 204 if success, or "message": "Item with _id `{}` not found."
                response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_item']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Item with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "Item with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
        :param request: Request entity, contains request payload.
        :param pk: entity primary key.
        :return: Response message: "message": "Item with id `{}` has been updated.",
                response status 202 if success, or "message": "Item with _id `{}` not found."
                response status 404 otherwise.
        """
        updated_fields = request.data
        if "_showDetails" in updated_fields:
            updated_fields.pop("_showDetails")
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_item']
        if collection:
            prep_updated_fields.pop("_id")
            if prep_updated_fields['components']:
                index = 1
                for component in prep_updated_fields['components']:
                    component['id'] = index
                    index += 1
            collection.update_one({
                "_id": ObjectId(pk)
            }, {
                "$set": prep_updated_fields
            }, upsert=False)
            return Response({"message": "Item with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "Item with _id `{}` not found.".format(pk)}, status=404)


class EmployeeView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: employee list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_employee']
        employees = collection.find()

        if collection:
            for document in employees:
                document['_id'] = str(document['_id'])
                result.append(document)
        collection = mongo.get_conn()['main_item']
        items = collection.find()
        set_employees = set()
        if collection:
            for document in items:
                set_employees.add(document['responsible'])
                set_employees.add(document['user'])
                for component in document['components']:
                    set_employees.add(component['user'])
            if '' in set_employees:
                set_employees.remove('')
        return Response({
            'employees': result,
            'prep_employees': set_employees
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "employee '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_employee']
        employee = request.data
        prep_employee = utils.prepare_data(employee)
        employee_id = collection.insert_one(prep_employee).inserted_id
        return Response({"message": "employee with _id '{}' created successfully."
                        .format(employee_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "employee with id `{}` has been deleted.",
                    response status 204 if success, or "message": "employee with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_employee']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "employee with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "employee with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "employee with id `{}` has been updated.",
                    response status 202 if success, or "message": "employee with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_employee']
        if collection:
            prep_updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "employee with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "employee with _id `{}` not found.".format(pk)}, status=404)


class OTSSView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: OTSS category list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_otss']
        categories = collection.find()
        if collection:
            for document in categories:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'otss': result
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "OTSS category '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_otss']
        category = request.data
        prep_category = utils.prepare_data(category)
        category_id = collection.insert_one(prep_category).inserted_id
        return Response({"message": "OTSS category with _id '{}' created successfully."
                        .format(category_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "OTSS category with id `{}` has been deleted.",
                    response status 204 if success, or "message": "OTSS category with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_otss']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "OTSS category with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "OTSS category with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "OTSS category with id `{}` has been updated.",
                    response status 202 if success, or "message": "OTSS category with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_otss']
        if collection:
            prep_updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "OTSS category with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "OTSS category with _id `{}` not found.".format(pk)}, status=404)


class UnitView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: Unit list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_unit']
        units = collection.find()
        if collection:
            for document in units:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'units': result
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "Unit '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_unit']
        unit = request.data
        prep_unit = utils.prepare_data(unit)
        unit_id = collection.insert_one(prep_unit).inserted_id
        return Response({"message": "Unit with _id '{}' created successfully."
                        .format(unit_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Unit with id `{}` has been deleted.",
                    response status 204 if success, or "message": "Unit with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_unit']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Unit with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "Unit with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Unit with id `{}` has been updated.",
                    response status 202 if success, or "message": "Unit with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_unit']
        if collection:
            prep_updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "Unit with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "Unit with _id `{}` not found.".format(pk)}, status=404)


class TypeView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: Type list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_type']
        types = collection.find()
        if collection:
            for document in types:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'types': result
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "Type '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_type']
        _type = request.data
        prep_type = utils.prepare_data(_type)
        type_id = collection.insert_one(prep_type).inserted_id
        return Response({"message": "Type with _id '{}' created successfully."
                        .format(type_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Type with id `{}` has been deleted.",
                    response status 204 if success, or "message": "Type with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_type']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Type with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "Type with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Type with id `{}` has been updated.",
                    response status 202 if success, or "message": "Type with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_type']
        if collection:
            prep_updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "Type with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "Type with _id `{}` not found.".format(pk)}, status=404)


class CategoryView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: Category list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_category']
        categories = collection.find()
        if collection:
            for document in categories:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'categories': result
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "Category '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_category']
        category = request.data
        prep_category = utils.prepare_data(category)
        category_id = collection.insert_one(prep_category).inserted_id
        return Response({"message": "Category with _id '{}' created successfully."
                        .format(category_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Category with id `{}` has been deleted.",
                    response status 204 if success, or "message": "Category with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_category']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Category with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "Category with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Category with id `{}` has been updated.",
                    response status 202 if success, or "message": "Category with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_category']
        if collection:
            prep_updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "Category with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "Category with _id `{}` not found.".format(pk)}, status=404)


class LocationView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: Location list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_location']
        locations = collection.find()
        if collection:
            for document in locations:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'locations': result
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "Location '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_location']
        location = request.data
        prep_location = utils.prepare_data(location)
        location_id = collection.insert_one(prep_location).inserted_id
        return Response({"message": "Location with _id '{}' created successfully."
                        .format(location_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Location with id `{}` has been deleted.",
                    response status 204 if success, or "message": "Location with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_location']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Location with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "Location with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Location with id `{}` has been updated.",
                    response status 202 if success, or "message": "Location with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        collection = mongo.get_conn()['main_location']
        if collection:
            prep_updated_fields.pop("_id")
            collection.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "Location with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "Location with _id `{}` not found.".format(pk)}, status=404)


class ConditionView(APIView):

    def get(self, _):
        """
            :param _: Default to none.
            :return: Condition list. Response status 200.
        """
        result = []
        collection = mongo.get_conn()['main_condition']
        conditions = collection.find()
        if collection:
            for document in conditions:
                document['_id'] = str(document['_id'])
                result.append(document)
        return Response({
            'conditions': result
        }, status=200)

    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "message": "Condition '{}' created successfully.",
                    response status 201.
        """
        collection = mongo.get_conn()['main_condition']
        condition = request.data
        prep_condition = utils.prepare_data(condition)
        condition_id = collection.insert_one(prep_condition).inserted_id
        return Response({"message": "Condition with _id '{}' created successfully."
                        .format(condition_id)}, status=201)

    def delete(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Condition with id `{}` has been deleted.",
                    response status 204 if success, or "message": "Condition with _id `{}` not found."
                    response status 404 otherwise.
        """
        collection = mongo.get_conn()['main_condition']
        if collection:
            collection.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Category with id `{}` has been deleted."
                            .format(pk)}, status=204)
        else:
            return Response({"message": "Category with _id `{}` not found.".format(pk)}, status=404)

    def put(self, request, pk):
        """
            :param request: Request entity, contains request payload.
            :param pk: entity primary key.
            :return: Response message: "message": "Condition with id `{}` has been updated.",
                    response status 202 if success, or "message": "Condition with _id `{}` not found."
                    response status 404 otherwise.
        """
        updated_fields = request.data
        prep_updated_fields = utils.prepare_data(updated_fields)
        condition = mongo.get_conn()['main_condition']
        if condition:
            prep_updated_fields.pop("_id")
            condition.update_one({
                '_id': ObjectId(pk)
            }, {
                '$set': prep_updated_fields
            }, upsert=False)
            return Response({"message": "Condition with id `{}` has been updated."
                            .format(pk)}, status=202)
        else:
            return Response({"message": "Condition with _id `{}` not found.".format(pk)}, status=404)


class TestView(APIView):
    def get(self, _):
        """
            :param _: Default to none.
            :return: Response status 200.
        """
        host, port = mongo.get_param()
        connection = mongo.get_conn()
        if connection is not None:
            return Response({'host': host, 'port': port, 'settings': socket.gethostname()}, status=200,
                            headers={'Access-Control-Allow-Origin': '*'})
        else:
            return Response({'host': 'error', 'port': 'error', 'settings': socket.gethostname()}, status=400,
                            headers={'Access-Control-Allow-Origin': '*'})


class ExcelExporterView(APIView):
    def post(self, request):
        """
            :param request: Request entity, contains request payload.
            :return: Response message: "File .xlsx with name '{}' created successfully.",
                            response status 201.
        """
        payload = request.data
        result = excel_exporter.export_to_excel(payload=payload)
        utils.del_all('/media/generated/', '*.xlsx')
        return FileResponse(open(result, 'rb'), status=201)


# class RecognizerView(APIView):
#     def post(self, request):
#         payload = request.data
#         filename = "{}.png".format(str(uuid.uuid4()))
#         with default_storage.open(filename, 'wb+') as destination:
#             for chunk in payload['file'].chunks():
#                 destination.write(chunk)
#         print(settings.MEDIA_ROOT + filename)
#         result = recognizer.recognizer('media/' + filename)
#         return Response({
#             'extracting_data': result
#         }, status=201)


# class TemplaterView(APIView):
#     def get(self, _):
#         result = os.listdir('media/templates')
#         info = ''
#         for key in templater.ALLOWED_TEMPLATES:
#             info += templater.ALLOWED_TEMPLATES[key] + '\n'
#         return Response({'docs': result,
#                          'info': info}, status=200)
#
#     def post(self, request):
#         file = request.data['file']
#         with default_storage.open('templates/' + str(request.data['file']), 'wb+') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
#         if templater.docx_size('media/templates/' + str(request.data['file'])) > 0:
#             return Response({'message': 'File {} added successfully'.format(str(request.data['file']))},
#                             status=201)
#         else:
#             os.remove('media/templates/' + str(request.data['file']))
#             return Response({'message': 'Файл {} не содержит шаблонов для вставки.'.format(str(request.data['file']))},
#                             status=400)
#
#
# class DownloadDocsView(APIView):
#     def post(self, request):
#         filename = request.data['filename']
#         items = request.data['items']
#         merge_doc = request.data['merge_doc']
#         for item in items:
#             item.pop('_id')
#         print(items)
#         result = templater.final_replacement('media/templates/' + filename, items, merge_doc)
#         return FileResponse(open(result, 'rb'), status=201)


class TemplaterView(APIView):
    def get(self, _):
        result = os.listdir(os.getcwd() + '/media/templates/')
        info = ''
        for key in templater.ALLOWED_TEMPLATES:
            info += templater.ALLOWED_TEMPLATES[key] + '\n'
        return Response({'docs': result,
                         'cwd': os.getcwd(),
                         'info': info}, status=200)

    def post(self, request):
        file = request.data['file']
        if not os.path.isdir(os.getcwd() + '/media/templates'):
            os.mkdir(os.getcwd() + '/media/templates')
        with default_storage.open(os.getcwd() + '/media/templates/' + str(file), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        if templater.docx_size(os.getcwd() + '/media/templates/' + str(file)) > 0:
            return Response({'message': 'File {} added successfully'.format(str(file))},
                            status=201)
        else:
            os.remove(os.getcwd() + '/media/templates/' + str(file))
            return Response({'message': 'Файл {} не содержит шаблонов для вставки.'
                            .format(str(file))},
                            status=400)

    def delete(self, request, pk):
        full_path = os.getcwd() + '/media/templates/' + pk
        os.remove(full_path)
        return Response({'message': 'Файл {} успешно удален.'
                        .format(str(pk))},
                        status=204)

    def put(self, request, pk):
        full_path = os.getcwd() + '/media/templates/' + pk
        return FileResponse(open(full_path, 'rb'), status=202)


class DownloadDocsView(APIView):
    def post(self, request):
        filename = request.data['filename']
        items = request.data['items']
        merge_doc = request.data['merge_doc']
        for item in items:
            item.pop('_id')
        result = templater.final_replacement(os.getcwd() + '/media/templates/' + filename,
                                             items,
                                             merge_doc)
        utils.del_all('/media/generated/', '*.docx')
        return FileResponse(open(result, 'rb'), status=201)


class EncodeView(APIView):
    def post(self, request):
        # path_to_doc = os.getcwd() + '/media/Коды.docx'
        path_to_doc = os.getcwd() + '/media/Коды.xlsx'
        if os.path.isfile(path_to_doc):
            os.remove(path_to_doc)
        result = utils.create_data_matrix_xlsx(request.data['payload'])
        utils.del_all('/media/codes/', '*.png')
        return FileResponse(open(result, 'rb'), status=201)


class AndroidView(APIView):
    def post(self, request):
        file = request.data['file']
        if not os.path.isdir(os.getcwd() + '/media/for_android'):
            os.mkdir(os.getcwd() + '/media/for_android')
        with default_storage.open(os.getcwd() + '/media/for_android/' + str(file), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        result = for_android.update(os.getcwd() + '/media/for_android/' + str(file))
        if result:
            os.remove(os.getcwd() + '/media/for_android/' + str(file))
            return Response({'message': 'Success'}, status=201)
