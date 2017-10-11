import json
import logging
from collections import OrderedDict

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from WebService.models import PhalanxIDDataModel
from WebService.serializers import PhalanxIDSerializer
from rest_framework import generics

logger = logging.getLogger('phalanx_id')


class PhalanxDataDisplayView(ListView):
    model = PhalanxIDDataModel

    def get_context_data(self, **kwargs):
        context = super(PhalanxDataDisplayView, self).get_context_data(**kwargs)
        context['phalanx_info'] = PhalanxIDDataModel.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'phalanx_table.html')


class PhalanxIDUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhalanxIDDataModel.objects.all()
    serializer_class = PhalanxIDSerializer

    def update(self, request, *args, **kwargs):
        logger.info("Update request received")
        try:
            obj = PhalanxIDDataModel.objects.get(pk=self.kwargs['pk'])
        except PhalanxIDDataModel.DoesNotExist:
            obj = None
        phalanx_id = request.data.get('phalanx_id', None)
        phalanx_uid = request.data.get('phalanx_uid', None)
        uart_test = request.data.get('uart_test', False)
        gpio_test = request.data.get('gpio_test', False)
        radio_test = request.data.get('radio_test', False)
        sender_rssi = request.data.get('sender_rssi', None)
        receiver_rssi = request.data.get('receiver_rssi', None)
        timestamp = request.data.get('timestamp', None)

        if uart_test == 'True':
            uart_test = True
        if gpio_test == 'True':
            gpio_test = True
        if radio_test == 'True':
            radio_test = True

        if obj:
            obj.uart_test = uart_test
            obj.gpio_test = gpio_test
            obj.radio_test = radio_test
            obj.sender_rssi = sender_rssi
            obj.receiver_rssi = receiver_rssi
            obj.timestamp = timestamp
            obj.save()
            logger.debug("Phalanx ID obj {} updated".format(obj.phalanx_id))
            response = OrderedDict()
            response['status'] = 'PHALANX_ID UPDATED {}'.format(obj.phalanx_id)
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            return HttpResponse(json.dumps("ERR_PHALANX_ID_NOT_FOUND"), content_type="application/json")

    def delete(self, request, *args, **kwargs):
        logger.info("Delete request received")
        try:
            obj = PhalanxIDDataModel.objects.get(pk=self.kwargs['pk'])
            logger.debug("Phalanx ID obj {} deleted".format(obj.phalanx_id))
        except PhalanxIDDataModel.DoesNotExist:
            obj = None
        response = OrderedDict()
        response['status'] = "PHALANX_ID DELETED {}".format(obj.phalanx_id)
        obj.delete()
        return HttpResponse(json.dumps(response), content_type="application/json")


class PhalanxIDView(generics.ListCreateAPIView):
    queryset = PhalanxIDDataModel.objects.all()
    serializer_class = PhalanxIDSerializer

    def post(self, request, *args, **kwargs):
        logger.info("POST request received {}".format(request.data))
        phalanx_id = request.data.get('phalanx_id', None)
        phalanx_uid = request.data.get('phalanx_uid', None)
        get_pk = request.data.get('get_pk', None)

        if phalanx_id and phalanx_uid and not get_pk:
            # First case, generate ID.
            phalanx_id = phalanx_id.upper()
            phalanx_uid = phalanx_uid.upper()

            if phalanx_id == 'FFFFFFFF' or phalanx_id == '0XFFFFFFFF':
                logger.info("Generate id, uid received={}".format(phalanx_uid))
                phalanx_id = self._generate_id()
                # phalanx_uid = int(phalanx_uid, 16)
                # phalanx_uid = "{0:#0{1}x}".format(phalanx_uid, 10)
                # Check uid uniqueness
                try:
                    exists = PhalanxIDDataModel.objects.get(phalanx_uid=phalanx_uid)
                    logger.debug("The phalanx_uid already exists {}".format(phalanx_uid))
                except PhalanxIDDataModel.DoesNotExist:
                    exists = None

                if exists:
                    response = OrderedDict()
                    response['status'] = 'ERROR, UID ALREADY EXISTS'
                    response['phalanx_uid'] = phalanx_uid
                    response['phalanx_id'] = exists.phalanx_id
                    response['uart_test'] = exists.uart_test
                    response['gpio_test'] = exists.gpio_test
                    response['radio_test'] = exists.radio_test
                    response['sender_rssi'] = exists.sender_rssi
                    response['receiver_rssi'] = exists.receiver_rssi
                    response['timestamp'] = exists.timestamp
                    return HttpResponse(json.dumps(response), content_type="application/json")

                serializer = PhalanxIDSerializer(data=request.data)
                if serializer.is_valid():
                    logger.debug("Phalanx ID created {}".format(phalanx_id))
                    state = "PHALANX_ID ASSIGNED"
                    try:
                        serializer.save(phalanx_id=phalanx_id, phalanx_uid=phalanx_uid)
                    except IntegrityError:
                        response = {"ERROR": "Try again"}
                        return HttpResponse(json.dumps(response), content_type="application/json")
                    response = serializer.data
                    response['status'] = state
                    return HttpResponse(json.dumps(response), content_type="application/json")

            # Check for prefix
            # phalanx_id = int(phalanx_id, 16)
            # phalanx_uid = int(phalanx_uid, 16)
            # phalanx_id = "{0:#0{1}x}".format(phalanx_id, 10)
            # phalanx_uid = "{0:#0{1}x}".format(phalanx_uid, 10)
            response_dict = OrderedDict()
            response_dict['phalanx_id'] = phalanx_id
            response_dict['phalanx_uid'] = phalanx_uid
            response_dict['uart_test'] = request.data.get('uart_test', False)
            response_dict['gpio_test'] = request.data.get('gpio_test', False)
            response_dict['radio_test'] = request.data.get('radio_test', False)
            response_dict['sender_rssi'] = request.data.get('sender_rssi', None)
            response_dict['receiver_rssi'] = request.data.get('receiver_rssi', None)
            response_dict['timestamp'] = request.data.get('timestamp', None)

            # Second case, check if is correct
            try:
                obj = PhalanxIDDataModel.objects.get(phalanx_id=phalanx_id)
                logger.info("Phalanx ID exists {}".format(phalanx_id))
            except PhalanxIDDataModel.DoesNotExist:
                obj = None

            if obj:
                # Check its uid
                if phalanx_uid == obj.phalanx_uid:
                    logger.debug("Phalanx ID {} and UID {} correct.".format(phalanx_id, phalanx_uid))
                    state = 'PHALANX_ID EXISTS WITH CORRECT UID'
                    response = OrderedDict()
                    response['phalanx_id'] = phalanx_id
                    response['phalanx_uid'] = phalanx_uid
                    response['uart_test'] = obj.uart_test
                    response['gpio_test'] = obj.gpio_test
                    response['radio_test'] = obj.radio_test
                    response['sender_rssi'] = obj.sender_rssi
                    response['receiver_rssi'] = obj.receiver_rssi
                    response['timestamp'] = str(obj.timestamp)
                    response['status'] = state
                else:
                    state = 'PHALANX_ID EXISTS WITH INCORRECT UID'
                    logger.debug("Phalanx ID {} and UID {} incorrect.".format(phalanx_id, phalanx_uid))
                    response = OrderedDict()
                    response['phalanx_id'] = phalanx_id
                    response['phalanx_uid'] = phalanx_uid + " Correct uid: {}".format(
                        PhalanxIDDataModel.objects.get(phalanx_id=phalanx_id).phalanx_uid)
                    response['uart_test'] = obj.uart_test
                    response['gpio_test'] = obj.gpio_test
                    response['radio_test'] = obj.radio_test
                    response['sender_rssi'] = obj.sender_rssi
                    response['receiver_rssi'] = obj.receiver_rssi
                    response['timestamp'] = str(obj.timestamp)
                    response['status'] = state

                return HttpResponse(json.dumps(response), content_type="application/json")

            else:
                # Third case, just save it
                serializer = PhalanxIDSerializer(data=response_dict)
                if serializer.is_valid():
                    logger.debug("Phalanx ID and UID saved".format(phalanx_id, phalanx_uid))
                    state = 'PHALANX_ID and UID REGISTERED'
                    serializer.save(phalanx_id=phalanx_id, phalanx_uid=phalanx_uid)
                    response = response_dict
                    response['status'] = state
                else:
                    logger.exception("Something happened Phalanx ID {} and UID {}".format(phalanx_id, phalanx_uid))
                    response = OrderedDict()
                    response['status'] = 'ERROR, UID ALREADY EXISTS'
                    response['phalanx_uid'] = phalanx_uid
                    return HttpResponse(json.dumps(response), content_type="application/json")

            return HttpResponse(json.dumps(response), content_type="application/json")

        elif get_pk:
            phalanx_id = phalanx_id.upper()
            phalanx_id = int(phalanx_id, 16)
            phalanx_id = "{0:#0{1}x}".format(phalanx_id, 10)
            try:
                pk = PhalanxIDDataModel.objects.get(phalanx_id=phalanx_id).pk
            except PhalanxIDDataModel.DoesNotExist:
                pk = 0

            if pk:
                response = OrderedDict()
                response['pk'] = pk
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                response = OrderedDict()
                response['pk'] = 'DOES NOT EXIST'
            return HttpResponse(json.dumps(response), content_type="application/json")

        elif phalanx_id:
            phalanx_id = phalanx_id.upper()
            phalanx_id = int(phalanx_id, 16)
            phalanx_id = "{0:#0{1}x}".format(phalanx_id, 10)
            try:
                obj = PhalanxIDDataModel.objects.get(phalanx_id=phalanx_id)
            except PhalanxIDDataModel.DoesNotExist:
                obj = None
            if obj:
                response = OrderedDict()
                response['phalanx_id'] = obj.phalanx_id
                response['phalanx_uid'] = obj.phalanx_uid
                response['uart_test'] = obj.uart_test
                response['gpio_test'] = obj.gpio_test
                response['radio_test'] = obj.radio_test
                response['sender_rssi'] = obj.sender_rssi
                response['receiver_rssi'] = obj.receiver_rssi
                response['timestamp'] = str(obj.timestamp)
                response['status'] = 'ID EXISTS'
            else:
                response = OrderedDict()
                response['phalanx_id'] = phalanx_id
                response['status'] = 'ID DOES NOT EXIST'
            return HttpResponse(json.dumps(response), content_type="application/json")

        else:
            serializer = PhalanxIDSerializer(data=request.data)
            if not serializer.is_valid():
                return super(PhalanxIDView, self).post(request, *args, **kwargs)

    @staticmethod
    def _generate_id():
        logger.info("Generating ID")
        list_id = []
        try:
            numbers = PhalanxIDDataModel.objects.all()
        except PhalanxIDDataModel.DoesNotExist:
            numbers = None
        if numbers:
            for number in numbers:
                list_id.append(number.phalanx_id)

            last_id = int(max(list_id), 16)
            phalanx_id = last_id + 1
            phalanx_id = "{0:#0{1}x}".format(phalanx_id, 10)
        else:
            phalanx_id = "{0:#0{1}x}".format(1, 10)
            logger.debug("Phalanx ID {} generated".format(phalanx_id))
        return phalanx_id
