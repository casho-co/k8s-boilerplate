import { IConsumer } from '../interfaces/iconsumer';
import { IConsumerConfiguration } from '../interfaces/iconsumer-configuration';
import { KafkaConsumer } from '../kafka/kafka-consumer';

export const ConsumerType = {
  KAFKA: 'Kafka',
};

// Helps with creation of a IConsumer base on
// the configuration sent
export class ConsumerFactory {
  static getConsumer(metadata: IConsumerConfiguration): IConsumer | undefined {
    if (metadata.type === ConsumerType.KAFKA) {
      return new KafkaConsumer(metadata.broker);
    }
    return undefined;
  }
}
