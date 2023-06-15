import { IProducer } from '../interfaces/iproducer';
import { IProducerConfiguration } from '../interfaces/iproducer-configuration';
import { KafkaProducer } from '../kafka/kafka-producer';

export const ProducerType = {
  KAFKA: 'Kafka',
};

// Helps with creation of a IProducer based on
// the configuration sent
export class ProducerFactory {
  private static kafkaProducers: Record<string, IProducer> = {};

  static getProducer(metadata: IProducerConfiguration): IProducer | undefined {
    if (metadata.type === ProducerType.KAFKA) {
      return this.getKafkaProducer(metadata.broker);
    }
    return undefined;
  }

  private static getKafkaProducer(broker: string): IProducer {
    if (this.kafkaProducers[broker] !== undefined) {
      return this.kafkaProducers[broker];
    } else {
      const producer = KafkaProducer.getInstance(broker);
      this.kafkaProducers[broker] = producer;
      return producer;
    }
  }
}
