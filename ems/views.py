from django.shortcuts import render
from rest_framework.decorators import api_view
from ems.models import Student
from ems.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.files.base import ContentFile
import pdfkit




# Create your views here.
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def view_func(request,pk=None):
    if request.method=='GET':
        id=pk
        if id is not None:
            #id=request.data.get('id')
            stu=Student.objects.get(id=id)
            serial=StudentSerializer(stu)
            return Response({'data':serial.data},status=status.HTTP_200_OK)
        else:
            stu=Student.objects.all()
            serial=StudentSerializer(stu,many=True)
            return Response({'data':serial.data},status=status.HTTP_200_OK)
    if request.method=='POST':
        serial=StudentSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'data':serial.data},status=status.HTTP_201_CREATED)
        else:
            return Response({'data':serial.errors},status=status.HTTP_400_BAD_REQUEST) 
    if request.method=='PUT':
        id=pk
        stu=Student.objects.get(id=id)
        serial=StudentSerializer(stu,data=request.data,many=True)
        if serial.is_valid():
            serial.save()
            return Response({'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'data':serial.errors},status=status.HTTP_404_NOT_FOUND)
    if request.method=='PATCH':
        id=pk
        stu=Student.objects.get(id=id)
        serial=StudentSerializer(stu,data=request.data,partial=True)
        if serial.is_valid():
            serial.save()
            return Response({'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'data':serial.errors},status=status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        id=pk
        stu=Student.objects.get(id=id)
        if stu is not None:
            stu.delete()
            return Response({"data":"data deleted successfully!!!"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"data":"student does not exist!!!"},status=status.HTTP_404_NOT_FOUND)



class getAPI(APIView):
    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
                try:
                    stu=Student.objects.get(id=id)
                    serial=StudentSerializer(stu)
                    return Response({'data':serial.data},status=status.HTTP_200_OK)
                except Student.DoesNotExist:
                    return Response({'data':'student does not exist'},status=status.HTTP_404_NOT_FOUND)        
        else:
            stu=Student.objects.all()
            serial=StudentSerializer(stu,many=True)
            return Response({'data':serial.data},status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serial=StudentSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'msg':'Data created successfully!!!'},status=status.HTTP_201_CREATED)
        return Response({'msg':serial.errors},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,pk,format=None):
        id=pk
        stu=Student.objects.get(id=pk)
        serial=StudentSerializer(stu,data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'msg':'data updated completely'},status=status.HTTP_202_ACCEPTED)
        return Response({'msg':serial.errors},status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk,format=None):
        id=pk
        stu=Student.objects.get(id=pk)
        serial=StudentSerializer(stu,data=request.data,partial=True)
        if serial.is_valid():
            serial.save()
            return Response({'data':'data updated partially'},status=status.HTTP_200_OK)
        return Response({'data':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        id=pk
        stu=Student.objects.get(id=id)
        stu.delete()
        return Response({'msg':'data deleted successfully!!!'},status=status.HTTP_200_OK)
    


class viewset_func(viewsets.ViewSet):
    def list(self,request):
        stu=Student.objects.all()
        serial=StudentSerializer(stu,many=True)
        return Response({'data':serial.data},status=status.HTTP_200_OK)
    def retrieve(self,request,pk=None):
        id=pk
        stu=Student.objects.get(id=id)
        serial=StudentSerializer(stu)
        return Response({'data':serial.data},status=status.HTTP_200_OK)
    def create(self,request):
        serial=StudentSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'msg':'data created successfully!!!'},status=status.HTTP_200_OK)
        else:
            return Response({'data':serial.errors},status=status.HTTP_403_FORBIDDEN)
    def update(self,request,pk=None):
        id=pk
        stu=Student.objects.get(id=id)
        serial=StudentSerializer(stu,data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({'msg':'data updated successfully!!!'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':serial.errors},status=status.HTTP_304_NOT_MODIFIED)
    def partial_update(self,request,pk=None):
        id=pk
        stu=Student.objects.get(id=id)
        serial=StudentSerializer(stu,data=request.data,partial=True)
        if serial.is_valid():
            serial.save()
            return Response({'msg':'data partially updated successfully!!!'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':serial.errors},status=status.HTTP_304_NOT_MODIFIED)
    def destroy(self,request,pk=None):
        id=pk
        stu=Student.objects.get(id=id)
        stu.delete()
        return Response({'msg':'data deleted successfully'},status=status.HTTP_200_OK)
            
    


class GeneratePdf:
    def __init__(self,**kwargs):
        self.type=kwargs.get("type",None)
        self.context=kwargs.get("context",None)
        if self.type=="user":
            self.template_name="ems/user.html"
        if self.type=="index":
            self.template_name="ems/index.html"
        if self.type=="team":
            self.template_name="ems/team.html"



    def __call__(self):
        return self.generatepdf()

    
    def generatepdf(self):
        context=self.context
        template=get_template(self.template_name)
        html_tostring=template.render(context)
        pdf=pdfkit.from_string(html_tostring)
        return pdf
    


def home(request,id):
    user=Student.objects.get(id=id)
    context={"user":user,"address":"Noida sector 65"}
    template=GeneratePdf(context =context,type="user")
    myfile=ContentFile(template())
    user.file.save(str(user.name)+".pdf",myfile)
    return HttpResponse("<h1>Response stored successfully!!!</h1>")