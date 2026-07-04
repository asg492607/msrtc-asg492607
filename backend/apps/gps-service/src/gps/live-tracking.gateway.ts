import { 
  WebSocketGateway, 
  WebSocketServer, 
  SubscribeMessage, 
  MessageBody, 
  ConnectedSocket 
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({ cors: true, namespace: '/live-tracking' })
export class LiveTrackingGateway {
  @WebSocketServer()
  server: Server;

  /**
   * Passengers subscribe to a specific trip ID to get live location updates.
   */
  @SubscribeMessage('subscribe_trip')
  handleSubscribe(@MessageBody('tripId') tripId: string, @ConnectedSocket() client: Socket) {
    const room = `trip_${tripId}`;
    client.join(room);
    return { event: 'subscribed', room };
  }

  /**
   * Called by the internal GpsService when a new ping is processed.
   */
  broadcastLocation(tripId: string, payload: any) {
    this.server.to(`trip_${tripId}`).emit('location_update', payload);
  }
}
