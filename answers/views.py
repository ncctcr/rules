from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from answers.models import Answers
from answers.serializer import AnswerSerializer, AskSerializer

#
# class TemplateView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'input_data.html'


class InputData(View):

    def get(self,request):
        return render(request, 'input_data.html')

    # def post(self, request):
    #     print(request.POST.get('gender'))
    #
    #
    #     return HttpResponse('/input_data')
    #
    #

class AnswerView(generics.ListCreateAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = AnswerSerializer
    queryset = Answers.objects.all()


class AskView(generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = AskSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)

        data = {'answers': serializer.validated_data['response']}
        return Response(data, status.HTTP_200_OK)

