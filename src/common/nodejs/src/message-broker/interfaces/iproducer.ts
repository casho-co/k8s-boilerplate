import { IEvent } from './ievent';
import { IMetadata } from './imetadata';

// To be implemented by concrete producers to provide support
// for send events to topics and/ or channels
export interface IProducer {
  sendMessage(metadata: IMetadata, event: IEvent): void;
}
