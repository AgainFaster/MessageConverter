from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging

# from MyProject.MyApp import CalcClass
from message_converter.json2csv import Json2Csv
from message_converter.models import IncomingMessage, ConvertedMessageQueue, ApiProject

logging.basicConfig(level=logging.DEBUG)

class ApiProjectView(APIView):

    def get(self, request, *args, **kw):
        return self._response(request, 'GET is currently not implemented. Try POST.')

    def post(self, request, *args, **kw):
        # the raw json is in request.POST['_content']
        # application/json is in request.POST['_content_type']
        # djangorest loads the json into dict request.DATA

        if not 'project_name' in kw:
            raise Http404

        try:
            project = ApiProject.objects.get(name=kw['project_name'])
        except ApiProject.DoesNotExist:
            return self._response(request, 'Project name does not exist.', False)

        if not request.DATA.get('request_id'):
            return self._response(request, 'Missing request_id.', False)

        if project.from_type.format == 'JSON' and project.to_type.format == 'CSV':
            original_message = IncomingMessage.objects.create(project=project,
                                                              message=request.POST.get('_content', json.dumps(request.DATA)))

            """
            Example:
            {
                "outlines": [
                    {"first_record": ["record_type", "HDR"], "map": [["billing_address_city", "order.billing_address.city"], ["billing_address_firstname", "order.billing_address.firstname"]]},
                    {"collection": "order.line_items", "first_record": ["record_type", "DTL"], "map": [["line_item_name", "name"], ["line_item_quantity", "quantity"]]}
                ]
            }

            """

            parameters = json.loads(project.conversion_parameters)

            csv_str = ""
            for outline in parameters['outlines']:
                json2csv = Json2Csv(outline)
                json2csv.process(request.DATA)

                if not json2csv.rows or len(json2csv.rows) == 0:
                    logging.info("No data to convert for one or more outlines.")
                    return self._response(request, 'No data to convert.')

                csv_str += json2csv.write_string(write_header_row=False)

            print(csv_str)

            ConvertedMessageQueue.objects.create(original_message=original_message,
                                                 converted_message=csv_str, project=project)
        else:
            raise NotImplementedError('Currently only JSON to CSV conversion is implemented.')

        return self._response(request, 'Data converted and queued successfully.')

    def _response(self, request, summary=None, success=True):
        response_status = status.HTTP_200_OK if success else status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'request_id': request.DATA.get('request_id'), 'summary': summary}, status=response_status)