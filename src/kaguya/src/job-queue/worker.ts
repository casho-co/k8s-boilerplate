import { Worker } from 'bullmq';
import { jobHandler, handleState } from './handler';
import connectDB from '../database';
import { logger } from '@cashoco/shared';
import { QUEUES } from './queue';
import '../kafka/events';

connectDB();

// Create the worker
const emailWorker = new Worker(QUEUES.CHECK, jobHandler, {
  connection: {
    host: process.env.REDIS_HOST!,
    port: +process.env.REDIS_PORT!,
  },
  concurrency: 1,
});

// Event listeners for the worker
emailWorker.on('active', (job) => {
  logger.info(`Job ${job.id} is active`);
  handleState(job.id!, 'active', job.data, job.data.trackerId);
});

emailWorker.on('completed', async (job) => {
  console.log(`Job ${job.id} has been completed!`);
  const userId = job.data.userId;
  const userEmail = job.data.userEmail;
  const platform = job.data.platform;
  handleState(job.id!, 'completed', job.data, job.data.trackerId);
});

// the job is possibly undefiend
emailWorker.on('failed', (job, error) => {
  if (job) {
    console.log(`Job ${job.id} has been failed , error:${JSON.stringify(error)}`);
    handleState(job.id!, 'failed', { error: JSON.stringify(error) }, job.data.trackerId);
  }
});

emailWorker.on('progress', (job, progress) => {
  console.log(`Job ${job.id} is in progress: ${progress}`);
  handleState(job.id!, 'progress', { data: job.data, progress: progress }, job.data.trackerId);
});

emailWorker.on('stalled', async (jobId, error) => {
  console.log(`Job ${jobId} is stalled : ${JSON.stringify(error)}`);
  handleState(jobId, 'stalled', { error: JSON.stringify(error) });
});
