// The configuration to be passed to the consumer factory
// for creation of different types of consumers

export interface IConsumerConfiguration {
  type: string;
  broker: string;
}
