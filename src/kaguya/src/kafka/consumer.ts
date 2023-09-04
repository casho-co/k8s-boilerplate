import { KafkaConsumer } from '@cashoco/shared';
import TOPICS from './config';
import './events';

const KAFKA_BROKER: string = process.env.KAFKA_BROKER!;

const consumer = new KafkaConsumer(KAFKA_BROKER);

consumer.subscribe([TOPICS.HEALTH], 'kaguya_health_group', false);
