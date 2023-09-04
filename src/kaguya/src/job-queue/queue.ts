import { Queue } from 'bullmq';

export enum QUEUES {
  CHECK = 'Check',
}

export function getQueue(): Queue {
  return new Queue(QUEUES.CHECK, {
    connection: {
      host: process.env.REDIS_HOST,
      port: Number(process.env.REDIS_PORT),
    },
  });
}
