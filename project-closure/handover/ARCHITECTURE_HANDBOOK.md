# Architecture Handbook (Knowledge Transfer)

## The Big Picture
The MSRTC platform consists of 20+ NestJS microservices running on Kubernetes (EKS/GKE).

## Key Design Patterns
1. **API Gateway:** Acts as the single entry point, handling JWT validation and rate limiting.
2. **Saga Pattern (Kafka):** Bookings are handled asynchronously. The `booking-service` emits a `BookingInitiated` event, which the `payment-service` consumes.
3. **Distributed Locking (Redis):** To prevent double-booking the same seat, we use `@msrtc/redis` for sub-millisecond distributed locks.
4. **Service Mesh (Istio):** All internal traffic is encrypted via mTLS. No service can bypass the mesh policies.
