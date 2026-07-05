# Feature Flag Guide

## Decoupling Deployment from Release
Code deployment (pushing to Kubernetes) should be boring. Releasing a feature (turning it on for users) is a business decision.

## `feature-flag-service`
To wrap a new risky feature:
```typescript
const isEnabled = await this.ffService.isEnabled('NEW_PAYMENT_GATEWAY');
if (isEnabled) {
   // Execute new logic
} else {
   // Fallback to old logic
}
```
If the new payment gateway crashes in production, a Product Manager simply toggles the flag to `false` via the API. The Redis cache expires in 5 minutes, instantly routing users back to the safe code without requiring a hotfix deployment.
