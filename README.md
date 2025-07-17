Opal Audio

Considerations

 - Used the synchronous GRPC and not the asyncio GRPC
 - Did not change the client.py
 - As expected from the requirements. The stop button stops the streaming sent from the server.
 - Added some error handling and connection closing print statements


Assumptions
 - Battery health is unnecessory field and will not be changed for this application
 - There is only a Button press event on the client. So we are assuming a click is press. Hold and Release do not have any meaning. Although I defined the state of the Buttons on my server code. It is not used or modified appropriately.
 - When we press stop and play again the whole file is retransmited and not a partial file. We can store where it was stopped and play from there but for now I am assuming we are using this as a music transfer system. If you want to see this as a podcast player instead. I left a PR open which you can merge to see this feature.

Issues
 - THe DeviceStatus sent by the client sends only the led values althought mode and battery_level were defined in the comms.proto. Could be for some future extention, but it was slightly confusing.
 - I found the get status from client device unnecessory as the state of the application is decided by the server.
 - The client needs to check if the device name already exists or not.
