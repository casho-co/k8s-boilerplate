// Events will follow this specific interface to be
// sent across via the message broker/ service bus
export interface IEvent {
  eventType: string;
  data: any;
  createdAt?: string;
}
