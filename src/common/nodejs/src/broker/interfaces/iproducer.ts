import { IEvent } from './ievent';

// To be implemented by concrete producers to provide support
// for send events to topics and/ or channels
export interface IProducer {
  sendMessage(topic: string, event: IEvent): void;
}
