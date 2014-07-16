from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from MyProject.MyApp import CalcClass
from message_converter.dict2csv import Dict2Csv
from message_converter.models import IncomingMessage, ConvertedMessageQueue, ApiProject


class ApiProjectView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        # Any URL parameters get passed in **kw
        # myClass = CalcClass(get_arg1, get_arg2, *args, **kw)
        # result = myClass.do_work()

        result = ((1, 2, 3, ), (4, 5, get_arg1,))
        #
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kw):
        # the raw json is in request.POST['_content']
        # application/json is in request.POST['_content_type']
        # djangorest loads the json into dict request.DATA

        if not 'project_name' in kw:
            raise Http404

        try:
            project = ApiProject.objects.get(name=kw['project_name'])
        except ApiProject.DoesNotExist:
            raise Http404

        if project.from_type.type == 'JSON' and project.to_type.type == 'CSV':
            original_message = IncomingMessage.objects.create(project=project, message=request.POST['_content_type'])

            # json:
            # [{"map": [["billing_address_city", "billing_address.city"], ["billing_address_firstname", "billing_address.firstname"]], "first_record": ["record_type", "HDR"]},
            # {"map": [["line_item_name", "name"], ["line_item_quantity", "quantity"]], "first_record": ["record_type", "DTL"], "collection": "line_items"}]
            # outlines = json.loads(project.conversion_argument)
            # for outline in outlines:

            # Convert to HDR record
            outline = {"map": [['billing_address_city', 'billing_address.city'], ['billing_address_firstname', 'billing_address.firstname']], "first_record": ['record_type', 'HDR']}
            dict2csv = Dict2Csv(outline)
            dict2csv.process_each_item_as_row([request.DATA])
            csv_str = dict2csv.write_string(write_header_row=False)

            # Convert each DTL record
            outline = {
                "map": [['line_item_name', 'name'], ['line_item_quantity', 'quantity']],
                "collection": "line_items",
                "first_record": ['record_type', 'DTL']
            }

            dict2csv = Dict2Csv(outline)
            dict2csv.process_each_item_as_row(request.DATA)
            csv_str += dict2csv.write_string(write_header_row=False)
            print(csv_str)

            ConvertedMessageQueue.objects.create(original_message=original_message,
                                                 converted_message=csv_str, project=project)
        else:
            raise NotImplementedError('Currently only JSON to CSV conversion is implemented.')

        message = 'Data converted and queued successfully.'
        return Response(message, status=status.HTTP_200_OK)