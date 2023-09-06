import { model, Schema } from 'mongoose';

export interface IJobStore {
  jobId: string;
  jobState: string;
  payload: object;
  createdAt: string;
  trackerId?: string;
}

const JobStoreSchema: Schema = new Schema({
  jobId: { type: String, required: true },
  jobState: { type: String, required: true },
  payload: { type: Object, required: true },
  createdAt: { type: Date, required: true },
  trackerId: { type: String, required: false, default: null },
});
export const JobStore = model<IJobStore>('JobStore', JobStoreSchema);
