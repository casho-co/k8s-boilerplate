// The configuration to be passed to the producer factory
// for creation of different types of producers

export interface IProducerConfiguration {
  type: string;
  broker: string;
}
