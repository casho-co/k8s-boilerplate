import { Job } from 'bullmq';
import { KafkaProducer, logger, topicsRegistry } from '@cashoco/shared';
import { JobStore } from './models'
import TOPICS from '../kafka/config';

export async function jobHandler(job: Job): Promise<void> {
  const userId = job.data.userId;
  const userEmail = job.data.userEmail;
  const platform = job.data.platform;
  const trackerId = job.data.trackerId;
  const producer = KafkaProducer.getInstance(process.env.KAFKA_BROKER!);
  const event = {
    eventType: topicsRegistry[TOPICS.HEALTH].produce_check_health(),
    data: 'check check',
  };
  producer.sendMessage(TOPICS.HEALTH, event);
  
}

export async function handleState(id: string, state: string, payload: object, trackerId?: string) {
  const jobEvent = new JobStore({
    jobId: id,
    jobState: state,
    payload: payload,
    createdAt: new Date(),
    trackerId: trackerId,
  });
  try {
    jobEvent.save();
  } catch (err) {
    logger.info(`error occured while adding job state :${err}`);
  }
}
