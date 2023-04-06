import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.apps import apps


class ReportConsumer(AsyncJsonWebsocketConsumer):

    async def websocket_connect(self, event):
        await self.accept()
        await self.send(
            json.dumps({
                "type": "websocket.accept",
                "system": "Connected",
            })
        )
        report_model = apps.get_model('social', 'Report')

        user = self.scope['user']
        properties_model = apps.get_model('properties', 'Properties')
        properties = await sync_to_async(properties_model.objects.filter, thread_sensitive=True) \
            (user=user)
        try:
            reports = await sync_to_async(report_model.objects.filter)(content_object__in=properties)
            report = await sync_to_async(reports.get, thread_sensitive=True) \
                (id=self.scope['url_route']['kwargs']['report_id'])
            await self.send(
                json.dumps({
                    "type": "websocket.send",
                    "system": "Connected to report",
                    "text": f"Connected to report {report.id}",
                })
            )
        except report_model.DoesNotExist:
            print("Report not found")
            await self.close(code=4004)
        except Exception as e:
            print(e)
            await self.close(code=4002)

    async def websocket_receive(self, event):
        user = self.scope['user']
        try:
            report_model = apps.get_model('social', 'Report')
            report_messages_model = apps.get_model('social', 'ReportMessages')
            properties_model = apps.get_model('properties', 'Properties')
            properties = await sync_to_async(properties_model.objects.filter, thread_sensitive=True) \
                (user=user)
            reports = await sync_to_async(report_model.objects.filter)(content_object__in=properties)
            report = await sync_to_async(reports.get) \
                (id=self.scope['url_route']['kwargs']['report_id'])
            message_db = await sync_to_async(report_messages_model.objects.filter)(report=report)
            message_db = message_db.last()
            if message_db is None or message_db.user != self.scope['user']:
                report_messages_model.objects.create(
                    report=report,
                    user=self.scope['user'],
                    message=event['text'],
                )
                await self.send(
                    json.dumps({
                        "type": "websocket.send",
                        "code": 2001,
                        "system": "Sent",
                    })
                )
            else:
                await self.send(
                    json.dumps({
                        "type": "websocket.send",
                        "code": 4003,
                        "text": "You can't send two messages in a row",
                    })
                )
        except Exception as e:
            await self.send(
                json.dumps({
                    "type": "websocket.send",
                    "code": 4002,
                    "system": f"Error {e}",
                })
            )

    async def websocket_disconnect(self, event):
        print("Disconnected", event)
        print(self.scope['url_route']['kwargs'])

