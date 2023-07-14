import { IEvent } from './ievent';

// To be implemented by concrete consumers to provide support
// for listening events on specific topics and/ or channels
export interface IConsumer {
  subscribe(topics: string[], consumerGroup: string, fromBeginning?: boolean): Promise<void>;
}
